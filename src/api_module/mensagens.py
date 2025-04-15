import requests
from typing import Dict, Any

# from src.api_module import auth
# from src.api_module.download_pdf import baixar_pdf, converter_para_base64
import auth
from download_pdf import baixar_pdf, converter_para_base64

URI_MESSAGES = 'messages'
URI_SERVICES = 'services'
URI_DEPARTMENTS = 'departments'

def get_headers() -> Dict[str, str]:
    token = auth.get_access_token()
    return {'Authorization': f'Bearer {token}'}


def get_url(uri: str) -> str:
    return f"{auth.url}{uri}"


def tratar_erro(e: Exception) -> Dict[str, str]:
    return {'error': str(e)}


def get_mensagens(page: int = 1, qtd: int = 50) -> Dict[str, Any]:
    try:
        response = requests.get(
            get_url(URI_MESSAGES),
            headers=get_headers(),
            params={'page': page, 'per_page': qtd}
        )
        return response.json()
    except Exception as e:
        return tratar_erro(e)

def post_mensagem(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Envia mensagem para um contato já cadastrado.
    """
    payload = {
        "text": data['text'],
        "type": "chat",
        "contactId": data['contact_id'],
        "userId": data['user_id'],
        "origin": "bot"
    }

    try:
        response = requests.post(get_url(URI_MESSAGES), headers=get_headers(), json=payload)
        return response.json()
    except Exception as e:
        return tratar_erro(e)

def post_mensagem_sem_cadastro(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Envia mensagem para número ainda não cadastrado como contato.
    """
    payload = {
        "text": data['text'],
        "type": "chat",
        "serviceId": data['service_id'],
        "number": data['number'],
        "origin": "user" # ou "bot"
    }

    try:
        response = requests.post(get_url(URI_MESSAGES), headers=get_headers(), json=payload)
        return response.json()
    except Exception as e:
        return tratar_erro(e)

def enviar_mensagem_com_pdf(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Envia uma mensagem com um PDF anexado via WhatsApp.

    Parâmetros esperados em `data`:
        - url_pdf: URL do PDF.
        - text: Texto da mensagem.
        - number: Número com DDI (ex: 558599999999).
        - departmentId: ID do departamento.
        - serviceId: ID do serviço.
    """
    try:
        pdf_content = baixar_pdf(data['url_pdf'])
        pdf_base64 = converter_para_base64(pdf_content)
        
        payload = {
            "text": data['text'],
            "number": data['number'],
            "departmentId": data['departmentId'],
            "serviceId": data['serviceId'],
            "dontOpenTicket": "true",
            "file": {
                "base64": pdf_base64,
                "mimetype": "application/pdf",
                "name": "fatura.pdf"
            }
        }

        response = requests.post(get_url(URI_MESSAGES), headers=get_headers(), json=payload)
        return response.json()
    except Exception as e:
        return tratar_erro(e)

def get_conexoes_ativas():
    """
    Obtém todas as conexões ativas e conectadas.
    """
    try:
        page = 1
        per_page = 50
        todas_conexoes = []

        while True:
            url = get_url(f"{URI_SERVICES}?page={page}&perPage={per_page}")
            response = requests.get(url, headers=get_headers())
            data = response.json()
            conexoes = data.get("data", [])

            # Se não veio mais nada, fim da paginação
            if not conexoes:
                break

            todas_conexoes.extend(conexoes)
            page += 1

        # Filtra conexões ativas e conectadas
        conexoes_ativas = [
            item for item in todas_conexoes
            if item.get("archivedAt") is None
            and item.get("deletedAt") is None
            and item.get("data", {}).get("status", {}).get("isConnected") is True
        ]

        return conexoes_ativas

    except Exception as e:
        return tratar_erro(e)


    except Exception as e:
        return tratar_erro(e)

def get_departamentos():
    """
    Obtém os departamentos disponíveis.
    """
    try:
        response = requests.get(get_url(URI_DEPARTMENTS), headers=get_headers())
        data = response.json()
        departamentos = data.get("data", [])
        
        departamentos_ativos = [
            dept for dept in departamentos
            if dept.get("archivedAt") is None or dept.get("archivedAt") is False
        ]

        return departamentos_ativos
    except Exception as e:
        return tratar_erro(e)

