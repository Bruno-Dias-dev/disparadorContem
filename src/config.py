import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils.logs import log_info
from src.utils.handle_element import acessar_pagina 
from datetime import datetime

def iniciar_navegacao(url):
    log_info("Inicializando navegador")
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.expanduser("/opt/airflow/downloads"),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    log_info("WebDriver inicializado com sucesso")
    acessar_pagina(driver, url+'/login')
    time.sleep(10)

    return driver, datetime.now()
