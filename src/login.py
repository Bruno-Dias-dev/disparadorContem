import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By  
from src.utils.handle_element import aguardar_elemento, aguardar_elemento_clicavel
from src.utils.logs import log_info
from src.captcha import resolver_captcha
load_dotenv()

def realizar_login(driver, usuario, senha):
    resolver_captcha(driver,os.getenv("ANTI_CAPTCHA_API_KEY"))
    log_info("Preenchendo o login")
    user_field = aguardar_elemento(driver, By.NAME, "login")
    user_field.send_keys(usuario)
    pass_field = aguardar_elemento(driver, By.NAME, "senha")
    pass_field.send_keys(senha)
    
    log_info("Realizando login")
    btn_login = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, ".btn.btn-blue.btn-block")
    btn_login.click()
