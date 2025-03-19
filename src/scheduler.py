from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from src.services.agendamento_service import listar_agendamentos
from src.services.mensagens_service import *
from src.api_module.envio_cobranca import *

scheduler = BackgroundScheduler(timezone=pytz.UTC)

def disparar_mensagens():
    """Verifica os agendamentos e dispara mensagens no horário correto"""
    agora = datetime.now().strftime("%H:%M")
    print(f"🔔 Verificando agendamentos para {agora}...")

    agendamentos = listar_agendamentos()
    for agendamento in agendamentos:
        horario_agendado = agendamento["horario_disparo"].strftime("%H:%M")
        print(f"🕒 Agendamento: {horario_agendado} | Agora: {agora}")
        if horario_agendado == agora: 
            faturas = get_faturas_por_grupo(agendamento["grupo_id"])
            pdf = get_grupo_by_id(agendamento["grupo_id"])["pdf"]
            
            envio_via_banco(faturas,pdf)   
            print(f"🚀 Mensagens disparadas para o grupo {agendamento['grupo_id']}")

# Configurei para rodar a cada minuto
scheduler.add_job(disparar_mensagens, "interval", minutes=1)

def iniciar_scheduler():
    scheduler.start()
