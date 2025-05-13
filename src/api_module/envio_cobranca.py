import pandas as pd
import csv
import time
from src.api_module.mensagens import *
from datetime import datetime

def processar_xlsx(arquivo_xlsx):
    df = pd.read_excel(arquivo_xlsx)
    df = df.head(3)  # Pega apenas as 5 primeiras linhas

    resultados = []

    for index, row in df.iterrows():
        url_pdf = 'https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo=' + str(row['Código da Fatura'])
        mensagem = ""
        numero = formtatar_numero(row['Celular'])
        try:
            enviar_mensagem_com_pdf(url_pdf, mensagem, numero)
            resultado = f"Mensagem enviada para {numero} com código da fatura {str(row['Código da Fatura'])}"
            resultados.append([row['Código da Fatura'], numero, 'Sucesso', ''])
        except Exception as e:
            resultado = f"Falha ao enviar mensagem para {numero} com código da fatura {str(row['Código da Fatura'])}: {e}"
            resultados.append([row['Código da Fatura'], numero, 'Falha', str(e)])
        
        time.sleep(1)

    # Escrever os resultados no arquivo CSV
    with open('resultados_envio.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Código da Fatura', 'Número', 'Status', 'Erro'])
        writer.writerows(resultados)
        
def envio_log(data_msg):
    numero = formtatar_numero(data_msg['celular'])
    data_msg['number'] = numero

    post_mensagem_sem_cadastro(data_msg)


def envio_via_banco(data_msg, fatura, pdf):
    resultados = []

    url_pdf = 'https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo=' + str(fatura['codigo_da_fatura']) 
    numero = formtatar_numero(fatura['celular'])
    data_msg['url_pdf'] = url_pdf
    data_msg['number'] = numero
    try:
        if pdf: 
            enviar_mensagem_com_pdf(data_msg)
            resultado = f"Mensagem enviada, com PDF, para {numero} com código da fatura {str(fatura['codigo_da_fatura'])}"
            resultados.append([fatura['codigo_da_fatura'], numero, 'Sucesso', ''])
        else:    
            post_mensagem_sem_cadastro(data_msg)
            resultado = f"Mensagem enviada para {numero} com código da fatura {str(fatura['codigo_da_fatura'])}"
            resultados.append([fatura['codigo_da_fatura'], numero, 'Sucesso', ''])
    except Exception as e:
        resultado = f"Falha ao enviar mensagem para {numero} com código da fatura {str(fatura['codigo_da_fatura'])}: {e}"
        resultados.append([fatura['codigo_da_fatura'], numero, 'Falha', str(e)])
    
    # Escrever os resultados no arquivo CSV
    data_hoje = datetime.now().strftime('%Y-%m-%d')  
    nome_arquivo = f'{data_hoje}_resultados_envio_automacao.csv'
    
    with open(nome_arquivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Código da Fatura', 'Número', 'Status', 'Erro'])
        writer.writerows(resultados)
        
def formtatar_numero(numero):
    wpp = numero.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    return str('55') + wpp

# arquivo_xlsx = '../../docs/faturas.xlsx'
# processar_xlsx(arquivo_xlsx)