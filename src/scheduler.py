from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import time
import random
from src.services.agendamento_service import listar_agendamentos, registrar_log_envio
from src.services.mensagens_service import *
from src.api_module.envio_cobranca import *
from src.api_module.gera_mensagem_ia import reescrever_mensagem

scheduler = BackgroundScheduler(timezone=pytz.UTC)

def disparar_mensagens():
    """Verifica os agendamentos e dispara mensagens no horário correto"""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    # print(f"🔔 Verificando agendamentos para {agora}...")

    agendamentos = listar_agendamentos()
    if not agendamentos:
        print("🔔 Nenhum agendamento encontrado.")
        return
    for agendamento in agendamentos:
        horario_agendado = agendamento["horario_disparo"].strftime("%d/%m/%Y %H:%M")
        print(f"🕒 Agendamento: {horario_agendado} | Agora: {agora}")
        # horario_agendado = agora
        if horario_agendado == agora: 
            envio_log(data_msg={
                "text": "Iniciando envio de mensagens",
                "service_id": str(agendamento["conexao_id"]),
                "celular": str("(85)989400378")
                })
            inicio_envio = datetime.now()
            qtd_enviados = 0
            qtd_falha = 0
            
            faturas = get_faturas_por_grupo(agendamento["grupo_id"])
            envia_pdf = get_grupo_by_id(agendamento["grupo_id"])["pdf"]            
            mensagem_id = agendamento["mensagem_ids"][0]
            mensagem_cadastrada = get_msg_by_id(mensagem_id)      
                      
            for fatura in faturas:
                try:
                    mensagem_gerada = reescrever_mensagem(mensagem_cadastrada)
                    data_msg = {
                        "text": mensagem_gerada,
                        "service_id": str(agendamento["conexao_id"]),
                        "departmentId": str(agendamento["departamento_id"])
                    }                  
                    envio_via_banco(data_msg,fatura,envia_pdf)
                    qtd_enviados += 1
                except Exception as e:
                    print(f"⚠️ Falha ao enviar para fatura {fatura['id']}: {e}")
                    qtd_falha += 1
                    
                intervalo = random.uniform(7, 30)
                print(f"⏳ Aguardando {intervalo:.2f} segundos antes do próximo envio...")
                time.sleep(intervalo)  
                
            final_envio = datetime.now()
            envio_log(data_msg={
                "text": f"Finalização do envio de mensagens - finalizado às {final_envio}: {qtd_enviados} enviados, {qtd_falha} falhas",
                "service_id": str(agendamento["conexao_id"]),
                "celular": str("(85)989400378")
                })
            registrar_log_envio(
                agendamento["id"],
                inicio_envio,
                final_envio,
                qtd_enviados,
                qtd_falha
            )        

# Configurei para rodar a cada minuto
scheduler.add_job(disparar_mensagens, "interval", minutes=1)

def iniciar_scheduler():
    scheduler.start()
