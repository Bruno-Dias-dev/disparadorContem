import requests
import base64

def baixar_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.content

def converter_para_base64(pdf_content):
    return base64.b64encode(pdf_content).decode('utf-8')
