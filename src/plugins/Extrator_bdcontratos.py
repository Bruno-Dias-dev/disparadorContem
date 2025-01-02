import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from datetime import datetime

CHAVEAPI = "99517b6e7960ec66280cd743ba75166c"

# Função para logar ações realizadas pelo robô
def log_acao(mensagem):
    print(f"[LOG - {datetime.now()}]: {mensagem}")

def iniciar_navegacao():
    tentativa = 1
    max_tentativas = 1
    while tentativa <= max_tentativas:
        try:
            log_acao("Iniciando a navegação do robô")

            # Configurações do Chrome
            chrome_options = Options()
            prefs = {
                "download.default_directory": os.path.expanduser("~/Downloads"),
                "download.prompt_for_download": False,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            time.sleep(5)
            # Inicialização do WebDriver
            driver = webdriver.Chrome(options=chrome_options)
            log_acao("WebDriver inicializado com sucesso")
            time.sleep(5)
            driver.get("https://www.digitalsaude.com.br/login")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'g-recaptcha')))
            log_acao("Página de login acessada")
            time.sleep(5)
            # Quebra do CAPTCHA
            resolver_captcha(driver)
            time.sleep(5)
            # Realizar login
            realizar_login(driver)
            time.sleep(5)
            # Salvar o momento da execução
            momento_execucao = datetime.now()
            log_acao(f"Momento da execução salvo: {momento_execucao}")
            time.sleep(5)
            # Gerar relatório

    
            gerar_relatorio(driver)
        
            
            time.sleep(5)

        
            baixar_relatorio(driver, momento_execucao)
                 


            time.sleep(60)
            log_acao("Processo concluído com sucesso")
            break

        except Exception as e:
            log_acao(f"Erro na tentativa {tentativa}: {str(e)}")
            tentativa += 1
            if tentativa > max_tentativas:
                log_acao("Número máximo de tentativas atingido. Processo abortado.")

        finally:
            if 'driver' in locals():
                time.sleep(10)

                time.sleep(500)
                driver.quit()
                log_acao("WebDriver encerrado")

def resolver_captcha(driver):
    try:
        log_acao("Tentando resolver o CAPTCHA")
        chave_recaptcha = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(CHAVEAPI)
        solver.set_website_url(driver.current_url)
        solver.set_website_key(chave_recaptcha)
        resposta = solver.solve_and_return_solution()
        if not resposta:
            raise ValueError("Falha ao resolver o CAPTCHA.")
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{resposta}'")
        time.sleep(20)
        log_acao("CAPTCHA resolvido com sucesso")
    except Exception as e:
        raise RuntimeError(f"Erro ao resolver CAPTCHA: {e}")

def realizar_login(driver):
    try:
        log_acao("Realizando login no sistema")
        time.sleep(5)
        driver.find_element(By.NAME, "login").send_keys("CJEFERSON")
        time.sleep(5)
        driver.find_element(By.NAME, "senha").send_keys("hm6dxwx6")
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-blue.btn-block").click()
        log_acao("Login realizado com sucesso")
    except Exception as e:
        raise RuntimeError(f"Erro ao realizar login: {e}")

def gerar_relatorio(driver):
    try:
        log_acao("Acessando página para gerar relatório")
        driver.get("https://www.digitalsaude.com.br/operacional/relatorio/ExibirImprimirRelatorioContrato")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "idRelatorio"))
        )
        # Aplicar filtros
        filtros = [
            "idConvenioArray",
            "convenio-cancelado",
            "idStatusContratoArray"
        ]
        for filtro in filtros:
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, \"marcarTodos('{filtro}'\")]"))
            ).click()

        # Selecionar tipo de relatório
        time.sleep(2)
        select = Select(driver.find_element(By.NAME, "idRelatorio"))
        time.sleep(2)
        select.select_by_visible_text("Planilha de Contratos")
        time.sleep(2)
        # Gerar relatório
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-large.btn-primary.pull-right"))
        ).click()
        time.sleep(10)
        log_acao("Relatório gerado com sucesso")
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar relatório: {e}")

def baixar_relatorio(driver, momento_execucao):
    time.sleep(5)

    driver.get("https://www.digitalsaude.com.br/global/processo/ListarProcesso")
    
    time.sleep(5)

    # Verifica se o botão de download está disponível
    while True:  # Loop para verificar continuamente até encontrar o relatório
        print("Atualizando a página...")
        driver.refresh()
        time.sleep(30)  # Aguarda 30 segundos antes de continuar

        try:
            # Localiza a tabela novamente após a atualização
            tabela = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "processoTable")))
            linhas = tabela.find_elements(By.XPATH, ".//tbody/tr")

            encontrou_relatorio = False  # Flag para indicar se o relatório foi encontrado

            for linha in linhas:
                data_hora_str = linha.find_element(By.XPATH, ".//td[2]").text
                usuario = linha.find_element(By.XPATH, ".//td[4]").text

                # Converte a data e hora da linha para um objeto datetime
                data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")

                # Verifica se o usuário é "Carlos Jefferson" e se a data/hora é posterior ao momento da execução
                if usuario == "CARLOS JEFERSON" and data_hora > momento_execucao:
                    # Itera sobre os botões na última coluna
                    botoes = linha.find_elements(By.XPATH, ".//td[last()]//a")
                    for botao in botoes:
                        link = botao.get_attribute("href")
                        print(f"Link encontrado: {link}")
                        # Verifica se o link é para download
                        if "downloadArquivoRelatorio" in link:
                            botao.click()
                            print("Botão de download clicado!")
                            time.sleep(5)  # Espera um pouco antes de continuar para garantir que o download seja iniciado
                            encontrou_relatorio = True
                            break  # Sai do loop dos botões
                    if encontrou_relatorio:
                        break  # Sai do loop das linhas quando o relatório é encontrado

            if encontrou_relatorio:
                print("Relatório encontrado e baixado!")
                break  # Sai do loop principal quando o relatório é encontrado
        except Exception as e:
                        print(f"Erro durante a verificação: {e}")
if __name__ == "__main__":
    iniciar_navegacao()
