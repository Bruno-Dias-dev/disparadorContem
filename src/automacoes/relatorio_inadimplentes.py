import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from src.login import realizar_login
from src.relatorio import gerar_relatorio, baixar_relatorio
from src.utils.logs import log_info, log_erro
from src.config import iniciar_navegacao

# Carregar variáveis do arquivo .env
load_dotenv()


URL_RELATORIO = "/financeiro/relatorio/ExibirImprimirRelatorioInadimplente"
URL_PROCESSOS = "/global/processo/ListarProcesso"

if __name__ == "__main__":
    try:
        driver, momento_execucao = iniciar_navegacao(os.getenv("BASE_URL"))
        realizar_login(driver, os.getenv("SISTEMA_LOGIN"), os.getenv("SISTEMA_SENHA"))
        gerar_relatorio(driver, os.getenv("BASE_URL")+URL_RELATORIO)
        baixar_relatorio(driver, os.getenv("BASE_URL")+URL_PROCESSOS,momento_execucao)
        log_info("Processo concluído com sucesso")
    except Exception as e:
        log_erro(f"Erro durante a execução: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            log_info("WebDriver encerrado") 
