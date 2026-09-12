from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.app.schemas.weather import WeatherSnapshot

class BaseWeatherProvider(ABC):
    @abstractmethod
    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        pass
