from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils import log_acao
from src.captcha import CaptchaSolver
from datetime import datetime

class Navegador:
    def __init__(self):
        self.driver = None
        self.captcha_solver = CaptchaSolver()
        self.chrome_options = self._configurar_chrome_options()

    def _configurar_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "~/Downloads",
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        })
        return chrome_options

    def iniciar_navegacao(self, url):
        log_acao("Iniciando WebDriver")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(url)

    def realizar_login(self, usuario, senha):
        log_acao("Realizando login")
        self.driver.find_element(By.NAME, "login").send_keys(usuario)
        self.driver.find_element(By.NAME, "senha").send_keys(senha)
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-blue.btn-block").click()
        log_acao("Login realizado com sucesso")

    def salvar_momento_execucao(self):
        momento = datetime.now()
        log_acao(f"Momento da execução salvo: {momento}")
        return momento

    def gerar_relatorio(self, url, filtros, tipo_relatorio):
        log_acao("Gerando relatório")
        self.driver.get(url)
        for filtro in filtros:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, \"marcarTodos('{filtro}')\")]"))
            ).click()
        Select(self.driver.find_element(By.NAME, "idRelatorio")).select_by_visible_text(tipo_relatorio)
        self.driver.find_element(By.CSS_SELECTOR, "a.btn.btn-large.btn-primary.pull-right").click()
        log_acao("Relatório gerado com sucesso")

    def baixar_relatorio(self, url, momento_execucao, usuario):
        log_acao("Iniciando download do relatório")
        self.driver.get(url)
        while True:
            self.driver.refresh()
            tabela = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "processoTable")))
            for linha in tabela.find_elements(By.XPATH, ".//tbody/tr"):
                data_hora_str = linha.find_element(By.XPATH, ".//td[2]").text
                user = linha.find_element(By.XPATH, ".//td[4]").text
                if user == usuario and datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S") > momento_execucao:
                    botao = linha.find_element(By.XPATH, ".//td[last()]//a[contains(@href, 'downloadArquivoRelatorio')]")
                    botao.click()
                    log_acao("Relatório baixado com sucesso")
                    return

    def encerrar(self):
        if self.driver:
            self.driver.quit()
            log_acao("WebDriver encerrado")
