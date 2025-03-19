import pandas as pd
import csv
import time
from src.api_module.mensagens import *

URI_MESSAGES = 'messages'
CONEXAO_GESTAO_SAUDE = '79d8bc4b-4db2-4320-bd6b-f40fd0b6ae60'
USER_ID = '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d'

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
            print(resultado)
            resultados.append([row['Código da Fatura'], numero, 'Falha', str(e)])
        
        time.sleep(1)

    # Escrever os resultados no arquivo CSV
    with open('resultados_envio.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Código da Fatura', 'Número', 'Status', 'Erro'])
        writer.writerows(resultados)

def envio_via_banco(faturas, pdf):
    resultados = []

    for fatura in faturas:
        url_pdf = 'https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo=' + str(fatura['código_da_fatura'])
        print(f"📢 Enviando mensagem para {fatura['celular']}")
        numero = formtatar_numero(fatura['celular'])
                   
        data_msg = {
            'text': 'Olá, tudo bem? Teste de mensagem.',
            'service_id': CONEXAO_GESTAO_SAUDE,
            'number': numero,
            'user_id': USER_ID
        }
        try:
            if pdf: 
                enviar_mensagem_com_pdf(url_pdf, data_msg['text'], data_msg['number'])
                resultado = f"Mensagem enviada, com PFD, para {numero} com código da fatura {str(fatura['código_da_fatura'])}"
                print(resultado)
                resultados.append([fatura['código_da_fatura'], numero, 'Sucesso', ''])
            else:    
                post_mensagem_sem_cadastro(data_msg)
                resultado = f"Mensagem enviada para {numero} com código da fatura {str(fatura['código_da_fatura'])}"
                print(resultado)
                resultados.append([fatura['código_da_fatura'], numero, 'Sucesso', ''])
        except Exception as e:
            resultado = f"Falha ao enviar mensagem para {numero} com código da fatura {str(fatura['código_da_fatura'])}: {e}"
            print(resultado)
            resultados.append([fatura['código_da_fatura'], numero, 'Falha', str(e)])
            continue
        
        time.sleep(1)
    # Escrever os resultados no arquivo CSV
    with open('resultados_envio_automacao.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Código da Fatura', 'Número', 'Status', 'Erro'])
        writer.writerows(resultados)
        
def formtatar_numero(numero):
    wpp = numero.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    return str('55') + wpp

# arquivo_xlsx = '../../docs/faturas.xlsx'
# processar_xlsx(arquivo_xlsx)