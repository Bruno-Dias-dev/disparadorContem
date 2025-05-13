import requests
import auth

URI_CONTATOS = 'contacts'
def get_contatos(page=1, qtd=50):
    token = auth.get_access_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'page': page,
        'per_page': qtd
    }
    url = auth.url+URI_CONTATOS
    request = requests.get(url, headers=headers, params=params)
    return request.json()

