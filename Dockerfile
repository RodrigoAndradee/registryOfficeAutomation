FROM python:3.10-slim

ENV TZ=America/Sao_Paulo
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema e playwright
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia só os arquivos essenciais primeiro (para manter cache do Docker)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Instala dependências do Playwright e os navegadores
RUN pip install --no-cache-dir playwright && \
    playwright install-deps && \
    playwright install

# Só agora copia o resto do projeto (para não invalidar cache desnecessariamente)
COPY . .
