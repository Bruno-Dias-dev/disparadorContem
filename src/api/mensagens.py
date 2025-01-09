import requests
import auth

URI_MESSAGES = 'messages'

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

def post_mensagem(data):
    token = auth.get_access_token()
   
    data = {
        "text": data['text'], # Mensagem a ser enviada
        "type": "chat",
        "contactId": data['contact_id'], # ID do serviço
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
    
def post_mensagem_sem_cadastro(data):
    token = auth.get_access_token()
    data = {
        "text": data['text'], # Mensagem a ser enviada
        "type": "chat",
        "serviceId": data['service_id'], # ID do serviço
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
    'text': 'Olá, tudo bem?',
    'contact_id': '755b1fad-2f53-417e-84d7-fd9b2b1e82fdd',
    'number': '5585997048236',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d'
}
data_msg2 = {
    'text': 'Olá, tudo bem?',
    'service_id': 'bdd9f0d1-747c-41f1-a81e-709dab41a423',
    'number': '5585997048236',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d'
}

#contato_id = '755b1fad-2f53-417e-84d7-fd9b2b1e82fdd'
#Fatura = https://digitalsaude.com.br/financeiro/fatura/ImprimirFatura?codigo=3AAJ6RJKGW
print(post_mensagem(data=data_msg1))
# print(post_mensagem_sem_cadastro(data=data_msg2))