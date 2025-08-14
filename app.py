import os, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# carregue .env antes de importar qualquer coisa que use as variáveis
load_dotenv()

from openai import OpenAI
from services import get_weather  

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Weather Chatbot API")

class ChatRequest(BaseModel):
    message: str
    city: str | None = None
    units: str = "metric"   # 'metric' (°C) ou 'imperial' (°F)

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Obtém o clima atual (e resumo do dia, se disponível) para uma cidade.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade. Ex.: 'São Paulo', 'Rio de Janeiro'."
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "default": "metric",
                    "description": "metric=Celsius, imperial=Fahrenheit."
                }
            },
            "additionalProperties": False
        }
    }
}]

SYSTEM_PROMPT = (
    "Você é um assistente meteorológico educado. "
    "Quando o usuário pedir informações de clima ou previsão, chame a ferramenta get_weather. "
    "Se o usuário não informar a cidade, peça o nome da cidade. "
    "Explique resultados com °C quando 'units=metric' e em °F quando 'units=imperial'."
)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "up"}

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.message},
    ]

    try:
        first = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na OpenAI (1ª chamada): {e}")

    msg = first.choices[0].message
    tool_calls = msg.tool_calls or []

    if tool_calls:
        tool_msgs = []
        for call in tool_calls:
            if call.function.name != "get_weather":
                continue

            args = json.loads(call.function.arguments or "{}")

            if request.city:
                args.setdefault("city", request.city)
            args.setdefault("units", request.units)

            if not args.get("city"):
                raise HTTPException(status_code=400, detail="Informe a cidade.")

            try:
                data = await get_weather(**args)
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"Erro ao consultar clima: {e}")

            tool_msgs.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": "get_weather",
                "content": json.dumps(data, ensure_ascii=False)
            })

        try:
            second = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages + [msg] + tool_msgs,
                temperature=0.3,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na OpenAI (2ª chamada): {e}")

        return {"reply": second.choices[0].message.content}

    # Sem tool-call: retorna o texto do modelo (provavelmente pedindo a cidade)
    return {"reply": msg.content}
