from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LocationInfo(BaseModel):
    name: str = "Unknown Location"
    pincode: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: float = 0.0
    longitude: float = 0.0

class WarningItem(BaseModel):
    level: str = "GREEN"  # GREEN, YELLOW, ORANGE, RED
    category: str = "General"
    headline: str = ""
    description: str = ""
    issued_at: Optional[str] = None
    source: str = "IMD"

class ForecastHourlyItem(BaseModel):
    time: str
    temperature: float
    rain_probability: float
    rain_mm: float
    wind_speed: float
    weather_code: int
    weather_desc: str

class ForecastDailyItem(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    rain_probability: float
    precipitation_sum: float
    weather_code: int
    weather_desc: str
    uv_index_max: float

class WeatherSnapshot(BaseModel):
    location: LocationInfo
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    temperature: float = 0.0
    feels_like: float = 0.0
    humidity: float = 0.0
    pressure: float = 1013.25
    wind_speed: float = 0.0
    wind_direction: float = 0.0
    wind_gust: float = 0.0
    visibility: float = 10000.0
    cloud_cover: float = 0.0
    rain: float = 0.0
    rain_probability: float = 0.0
    weather_code: int = 0
    weather_desc: str = "Clear sky"
    uv_index: float = 0.0
    sunrise: str = "06:00"
    sunset: str = "18:00"
    warnings: List[WarningItem] = []
    source: str = "IMD + Open-Meteo"
    model: str = "ECMWF / GFS / IMD-AWS"
    confidence: float = 0.95

class ForecastResponse(BaseModel):
    location: LocationInfo
    current: WeatherSnapshot
    hourly: List[ForecastHourlyItem] = []
    daily: List[ForecastDailyItem] = []
    source: str = "Open-Meteo NWP Multi-Model"

class WarningResponse(BaseModel):
    location: LocationInfo
    active_warnings: List[WarningItem] = []
    highest_severity: str = "GREEN"
    total_warnings: int = 0
