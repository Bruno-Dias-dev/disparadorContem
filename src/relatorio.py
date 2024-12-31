import os, time
from src.utils.logs import log_info, log_erro
from src.utils.handle_element import acessar_pagina, aguardar_elemento_clicavel, aguardar_elemento
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import Select
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def gerar_relatorio(driver, uri):
    log_info("Gerando relatório")
    acessar_pagina(driver, uri)
    filtros = ["idConvenioArray", "convenio-cancelado", "idStatusContratoArray"]
    for filtro in filtros:
        link = aguardar_elemento_clicavel(driver, By.XPATH, f"//a[contains(@href, \"marcarTodos('{filtro}'\")]")
        link.click()
    select = Select(driver.find_element(By.NAME, "idRelatorio"))
    select.select_by_visible_text("Planilha de Contratos")
    btn_gerar = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, "a.btn.btn-large.btn-primary.pull-right")
    btn_gerar.click()

def gerar_relatorio_inadimplentes(driver, uri):
    log_info("Gerando relatório inadimplentes")
    acessar_pagina(driver, uri)
    filtros = ["idConvenioArray", "convenio-cancelado", "idStatusContratoArray"]
    for filtro in filtros:
        link = aguardar_elemento_clicavel(driver, By.XPATH, f"//a[contains(@href, \"marcarTodos('{filtro}'\")]")
        link.click()
    select = Select(driver.find_element(By.NAME, "idRelatorio"))
    select.select_by_visible_text("Planilha de Inadimplência")
    btn_gerar = aguardar_elemento_clicavel(driver, By.CSS_SELECTOR, "a.btn.btn-large.btn-primary.pull-right")
    HORAEXECUCAO = datetime.now()
    log_info(f"Momento da execução salvo: {HORAEXECUCAO}")
    btn_gerar.click()
    log_info("Relatório solicitado com sucesso")
    return HORAEXECUCAO

def baixar_relatorio(driver, uri, momento_execucao):
    log_info("Baixando relatório")
    driver.get(driver,uri)
    driver.refresh()
    tentativas = 0
    max_tentativas = 5  # Por exemplo, esperar 20 tentativas x 30 seg = 10 minutos
    usuario_alvo = "CARLOS JEFERSON"

    while tentativas < max_tentativas:
        driver.refresh()
        time.sleep(60)  # Aguarda 30s entre tentativas
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
                            time.sleep(280) # Varia de acordo com o tamanho do relatório
                            return
                        else:
                            log_info("Realtório ainda não foi processado")
        except Exception as e:
            # Caso algum erro ocorra na iteração, loga e tenta novamente
            log_erro(f"Erro durante a verificação do relatório: {e}")

    # Se sair do loop sem retornar, não encontrou o relatório
    raise RuntimeError("Não foi possível encontrar o relatório dentro do tempo limite.")