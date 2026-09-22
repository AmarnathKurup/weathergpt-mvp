from typing import Any, Optional
from pydantic import BaseModel, Field


class LocationQuery(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class GeocodeResult(BaseModel):
    name: str
    country: Optional[str] = None
    admin1: Optional[str] = None
    lat: float
    lon: float
    timezone: Optional[str] = None


class CurrentWeather(BaseModel):
    location: str
    lat: float
    lon: float
    timezone: Optional[str] = None
    temperature_c: Optional[float] = None
    apparent_temperature_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    wind_direction_deg: Optional[float] = None
    precipitation_mm: Optional[float] = None
    weather_code: Optional[int] = None
    condition: Optional[str] = None
    is_day: Optional[bool] = None
    observed_at: Optional[str] = None
    source: str = "open-meteo"


class ForecastDay(BaseModel):
    date: str
    temp_max_c: Optional[float] = None
    temp_min_c: Optional[float] = None
    precipitation_sum_mm: Optional[float] = None
    precipitation_probability_pct: Optional[float] = None
    wind_speed_max_kmh: Optional[float] = None
    weather_code: Optional[int] = None
    condition: Optional[str] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None


class ForecastHour(BaseModel):
    time: str
    temperature_c: Optional[float] = None
    precipitation_mm: Optional[float] = None
    precipitation_probability_pct: Optional[float] = None
    weather_code: Optional[int] = None
    condition: Optional[str] = None


class ForecastResponse(BaseModel):
    location: str
    lat: float
    lon: float
    timezone: Optional[str] = None
    daily: list[ForecastDay] = Field(default_factory=list)
    hourly: list[ForecastHour] = Field(default_factory=list)
    source: str = "open-meteo"


class WeatherAlert(BaseModel):
    id: str
    event: str
    severity: str
    headline: str
    description: str
    start: Optional[str] = None
    end: Optional[str] = None
    source: str


class AlertsResponse(BaseModel):
    location: str
    lat: float
    lon: float
    alerts: list[WeatherAlert] = Field(default_factory=list)
    generated: list[WeatherAlert] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    location: str
    summary: str
    highlights: list[str] = Field(default_factory=list)
    risk_score: int = 0
    risk_level: str = "Low"
    risk_factors: list[str] = Field(default_factory=list)


class CommunityReportCreate(BaseModel):
    lat: float
    lon: float
    category: str  # e.g. "Flooding", "Waterlogging", "Power Outage", "Road Blocked", "Heavy Rain", "Other"
    note: Optional[str] = None
    location_name: Optional[str] = None


class CommunityReport(BaseModel):
    id: str
    lat: float
    lon: float
    category: str
    note: Optional[str] = None
    location_name: Optional[str] = None
    created_at: str
    distance_km: Optional[float] = None


class FarmerAdvisoryResponse(BaseModel):
    location: str
    spray_advice: str
    irrigation_advice: str
    livestock_advice: str
    summary: list[str] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)
    lat: Optional[float] = None
    lon: Optional[float] = None
    location_name: Optional[str] = None
    language: Optional[str] = None  # force a language; else auto-detect


class ToolCallTrace(BaseModel):
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    reply: str
    detected_language: str
    tool_calls: list[ToolCallTrace] = Field(default_factory=list)
    used_location: Optional[LocationQuery] = None
