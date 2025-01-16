import requests
import auth
from download_pdf import baixar_pdf, converter_para_base64

URI_MESSAGES = 'messages'

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
    'text': 'Olá, tudo bem? Teste de mensagem.',
    'contact_id': '755b1fad-2f53-417e-84d7-fd9b2b1e82fd',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d',
}
data_msg2 = {
    'text': 'Olá, tudo bem? Teste de mensagem.',
    'service_id': 'bdd9f0d1-747c-41f1-a81e-709dab41a423',
    'number': '5585997048236',
    'user_id': '6f4e2634-1fa5-47a3-b05c-c15a91e3d96d'
}


def enviar_mensagem_com_pdf(url_pdf, mensagem, numero):
    pdf_content = baixar_pdf(url_pdf)
    pdf_base64 = converter_para_base64(pdf_content)
    #Inadimplentes
    mensagem ="👋 Olá! Não identificamos em nossos registros o pagamento do seu plano de Assistência Médica e/ou odontológica. \n💭Lembramos que no 11o dia de atraso, a prestação do serviço junto à operadora será suspensa, bem como o cancelamento do contrato conforme cláusulas contratuais. \n📖 De acordo com o Art. 43, parágrafo 2º, da Lei n.º 8078/90, atrasos superiores a 10 (dez) dias resultarão no registro do seu débito no Serviço de Proteção ao Crédito - SPC. \n❌ Desconsiderar esta notificação caso o pagamento já tenha sido efetuado. \n🙏🏻 Desde já, colocamo-nos à disposição para eventuais dúvidas. Só nos chamar aqui 👇🏻"
    #Fase 4 e 5
    #mensagem ="👋 Olá, esperamos que você esteja bem! \n\n📱Estamos entrando em contato para informá-lo sobre a possibilidade de regularizar sua pendência financeira referente ao contrato cancelado. \n\nℹ️ Atualmente, estamos oferecendo uma condição especial, com descontos de até 50% para a quitação total do seu débito. \n\n⏳Essas condições são válidas por tempo limitado, e nossa equipe está à disposição para ajudar a resolver essa situação de maneira rápida e simples, retirando a restrição do CPF nos órgão de proteção ao Credito em 48 horas úteis. \n\n👇🏻Caso tenha interesse em aproveitar essa oportunidade ou precise de mais informações, por favor, estamos prontos para encontrar a melhor solução para você!"

    data_msg_pdf = {
        "text": mensagem,
        "number": numero,
        "departmentId": "919aa271-a6fa-43a7-8ec0-e9f81aab75e5",
        "serviceId": "bdd9f0d1-747c-41f1-a81e-709dab41a423",
        #"serviceId": "49ff100b-a917-48ca-b27d-5496c86ba655",
        #Parametro que garante a não abertura do chamado.
        "dontOpenTicket": "true",
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

