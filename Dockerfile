# Usa uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema (se precisar compilar libs Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de dependências primeiro (para aproveitar cache)
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar em produção (mais robusto que uvicorn puro)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.api:app", "--bind", "0.0.0.0:8000", "--workers", "4"]

# Alternativamente, se preferir usar uvicorn diretamente, descomente a linha abaixo e comente a linha acima
# CMD ["uvicorn", "main:app", "--host"#, "0.0.0.0", "--port", "8000"]
