# 🌦️ Chatbot Clima

Um chatbot em **Python (FastAPI)** que usa **OpenAI** para entender perguntas em linguagem natural e **OpenWeather** para buscar o clima por **nome da cidade**.

---

## ✨ Funcionalidades
- Conversa em linguagem natural (OpenAI)
- Clima **atual** por cidade (`/data/2.5/weather`)
- Unidades: **metric (°C)** e **imperial (°F)**
- Documentação automática via **Swagger UI** (`/docs`)

---

## 🧱 Stack
- Python 3.10+
- FastAPI
- Uvicorn
- httpx
- python-dotenv
- OpenAI Python SDK

---

## 📁 Estrutura
.
├─ app.py
├─ services.py
├─ requirements.txt
├─ .env.example
└─ .gitignore
