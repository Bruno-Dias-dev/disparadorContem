# Baseado na imagem oficial do Apache Airflow
FROM apache/airflow:2.10.3

# Usuário root para instalar dependências do sistema
USER root

# Atualiza os pacotes e instala Chromium, seu driver, e configura o timezone
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    tzdata && \
    ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Alterna para o usuário airflow e define o diretório de trabalho
USER airflow
WORKDIR /opt/airflow

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Atualiza o pip e instala as dependências Python listadas no requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt
