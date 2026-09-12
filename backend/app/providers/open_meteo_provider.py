import httpx
from typing import Dict, Any
from backend.app.core.config import settings
from backend.app.providers.base import BaseWeatherProvider

class OpenMeteoProvider(BaseWeatherProvider):
    def __init__(self):
        self.base_url = settings.OPEN_METEO_BASE_URL

    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover",
            "hourly": "precipitation_probability,uv_index",
            "daily": "sunrise,sunset,uv_index_max",
            "timezone": "auto"
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            return res.json()

    async def get_forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m",
            "hourly": "temperature_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m,uv_index",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code,uv_index_max,sunrise,sunset",
            "timezone": "auto",
            "models": "best_match"
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            return res.json()
