import requests
import auth
from download_pdf import baixar_pdf, converter_para_base64

URI_MESSAGES = 'messages'
CONEXAO_GESTAO_SAUDE = '79d8bc4b-4db2-4320-bd6b-f40fd0b6ae60'

#Listagem de mensagens
def get_mensagens(page=1, qtd=50):
    token = auth.get_access_token()
    try:
        headers = { 
            'Authorization': f'Bearer {token}'
        }
        params = {
            'page': page,
            'per_page': qtd
        }
        url = auth.url+URI_MESSAGES
        request = requests.get(url, headers=headers, params=params)
        return request.json()
    except Exception as e:
        return {'error': str(e)}

#Envio de msg p/ contato cadastrado
def post_mensagem(data):
    token = auth.get_access_token()
   
    data = {
        "text": data['text'], # Mensagem a ser enviada
        "type": "chat",
        "contactId": data['contact_id'], # ID do serviço
        "userId": data['user_id'], # ID do usuário
        "origin": "bot" #bot ou user
    }
    try:
        headers = { 
            'Authorization': f'Bearer {token}'
        }
        url = auth.url+URI_MESSAGES
        request = requests.post(url, headers=headers, json=data)
        return request.json()
    except Exception as e:
        return {'error': str(e)}

#Envio de msg p/ contato não cadastrado    
def post_mensagem_sem_cadastro(data):
    token = auth.get_access_token()
    data = {
        "text": data['text'], # Mensagem a ser enviada
        "type": "chat",
        "serviceId": data['service_id'], #  ID conexão
        "number": data['number'], # Número do contato(55DDD+numero)
        "userId": data['user_id'], # ID do usuário
        "origin": "bot" #bot ou user
    }
    try:
        headers = { 
            'Authorization': f'Bearer {token}'
        }
        url = auth.url+URI_MESSAGES
        request = requests.post(url, headers=headers, json=data)
        return request.json()
    except Exception as e:
        return {'error': str(e)}

data_msg1 = {    
    'text': 'Olá, tudo bem? Teste de mensagem.',
    'contact_id': '755b1fad-2f53-417e-84d7-fd9b2b1e82fd',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d',
}
data_msg2 = {
    'text': 'Olá, tudo bem? Teste de mensagem.',
    'service_id': CONEXAO_GESTAO_SAUDE,
    'number': '5585997048236',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d'
}


def enviar_mensagem_com_pdf(url_pdf, mensagem, numero):
    pdf_content = baixar_pdf(url_pdf)
    pdf_base64 = converter_para_base64(pdf_content)
    mensagem ="👋 Olá! Não identificamos em nossos registros o pagamento do seu plano de Assistência Médica e/ou odontológica. \n💭Lembramos que no 11o dia de atraso, a prestação do serviço junto à operadora será suspensa, bem como o cancelamento do contrato conforme cláusulas contratuais. \n📖 De acordo com o Art. 43, parágrafo 2º, da Lei n.º 8078/90, atrasos superiores a 10 (dez) dias resultarão no registro do seu débito no Serviço de Proteção ao Crédito - SPC. \n❌ Desconsiderar esta notificação caso o pagamento já tenha sido efetuado. \n🙏🏻 Desde já, colocamo-nos à disposição para eventuais dúvidas. Só nos chamar aqui 👇🏻"

    data_msg_pdf = {
        "text": mensagem,
        "number": numero,
        "serviceId": CONEXAO_GESTAO_SAUDE,
        "file": {
            "base64": pdf_base64,
            "mimetype": "application/pdf",
            "name": "fatura.pdf"
        }
    }   
        
    token = auth.get_access_token()
    try:
        headers = { 
            'Authorization': f'Bearer {token}'
        }
        url = auth.url+URI_MESSAGES
        request = requests.post(url, headers=headers, json=data_msg_pdf)
        return request.json()
    except Exception as e:
        return {'error': str(e)}

