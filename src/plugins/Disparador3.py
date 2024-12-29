import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()
LOGIN_USUARIO = os.getenv("LOGIN_USUARIO")
LOGIN_SENHA = os.getenv("LOGIN_SENHA")

# URL do sistema
URL_LOGIN = "https://grupocontem.digisac.chat/login"

# Funções para log
def log_info(mensagem):
    print(f"[INFO - {datetime.now()}]: {mensagem}")

def log_erro(mensagem):
    print(f"[ERRO - {datetime.now()}]: {mensagem}")

# Função para iniciar o navegador
def iniciar_navegacao(mensagem):
    try:
        log_info("Iniciando a navegação do robô")
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        log_info("WebDriver inicializado com sucesso")

        driver.get(URL_LOGIN)
        log_info("Página de login acessada")
        time.sleep(5)

        Preencher_login(driver)
        time.sleep(5)

        planilha = pd.read_excel('downloads/Fatura_NLWW5K3S3T5F241223154656.xlsx')
        filtro = planilha[(planilha['Data de Vencimento'] == "25/12/2024") &
                          (~planilha['Alerta'].str.contains('NÃO COBRAR', na=False)) &
                          (planilha['Data do Pagamento'].isnull())]

        relatorio = []

        for _, cliente in filtro.iterrows():
            nome_cliente = cliente['Nome Titular']
            codigo_fatura = cliente['Código da Fatura']
            log_info(f"Processando cliente: {nome_cliente}")
            try:
                processar_cliente(driver, nome_cliente, codigo_fatura, mensagem)
                status = 'Sucesso'
            except Exception as e:
                status = f'Erro: {str(e)}'

            relatorio.append({
                'Nome do Cliente': nome_cliente,
                'Código da Fatura': codigo_fatura,
                'Status': status
            })
            driver.refresh()

        pd.DataFrame(relatorio).to_excel('relatorio_envio.xlsx', index=False)
        log_info("Relatório gerado com sucesso")

    except Exception as e:
        log_erro(f"Erro durante o processo: {str(e)}")
    finally:
        time.sleep(5)
        driver.quit()
        log_info("WebDriver encerrado")

# Funções para manipulação de elementos
def aguardar_elemento(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def aguardar_elemento_clicavel(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))

# Função para login
def Preencher_login(driver):
    try:
        log_info("Preenchendo o login")
        aguardar_elemento(driver, By.ID, "username").send_keys(LOGIN_USUARIO)
        time.sleep(2)
        aguardar_elemento(driver, By.ID, "password").send_keys(LOGIN_SENHA)
        time.sleep(2)
        aguardar_elemento(driver, By.CSS_SELECTOR, "button[data-testid='login-button-login']").click()
        log_info("Login realizado com sucesso")
    except Exception as e:
        log_erro(f"Erro ao realizar login: {e}")

# Função para processar cliente
def processar_cliente(driver, nome, codigo_fatura, mensagem):
    try:
        log_info(f"Pesquisando cliente: {nome}")
        aguardar_elemento(driver, By.CSS_SELECTOR, "input[data-testid='chat-input-search_by_name_or_number']").send_keys(nome)
        time.sleep(1)

        aguardar_elemento(driver, By.CSS_SELECTOR, "div[data-testid='chat-tab-start_conversation']").click()
        time.sleep(2)

        aguardar_elemento(driver, By.CSS_SELECTOR, ".ReactVirtualized__Grid__innerScrollContainer > div:first-child").click()
        log_info("Contato selecionado")
        time.sleep(2)

        link_fatura = f"https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo={codigo_fatura}"
        mensagem_final = mensagem.replace("{link}", link_fatura)

        enviar_mensagem(driver, mensagem_final)
    except Exception as e:
        log_erro(f"Erro ao processar cliente: {e}")

# Função para enviar mensagem
def enviar_mensagem(driver, mensagem):
    try:
        log_info("Enviando mensagem...")
        text_area = aguardar_elemento(driver, By.CSS_SELECTOR, "textarea.reply-text-area")
        text_area.send_keys(mensagem)
        #text_area.send_keys("\ue007")
        time.sleep(2)
        log_info("Mensagem enviada com sucesso")
    except Exception as e:
        log_erro(f"Erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    mensagem_template = (
        "👋Olá! O boleto do seu plano de saúde e/ou odontológico VENCERÁ NO DIA 25/12/2024.\n\n"
        "🤔Não se esqueça de efetuar o pagamento, para garantia da prestação de serviço.\n\n"
        "❓Qualquer dúvida, podemos te dar o suporte aqui 👇🏻\n\n"
        "Segue link da fatura: {link}"
    )
    iniciar_navegacao(mensagem_template)
