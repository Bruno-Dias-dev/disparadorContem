from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from src.utils.logs import log_info
import time

def resolver_captcha(driver, chave_api):
    try:
        log_info("Tentando resolver o CAPTCHA")
        chave_recaptcha = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        time.sleep(10)
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(chave_api)
        solver.set_website_url(driver.current_url)
        solver.set_website_key(chave_recaptcha)
        resposta = solver.solve_and_return_solution()

        if not resposta:
            raise ValueError("Falha ao resolver o CAPTCHA via serviço de terceiros.")
        time.sleep(10)
        # Injetando a resposta do reCAPTCHA no campo esperado
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{resposta}'")

        # Aguarda alguns segundos para o site validar o reCAPTCHA (o tempo pode variar)
        time.sleep(10)
        
        log_info("CAPTCHA resolvido com sucesso")
    except Exception as e:
        raise RuntimeError(f"Erro ao resolver CAPTCHA: {e}")