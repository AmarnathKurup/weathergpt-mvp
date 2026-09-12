from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from backend.app.schemas.weather import WeatherSnapshot, WarningItem

class UserProfile(BaseModel):
    user_id: str = "guest"
    name: str = "User"
    age: Optional[int] = 25
    occupation: str = "general" # student, farmer, fisherman, driver, delivery_worker, senior_citizen, general
    preferred_language: str = "en" # en, hi, bn, ta, te, mr, gu, kn, ml, pa, or, etc.

class ChatRequest(BaseModel):
    query: str
    location: Optional[str] = None # PIN code, city name, or lat,lon
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    occupation: Optional[str] = "general"
    language: Optional[str] = "en"
    user_id: Optional[str] = "guest"

class ExplainabilityDetails(BaseModel):
    temperature: float
    rain_probability: float
    rain_mm: float
    wind_kmh: float
    uv_index: float
    weather_code: int
    weather_desc: str
    data_source: str
    nwp_model: str
    updated_at: str
    active_warnings: List[WarningItem] = []
    matched_rules: List[str] = []

class ChatResponse(BaseModel):
    query: str
    intent: str
    language: str
    location_name: str
    answer: str
    audio_url: Optional[str] = None
    weather_snapshot: WeatherSnapshot
    detected_events: List[str] = []
    recommended_actions: List[str] = []
    why_explainability: ExplainabilityDetails
    confidence: float = 0.95
