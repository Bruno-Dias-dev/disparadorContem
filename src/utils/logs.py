from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_info(mensagem):
    print(f"[INFO - {datetime.now()}]: {mensagem}")

def log_erro(mensagem):
    print(f"[ERRO - {datetime.now()}]: {mensagem}")
