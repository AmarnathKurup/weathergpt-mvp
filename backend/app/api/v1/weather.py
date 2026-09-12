from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.weather import WeatherSnapshot, ForecastResponse
from backend.app.services.weather_service import weather_service
from backend.app.location.pincode_service import pincode_service

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current", response_model=WeatherSnapshot)
async def get_current_weather(
    location: Optional[str] = Query(None, description="PIN code or city name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    return await weather_service.get_current_weather(location, lat, lon)

@router.get("/forecast", response_model=ForecastResponse)
async def get_weather_forecast(
    location: Optional[str] = Query(None, description="PIN code or city name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    return await weather_service.get_forecast(location, lat, lon)

@router.get("/pincode/{pin}", response_model=WeatherSnapshot)
async def get_weather_by_pincode(pin: str):
    return await weather_service.get_current_weather(location_query=pin)
