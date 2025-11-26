# src/weather_node.py
import requests
from config import settings

BASE = "https://api.openweathermap.org/data/2.5/weather"

class WeatherError(Exception):
    pass

def fetch_weather_by_city(city: str, units: str = "metric"):
    if not settings.OPENWEATHER_API_KEY:
        raise WeatherError("OpenWeather API key not set in .env")
    params = {"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": units}
    resp = requests.get(BASE, params=params, timeout=10)
    if resp.status_code != 200:
        raise WeatherError(f"OpenWeather error {resp.status_code}: {resp.text}")
    data = resp.json()
    return {
        "city": data.get("name"),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "weather": data.get("weather", [{}])[0].get("description"),
        "raw": data,
    }
