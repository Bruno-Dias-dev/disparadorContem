from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Testar se a variável está carregada
print(os.getenv("ANTI_CAPTCHA_API_KEY"))