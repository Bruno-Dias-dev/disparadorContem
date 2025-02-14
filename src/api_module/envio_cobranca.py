import pandas as pd
import csv
import time
from mensagens import enviar_mensagem_com_pdf

def processar_xlsx(arquivo_xlsx):
    df = pd.read_excel(arquivo_xlsx)
    df = df.head(3)  # Pega apenas as 5 primeiras linhas

    resultados = []

    for index, row in df.iterrows():
        url_pdf = 'https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo=' + str(row['Código da Fatura'])
        mensagem = ""
        numero = formtatar_numero(row['Celular'])
        # numero=''
        try:
            enviar_mensagem_com_pdf(url_pdf, mensagem, numero)
            # enviar_mensagem_com_pdf(url_pdf, mensagem)
            resultado = f"Mensagem enviada para {numero} com código da fatura {str(row['Código da Fatura'])}"
            print(resultado)
            resultados.append([row['Código da Fatura'], numero, 'Sucesso', ''])
        except Exception as e:
            resultado = f"Falha ao enviar mensagem para {numero} com código da fatura {str(row['Código da Fatura'])}: {e}"
            print(resultado)
            resultados.append([row['Código da Fatura'], numero, 'Falha', str(e)])
        
        time.sleep(1)

    # Escrever os resultados no arquivo CSV
    with open('resultados_envio.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Código da Fatura', 'Número', 'Status', 'Erro'])
        writer.writerows(resultados)

def formtatar_numero(numero):
    wpp = numero.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    return str('55') + wpp

arquivo_xlsx = '../../docs/faturas.xlsx'
processar_xlsx(arquivo_xlsx)