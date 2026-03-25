# Imagem oficial do Python como base
FROM python:3.12-slim

# Define variáveis de ambiente para o Python
# - PYTHONDONTWIRTEBITECODE: Impede que o Python gere arquivos .pyc no containner
# - PYTHONUNBUFFERED: Garante que o log do console seja exibido em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema necessárias para o Django e banco de dados
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o container
COPY . /app/
