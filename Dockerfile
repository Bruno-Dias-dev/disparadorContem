# Usa a imagem oficial do Python 3.10
FROM python:3.10

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos necessários para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Comando para rodar o FastAPI usando Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "20.42.60.155", "--port", "8000", "--reload"]
