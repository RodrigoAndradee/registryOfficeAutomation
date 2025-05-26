# Django Automation Dashboard

Este projeto é um painel web para importar, armazenar, filtrar e processar dados de automações com Django, Celery, Playwright e Docker.

## ✨ Funcionalidades

- Upload de arquivos `.json` com dados de automações
- Armazenamento dos dados no banco via Django ORM
- Execução assíncrona das automações com Celery
- Interface de filtro por status e data
- Uso de Playwright para automação web
- Frontend com Bootstrap 5 e Flatpickr
- Container Docker com execução automática de migrations

## 🛠 Tecnologias

- Python 3.11+
- Django 4+
- Celery + Redis
- Playwright
- Bootstrap 5
- Flatpickr (datepicker)
- Docker + docker-compose
- PostgreSQL

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/RodrigoAndradee/registryOfficeAutomation.git
cd seu-repo
```

### 2. Crie o .env

- Crie o arquivo .env
- Adicione as variáveis necessárias (siga o .env.example)

### 3. Rode os containers

```bash
docker compose up -d --build
```

### 4. Acesse o site

```bash
http://localhost:8000/
```

### 5. Upload de JSON

- O JSON deve seguir o seguinte formato:

```bash
{
    "automation_data": [
        {
            "code": str
            "quantity": str
            "type": str
        }
    ]
}
```
