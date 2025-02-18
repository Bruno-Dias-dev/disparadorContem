from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from src.services.agendamento_service import listar_agendamentos

scheduler = BackgroundScheduler(timezone=pytz.UTC)

def disparar_mensagens():
    """Verifica os agendamentos e dispara mensagens no horário correto"""
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"🔔 Verificando agendamentos para {agora}...")

    agendamentos = listar_agendamentos()
    for agendamento in agendamentos:
        horario_agendado = agendamento["horario_disparo"].strftime("%H:%M:%S")
        if horario_agendado == agora:
            print(f"📢 Enviando mensagem do Grupo {agendamento['grupo_id']}: {"Agendamento"}")

# Configurei para rodar a cada minuto
scheduler.add_job(disparar_mensagens, "interval", minutes=1)

def iniciar_scheduler():
    scheduler.start()
