from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import time
import random
import concurrent.futures # Importar para usar ThreadPoolExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from src.services.agendamento_service import listar_agendamentos, registrar_log_envio
from src.services.mensagens_service import get_grupo_by_id, get_msg_by_id
from src.api_module.envio_cobranca import envio_via_banco, envio_log # Ajuste se 'envio_log' estiver em outro lugar
from src.api_module.gera_mensagem_ia import reescrever_mensagem
from src.services.mensagens_service import get_faturas_por_grupo

# Configurar o scheduler com um ThreadPoolExecutor
# O max_workers define quantas tarefas podem rodar em paralelo.
# Ajuste este número conforme a capacidade do seu servidor e APIs.
scheduler = BackgroundScheduler(
    timezone=pytz.UTC,
    executors={'default': ThreadPoolExecutor(max_workers=5)}
)

def enviar_mensagens_para_grupo(agendamento_data):
    """
    Função dedicada a enviar mensagens para um ÚNICO grupo.
    Executará em sua própria thread.
    """
    agendamento_id = agendamento_data["id"]
    conexao_id = str(agendamento_data["conexao_id"])
    departamento_id = str(agendamento_data["departamento_id"])
    grupo_id = agendamento_data["grupo_id"]
    
    print(f"🚀 Iniciando envio para agendamento {agendamento_id} (Grupo {grupo_id}) em uma nova thread.")
    
    # Log de início de envio (opcional, remova se for muito verboso)
    envio_log(data_msg={
        "text": f"Iniciando envio de mensagens para Agendamento {agendamento_id}",
        "serviceId": conexao_id,
        "departmentId": departamento_id,
        "celular": str("(85)989400378") # Celular fixo para log, ajuste se necessário
    })
    
    inicio_envio = datetime.now()
    qtd_enviados = 0
    qtd_falha = 0
    
    try:
        faturas = get_faturas_por_grupo(grupo_id)
        if not faturas:
            print(f"ℹ️ Agendamento {agendamento_id}: Nenhuma fatura encontrada para o grupo {grupo_id}.")
            return
        
        envia_pdf = get_grupo_by_id(grupo_id)["pdf"]
        
        # Mantenha essa lógica se você sempre pega a primeira mensagem
        mensagem_id = agendamento_data["mensagem_ids"][0] 
        mensagem_cadastrada = get_msg_by_id(mensagem_id)
        
        total_faturas = len(faturas)
        
        for i, fatura in enumerate(faturas):
            try:
                mensagem_gerada = reescrever_mensagem(mensagem_cadastrada)
                data_msg = {
                    "text": mensagem_gerada,
                    "serviceId": conexao_id,
                    "departmentId": departamento_id,
                    "celular": str(fatura.get("celular")) # Use o celular da fatura!
                }
                
                envio_via_banco(data_msg, fatura, envia_pdf)
                qtd_enviados += 1
            except Exception as e:
                print(f"⚠️ Falha ao enviar para fatura {fatura.get('codigo_da_fatura', '')} (Grupo {grupo_id}): {e}")
                qtd_falha += 1
            
            # Log de progresso
            print(f"Agendamento {agendamento_id}: {i+1}/{total_faturas} faturas processadas.")
            
            # Intervalo aleatório para não sobrecarregar as APIs
            intervalo = random.uniform(5, 15)
            time.sleep(intervalo)
            
    except Exception as e:
        print(f"❌ Erro crítico no agendamento {agendamento_id} (Grupo {grupo_id}): {e}")
    finally:
        final_envio = datetime.now()
        
        # Log de finalização de envio
        envio_log(data_msg={
            "text": f"Finalização envio Agendamento {agendamento_id}: {qtd_enviados} enviados, {qtd_falha} falhas",
            "serviceId": conexao_id,
            "departmentId": departamento_id,
            "celular": str("(85)989400378") # Celular fixo para log, ajuste se necessário
        })
        
        registrar_log_envio(
            agendamento_id,
            inicio_envio,
            final_envio,
            qtd_enviados,
            qtd_falha
        )
        print(f"✅ Agendamento {agendamento_id} (Grupo {grupo_id}) finalizado.")


def disparar_mensagens():
    """
    Verifica os agendamentos e agenda suas execuções em threads separadas.
    Esta função roda no thread principal do scheduler.
    """
    agora_dt = datetime.now(pytz.UTC) # Use datetime com timezone para comparação
    agora_str = agora_dt.strftime("%d/%m/%Y %H:%M") # Formato para comparação com agendamentos do DB

    print(f"🔔 Verificando agendamentos para {agora_str}...")

    agendamentos = listar_agendamentos()
    if not agendamentos:
        print("🔔 Nenhum agendamento encontrado.")
        return
    
    # Criar um conjunto para armazenar os IDs dos agendamentos já processados nesta rodada
    # Isso evita agendar o mesmo job múltiplas vezes no mesmo minuto se listar_agendamentos
    # puder retornar o mesmo agendamento.
    processed_agendamentos = set() 

    for agendamento in agendamentos:
        horario_agendado = agendamento["horario_disparo"].strftime("%d/%m/%Y %H:%M")
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        print(f"🕒 Agendamento: {horario_agendado} | Agora: {agora}")        

        # O agendamento só deve ser disparado uma vez para a hora atual
        if horario_agendado == agora:
            agendamento_unique_id = agendamento["id"] # Use o ID do agendamento como identificador único
            
            if agendamento_unique_id in processed_agendamentos:
                print(f"Agendamento {agendamento_unique_id} já processado nesta rodada. Pulando.")
                continue

            print(f"🕒 Agendamento {agendamento_unique_id} detectado para disparo. Horário: {horario_agendado}")
            
            # Dispara a função 'enviar_mensagens_para_grupo' em uma nova thread
            # usando o executor 'default' configurado no scheduler.
            scheduler.add_job(enviar_mensagens_para_grupo, args=[agendamento],
                              id=f"agendamento_disparo_{agendamento_unique_id}_{agora_str}", # ID único para o job do APScheduler
                              executor='default',
                              replace_existing=True) # Impede que o mesmo job seja adicionado se já existir um com o mesmo ID
            
            processed_agendamentos.add(agendamento_unique_id) # Adiciona ao set de processados

        # else:
        #     print(f"🕒 Agendamento {agendamento_unique_id}: {horario_agendado_str} não corresponde a {agora_str}")


# Configurei para rodar a cada minuto
scheduler.add_job(disparar_mensagens, "interval", minutes=1, id="main_disparador_job")

def iniciar_scheduler():
    """Inicia o scheduler."""
    print("⏰ APScheduler iniciado. Verificando agendamentos a cada minuto...")
    scheduler.start()
