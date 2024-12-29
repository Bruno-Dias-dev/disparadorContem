import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração de login
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
def iniciar_navegacao():
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
        data_vencimento = "25/12/2024"
        filtro = planilha[(planilha['Data de Vencimento'] == data_vencimento) &
                          (~planilha['Alerta'].str.contains('NÃO COBRAR', na=False)) &
                          (planilha['Data do Pagamento'].isnull())]

        # Criar relatório de status
        relatorio = []

        for _, cliente in filtro.iterrows():
            nome_cliente = cliente['Nome Titular']
            codigo_fatura = cliente['Código da Fatura']
            log_info(f"Processando cliente: {nome_cliente}")
            try:
                Pesquisar_nome(driver, nome_cliente, codigo_fatura)
                status = 'Sucesso'
            except Exception as e:
                status = f'Erro: {str(e)}'

            relatorio.append({
                'Nome do Cliente': nome_cliente,
                'Código da Fatura': codigo_fatura,
                'Status': status
            })
            driver.refresh()

        # Salvar relatório em planilha
        relatorio_df = pd.DataFrame(relatorio)
        relatorio_df.to_excel('relatorio_envio.xlsx', index=False)
        log_info("Relatório gerado com sucesso")

        log_info("Processo concluído com sucesso")
    except Exception as e:
        log_erro(f"Erro durante o processo: {str(e)}")
    finally:
        time.sleep(5)
        if 'driver' in locals():
            driver.quit()
            log_info("WebDriver encerrado")

# Funções para aguardar elementos
def aguardar_elemento(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def aguardar_elemento_clicavel(driver, by, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))

# Função para login
def Preencher_login(driver):
    try:
        log_info("Preenchendo o login")
        user_field = aguardar_elemento(driver, By.ID, "username")
        user_field.send_keys(LOGIN_USUARIO)
        time.sleep(2)

        pass_field = aguardar_elemento(driver, By.ID, "password")
        pass_field.send_keys(LOGIN_SENHA)
        time.sleep(2)

        login_button = aguardar_elemento(driver, By.CSS_SELECTOR, "button[data-testid='login-button-login']")
        login_button.click()
        log_info("Login realizado com sucesso")

    except Exception as e:
        log_erro(f"Erro ao realizar login: {e}")                        

# Função para pesquisar um nome
def Pesquisar_nome(driver, nome,codigo_fatura):
    try:
        log_info("Pesquisando por nome")
        search_field = aguardar_elemento(driver, By.CSS_SELECTOR, "input[data-testid='chat-input-search_by_name_or_number']")
        search_field.send_keys(nome)
        time.sleep(1)

        start_conversation_button = aguardar_elemento(driver, By.CSS_SELECTOR, "div[data-testid='chat-tab-start_conversation']")
        start_conversation_button.click()
        time.sleep(1)

        # Seleciona o primeiro contato na lista de resultados
        first_contact = aguardar_elemento(driver, By.CSS_SELECTOR, ".ReactVirtualized__Grid__innerScrollContainer > div:first-child")
        first_contact.click()
        log_info("Contato Selecionado")
        time.sleep(2)
        link_fatura = f"https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo={codigo_fatura}"
        #mensagem = f"\ud83d\udc4b Olá! O boleto do seu plano de saúde e/ou odontológico VENCERÁ NO DIA 25/12/2024.\n\n\ud83e\udd14 Não se esqueça de efetuar o pagamento, para garantia da prestação de serviço.\n\n❓Qualquer dúvida, podemos te dar o suporte aqui 👇🏻\n\nSegue link da fatura: {link_fatura}"
            

        # Verifica se o botão de abrir o chamado está presente. Caso ele esteja:
        if verificar_botao_abrir_chamado(driver):

            log_info("Botão encontrado encontrado")
            #Clicar no botão para abrir o chamado
            abrir_chamado(driver)
            #Selecionar departamento e agente. Após isso, salvar;
            selecionar_opcoes_e_salvar(driver)
            time.sleep(2)
            #Mandar mensagem rápidas
            clicar_mensagens_rapidas(driver)
            #Enviar link da fatura
            inserir_link(driver, link_fatura)
        elif verificar_campo_texto(driver):
            time.sleep(2)
            log_info("Chamado já está aberto")
            clicar_mensagens_rapidas(driver)
            inserir_link(driver, link_fatura)
        else:
            log_info("NÃO DEU BOM")

    except Exception as e:
        log_erro(f"Erro ao pesquisar nome: {e}")

# Função para verificar se o botão de abrir chamado está disponível
def verificar_botao_abrir_chamado(driver):
    try:
        # Usa a mesma lógica de aguardar elemento clicável
        aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, "button[data-testid='open-ticket-button']", timeout=5)
        log_info("Chamado já foi aberto")
        return True
    except:
        log_info("Cliente desatualizado")
        return False

# Função para abrir chamado
def abrir_chamado(driver):
    try:
        log_info("Abrindo chamado...")
        botao_abrir = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, "button[data-testid='open-ticket-button']")
        botao_abrir.click()
        time.sleep(2)
        log_info("Chamado aberto com sucesso.")
    except Exception as e:
        log_erro(f"Erro ao abrir chamado: {e}")


def verificar_campo_texto(driver):
    try:
        # Usa a mesma lógica de aguardar elemento clicável
        aguardar_elemento(driver, By.CSS_SELECTOR, "textarea.reply-text-area")
        log_info("Campo texto disponível")
        return True
    except:
        log_info("Cliente precisa atualizar")
        return False


# Função para selecionar opções e salvar
def selecionar_opcoes_e_salvar(driver):
    try:
        log_info("Selecionando opções e salvando...")

        campo_departamento = aguardar_elemento_clicavel(driver, By.ID, "react-select-department-input")
        campo_departamento.send_keys("Cobrança Ativo")
        time.sleep(1)
        campo_departamento.send_keys("\ue007")

        campo_usuario = aguardar_elemento_clicavel(driver, By.ID, "react-select-user-input")
        campo_usuario.send_keys("Jeane Jordão")
        time.sleep(1)
        campo_usuario.send_keys("\ue007")

        salvar_button = aguardar_elemento(driver, By.CSS_SELECTOR, "button[data-testid='confirm-transfer-ticket-button']")
        salvar_button.click()
        log_info("Opções salvas com sucesso.")

    except Exception as e:
        log_erro(f"Erro ao selecionar opções e salvar: {e}")

# Função para clicar em mensagens rápidas
def clicar_mensagens_rapidas(driver):
    try:
        log_info("Clicando em mensagens rápidas...")
        quick_reply_button = aguardar_elemento_clicavel(driver, By.ID, "quick-reply-popover")
        quick_reply_button.click()
        time.sleep(2)

        aviso_button = aguardar_elemento_clicavel(driver, By.ID, "6")
        aviso_button.click()
        log_info("Mensagem rápida selecionada com sucesso.")

    except Exception as e:
        log_erro(f"Erro ao clicar em mensagens rápidas: {e}")

# Função para inserir texto na mensagem

def inserir_link(driver, link):
    try:
        log_info("Inserindo link na mensagem...")
        text_area = aguardar_elemento(driver, By.CSS_SELECTOR, "textarea.reply-text-area")
        text_area.send_keys(link)
        text_area.send_keys("\ue007")
        time.sleep(2)
        log_info("Link inserido e enviado com sucesso.")

    except Exception as e:
        log_erro(f"Erro ao inserir link na mensagem: {e}")



if __name__ == "__main__":
    iniciar_navegacao()
