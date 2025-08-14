import os, httpx
from dotenv import load_dotenv

load_dotenv()  # garante que .env foi carregado mesmo se importarem cedo

async def get_weather(city: str | None = None, units: str = "metric"):
    """
    Busca clima atual por nome da cidade usando /data/2.5/weather.
    Retorna um dicionário padronizado.
    """
    api_key = (os.getenv("OPENWEATHER_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY ausente")

    if not city:
        raise ValueError("Informe a cidade.")

    async with httpx.AsyncClient(timeout=15) as client:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": units, "lang": "pt_br"}
        r = await client.get(url, params=params)

        if r.status_code == 401:
            raise RuntimeError(f"OpenWeather 401 (weather): {r.text}")
        if r.status_code == 404:
            raise ValueError("Cidade não encontrada.")
        r.raise_for_status()

        data = r.json()
        return {
            "source": "current",
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "temp_min": data.get("main", {}).get("temp_min"),
            "temp_max": data.get("main", {}).get("temp_max"),
            "humidity": data.get("main", {}).get("humidity"),
            "weather": (data.get("weather") or [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "today_max": None,
            "today_min": None,
            "pop_today": None,
        }
