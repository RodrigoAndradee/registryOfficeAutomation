FROM python:3.10-slim

ENV TZ=America/Sao_Paulo
RUN apt-get update && apt-get install -y tzdata

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN playwright install-deps && playwright install
