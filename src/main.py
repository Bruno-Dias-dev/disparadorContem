import os
from dotenv import load_dotenv
from login import realizar_login
from relatorio import gerar_relatorio, baixar_relatorio
from utils.logs import log_info, log_erro
from config import iniciar_navegacao
from dotenv import load_dotenv

load_dotenv()
RELATORIO_CONTRATO = "/operacional/relatorio/ExibirImprimirRelatorioContrato"
LISTAR_PROCESSO = "/global/processo/ListarProcesso"


if __name__ == "__main__":
    try:
        driver, momento_execucao = iniciar_navegacao(os.getenv("BASE_URL"))
        realizar_login(driver, os.getenv("SISTEMA_LOGIN"), os.getenv("SISTEMA_SENHA"))
        gerar_relatorio(driver,RELATORIO_CONTRATO)
        baixar_relatorio(driver, LISTAR_PROCESSO)
        log_info("Processo concluído com sucesso")
    except Exception as e:
        log_erro(f"Erro durante a execução: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            log_info("WebDriver encerrado")
