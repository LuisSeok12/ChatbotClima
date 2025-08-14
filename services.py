import os, httpx
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from collections import Counter

load_dotenv() 

async def get_weather(city: str | None = None, units: str = "metric", forecast: bool = False):
    """
    Busca clima ou previsão de amanhã por nome da cidade usando /data/2.5/weather.
    Retorna um dicionário padronizado.
    Campos `today_max`, `today_min`, `pop_today`, etc. podem estar `None`
    dependendo do tipo de consulta (clima atual ou previsão), mas são
    mantidos por consistência no formato do retorno.
    """
    api_key = (os.getenv("OPENWEATHER_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY ausente")

    if not city:
        raise ValueError("Informe a cidade.")

    async with httpx.AsyncClient(timeout=15) as client:

        if not forecast:
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
                #Campos de previsão (não disponíveis aqui)
                "tomorrow_max": None,
                "tomorrow_min": None,
                "pop_tomorrow": None,
                "weather_tomorrow": None,
            }
        else:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": api_key, "units": units, "lang": "pt_br"}
            r = await client.get(url, params=params)

            if r.status_code == 401:
                raise RuntimeError(f"OpenWeather 401 (forecast): {r.text}")
            if r.status_code == 404:
                raise ValueError("Cidade não encontrada.")
            r.raise_for_status()

            data = r.json()
            
            tz = timezone(timedelta(seconds=data.get("city", {}).get("timezone", 0)))
            now = datetime.now(tz=tz)
            tomorrow = (now + timedelta(days=1)).date()

            slots = []
            for item in data.get("list", []):
                dt = datetime.fromtimestamp(item.get("dt", 0), tz=tz)
                dt_local = dt.astimezone(tz)
                if dt_local.date() == tomorrow:
                    slots.append(item)
                
            if not slots:
                raise RuntimeError("Previsão para amanhã indisponível.")
                
            temps = [s.get("main", {}).get("temp") for s in slots if s.get("main", {})]
            temps = [t for t in temps if t is not None]
            temp_min = min(temps) if temps else None
            temp_max = max(temps) if temps else None

            pops = [s.get("pop", 0) for s in slots if s.get("pop") is not None]
            pop_max = max(pops) if pops else 0

            decs = []
            for s in slots:
                weather = (s.get("weather") or [{}])[0].get("description")
                if weather:
                    decs.append(weather)
            description = Counter(decs).most_common(1)[0][0] if decs else None

            return {
                "source": "forecast_3h",
                "city": data.get("city", {}).get("name"),
                "country": data.get("city", {}).get("country"),
                # no modo previsão não trazemos 'temperature' atual
                "temperature": None,
                "temp_min": None,
                "temp_max": None,
                "humidity": None,
                "weather": None,
                "wind_speed": None,
                # amanhã agregado
                "tomorrow_min": temp_min,
                "tomorrow_max": temp_max,
                "pop_tomorrow": pop_max,
                "weather_tomorrow": description,
                "today_max": None,
                "today_min": None,
                "pop_today": None,
            }


