import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Carrega variáveis de ambiente
CHAVEAPI = os.getenv("ANTI_CAPTCHA_API_KEY")
LOGIN_USUARIO = os.getenv("SISTEMA_LOGIN")
LOGIN_SENHA = os.getenv("SISTEMA_SENHA")

URL_LOGIN = "https://www.digitalsaude.com.br/login"
URL_RELATORIO = "https://www.digitalsaude.com.br/operacional/relatorio/ExibirImprimirRelatorioContrato"
URL_PROCESSOS = "https://www.digitalsaude.com.br/global/processo/ListarProcesso"

# Função para logar ações realizadas pelo robô
def log_info(mensagem):
    print(f"[INFO - {datetime.now()}]: {mensagem}")

def log_erro(mensagem):
    print(f"[ERRO - {datetime.now()}]: {mensagem}")

def iniciar_navegacao():
    try:
        log_info("Iniciando a navegação do robô")

        # Configurações do Chrome
        chrome_options = Options()
        prefs = {
            "download.default_directory": os.path.expanduser("/opt/airflow/downloads"),
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Caso queira executar em modo headless
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        log_info("WebDriver inicializado com sucesso")

        # Acessa a página de login
        driver.get(URL_LOGIN)

        time.sleep(10)
        aguardar_elemento(driver, By.CLASS_NAME, 'g-recaptcha')
        log_info("Página de login acessada")
        time.sleep(10)
        #Preencher Login
        Preencher_login(driver)
        time.sleep(10)
        # Resolver CAPTCHA
        resolver_captcha(driver)
        time.sleep(10)
        # Realizar login
        realizar_login(driver)
        time.sleep(5)
        # Armazena o momento da execução antes de gerar o relatório
        
        
        
        # Gera o relatório
        HORAEXECUCAO = gerar_relatorio(driver)
        time.sleep(10)
        # Baixa o relatório
        baixar_relatorio(driver, HORAEXECUCAO)
        time.sleep(10)
        log_info("Processo concluído com sucesso")
    except Exception as e:
        log_erro(f"Erro durante o processo: {str(e)}")
    finally:
        # Aguarda alguns segundos antes de fechar (caso precise garantir o download)
        time.sleep(50)
        if 'driver' in locals():
            driver.quit()
            log_info("WebDriver encerrado")

def aguardar_elemento(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def aguardar_elemento_clicavel(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))

def resolver_captcha(driver):
    try:
        log_info("Tentando resolver o CAPTCHA")
        chave_recaptcha = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        time.sleep(10)
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(CHAVEAPI)
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

def Preencher_login(driver):
    try:
        log_info("Preenchendo o login")

        # Aguarda o campo de login para inserir o usuário
        user_field = aguardar_elemento(driver, By.NAME, "login")
        user_field.send_keys(LOGIN_USUARIO)
        time.sleep(3)
        # Aguarda o campo de senha para inserir a senha
        pass_field = aguardar_elemento(driver, By.NAME, "senha")
        pass_field.send_keys(LOGIN_SENHA)
        time.sleep(3)
     
    except Exception as e:
        raise RuntimeError(f"Erro ao realizar login: {e}")


def realizar_login(driver):
    try:
        log_info("Realizando login no sistema")

        time.sleep(3)
        # Aguarda e clica no botão de login
        btn_login = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, ".btn.btn-blue.btn-block")
        btn_login.click()
        time.sleep(5)
       
        log_info("Login realizado com sucesso")
    except Exception as e:
        raise RuntimeError(f"Erro ao realizar login: {e}")
    
def gerar_relatorio(driver):
    try:
        log_info("Acessando página para gerar relatório")
        driver.refresh()
        driver.get(URL_RELATORIO)
        driver.refresh()
        time.sleep(10)

        # Aguarda a presença do seletor de relatório
        aguardar_elemento(driver, By.NAME, "idRelatorio")
        time.sleep(10)

        # Aplica os filtros marcando todos
        filtros = ["idConvenioArray", "convenio-cancelado", "idStatusContratoArray"]
        for filtro in filtros:
            # Aguarda link de "marcar todos"
            time.sleep(10)
            link_marcar_todos = aguardar_elemento_clicavel(driver, By.XPATH, f"//a[contains(@href, \"marcarTodos('{filtro}'\")]")
            link_marcar_todos.click()
        
        time.sleep(10)

        # Seleciona tipo de relatório
        select = Select(driver.find_element(By.NAME, "idRelatorio"))
        select.select_by_visible_text("Planilha de Contratos")

        time.sleep(10)


        # Clica em "Gerar Relatório"
        btn_gerar = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, "a.btn.btn-large.btn-primary.pull-right")
        HORAEXECUCAO = datetime.now()
        log_info(f"Momento da execução salvo: {HORAEXECUCAO}")
        btn_gerar.click()


        # Aguardar a conclusão da geração (pode-se aguardar um elemento de confirmação ou spinner desaparecer)
        # Aqui, apenas espera um tempo fixo, mas o ideal é aguardar um elemento.
        time.sleep(10)

        log_info("Relatório solicitado com sucesso")
        return HORAEXECUCAO
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar relatório: {e}")


def baixar_relatorio(driver, momento_execucao):
    try:
        log_info("Acessando página de processos para download do relatório")
        driver.refresh()
        time.sleep(1200)
        driver.get(URL_PROCESSOS)
        driver.refresh()
        # Loop até encontrar o relatório. Atenção: isso pode gerar loop infinito se o relatório nunca aparecer.
        # Uma prática melhor seria ter um timeout total de tentativas.
        tentativas = 0
        max_tentativas = 5  # Por exemplo, esperar 20 tentativas x 30 seg = 10 minutos
        usuario_alvo = "CARLOS JEFERSON"

        while tentativas < max_tentativas:
            driver.refresh()
            time.sleep(30)  # Aguarda 30s entre tentativas
            tentativas += 1
            log_info(f"Tentativa {tentativas}/{max_tentativas}")


            try:
                # Aguarda a presença da tabela após o refresh
                tabela = aguardar_elemento(driver, By.ID, "processoTable")
                linhas = tabela.find_elements(By.XPATH, ".//tbody/tr")

                for linha in linhas:
                    data_hora_str = linha.find_element(By.XPATH, ".//td[2]").text
                    usuario = linha.find_element(By.XPATH, ".//td[4]").text
                    data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")

                    # Verifica se o usuário e data/hora correspondem ao esperado
                    if usuario == usuario_alvo and data_hora > momento_execucao:
                        # Procura o botão de download na última coluna
                        log_info("Relatório encontrado.Tentando realizar o download")
                        botoes = linha.find_elements(By.XPATH, ".//td[last()]//a")
                        for botao in botoes:
                            link = botao.get_attribute("href")
                            time.sleep(10)
                            if "downloadArquivoRelatorio" in link:
                                botao.click()
                                log_info("download iniciado com sucesso")
                                time.sleep(500)
                                return
                            else:
                                log_info("Realtório ainda não foi processado")
            except Exception as e:
                # Caso algum erro ocorra na iteração, loga e tenta novamente
                log_erro(f"Erro durante a verificação do relatório: {e}")

        # Se sair do loop sem retornar, não encontrou o relatório
        raise RuntimeError("Não foi possível encontrar o relatório dentro do tempo limite.")
    except Exception as e:
        raise RuntimeError(f"Erro ao baixar relatório: {e}")

if __name__ == "__main__":
    iniciar_navegacao()
