# 🌦️ Chatbot Clima

Um chatbot em **Python (FastAPI)** que usa **OpenAI** para entender perguntas em linguagem natural e **OpenWeather** para buscar o clima por **nome da cidade**.

---

## Funcionalidades

* Conversa em linguagem natural (OpenAI)
* Clima **atual** por cidade (`/data/2.5/weather`)
* Unidades: **metric (°C)** e **imperial (°F)**
* Documentação automática via **Swagger UI** (`/docs`)

---

## Stack

* Python 3.10+
* FastAPI
* Uvicorn
* httpx
* python-dotenv
* OpenAI Python SDK

---

## Estrutura

```
.
├─ app.py
├─ services.py
├─ requirements.txt
├─ .env.example
└─ .gitignore
```

---

## Variáveis de ambiente

Crie um arquivo **`.env`** na raiz com:

```
OPENAI_API_KEY=coloque_sua_key_openai_aqui
OPENWEATHER_API_KEY=coloque_sua_key_openweather_aqui
```

Arquivo de exemplo incluído: **`.env.example`**

```
OPENAI_API_KEY=your_openai_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

> **Importante:** não faça commit do `.env`. O repositório já contém `.gitignore` com:

```
__pycache__/
.env
*.pyc
```

---

## Como rodar

### 1) Clonar o repositório

```bash
git clone https://github.com/LuisSeok12/ChatbotClima.git
cd ChatbotClima
```

### 2) Criar e ativar o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Configurar o `.env`

```bash
# Linux/Mac
cp .env.example .env
# Windows (PowerShell)
copy .env.example .env
```

Edite o `.env` e coloque suas chaves.

### 5) Subir o servidor

```bash
uvicorn app:app --reload
# Se o comando 'uvicorn' não for reconhecido:
python -m uvicorn app:app --reload
```

Acesse:

* Swagger UI: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
* Healthcheck: **[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)**

---

## Exemplo de uso

### Swagger UI

1. Abra `http://127.0.0.1:8000/docs`
2. Selecione `POST /chat` → **Try it out** → Body:

```json
{
  "message": "Como está o tempo no Rio de Janeiro?",
  "units": "metric",
  "city": "Rio de Janeiro"
}
```

### cURL

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Como está o tempo em Recife agora?","units":"metric","city":"Recife"}'
```

### PowerShell

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method POST -ContentType "application/json" -Body '{
  "message":"Qual a temperatura em Belo Horizonte?",
  "units":"metric",
  "city":"Belo Horizonte"
}'
```

---

## Troubleshooting

* **`uvicorn: command not found`**
  Use `python -m uvicorn app:app --reload` ou ative o venv.
* **HTTP 401 (OpenWeather)**
  Chave inválida/expirada ou espaço extra no `.env`. Gere uma nova chave e verifique o arquivo.
* **ImportError FastAPI**
  Use `from fastapi import FastAPI` (F maiúsculo, restante minúsculo).

---
