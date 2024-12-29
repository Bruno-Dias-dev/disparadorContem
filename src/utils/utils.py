from datetime import datetime

def log_acao(mensagem):
    print(f"[LOG - {datetime.now()}]: {mensagem}")
