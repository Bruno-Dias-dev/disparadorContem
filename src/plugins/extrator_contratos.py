from navegacao import Navegador
from utils import log_acao

class ExtratorContratos(Navegador):
    def __init__(self):
        super().__init__()  # Inicializa o Navegador.

    def executar(self):
        try:
            log_acao("Iniciando extração de contratos")
            self.iniciar_navegacao("https://www.digitalsaude.com.br/login")

            # Resolver CAPTCHA e realizar login
            self.captcha_solver.resolver_captcha(self.driver)
            self.realizar_login("CJEFERSON", "hm6dxwx6")

            # Gerar relatório e baixar
            momento_execucao = self.salvar_momento_execucao()
            self.gerar_relatorio(
                "https://www.digitalsaude.com.br/operacional/relatorio/ExibirImprimirRelatorioContrato",
                filtros=[
                    "idConvenioArray",
                    "convenio-cancelado",
                    "idStatusContratoArray"
                ],
                tipo_relatorio="Planilha de Contratos"
            )
            self.baixar_relatorio(
                "https://www.digitalsaude.com.br/global/processo/ListarProcesso",
                momento_execucao,
                usuario="CARLOS JEFERSON"
            )
        except Exception as e:
            log_acao(f"Erro na extração de contratos: {e}")
        finally:
            self.encerrar()

if __name__ == "__main__":
    extrator = ExtratorContratos()
    extrator.executar()
