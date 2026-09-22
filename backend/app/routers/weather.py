from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import AnalysisResponse, CurrentWeather, FarmerAdvisoryResponse
from app.services import analysis_service, farmer_advisory_service, weather_service

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("", response_model=CurrentWeather)
async def current_weather(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    name: str | None = Query(None, description="Location name, alternative to lat/lon"),
):
    if lat is None and lon is None and not name:
        raise HTTPException(status_code=400, detail="Provide lat & lon, or a location name")
    try:
        return await weather_service.get_current_weather(lat=lat, lon=lon, name=name)
    except weather_service.WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/analysis", response_model=AnalysisResponse)
async def weather_analysis(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    name: str | None = Query(None),
):
    if lat is None and lon is None and not name:
        raise HTTPException(status_code=400, detail="Provide lat & lon, or a location name")
    try:
        return await analysis_service.analyze(lat=lat, lon=lon, name=name)
    except weather_service.WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/farmer-advisory", response_model=FarmerAdvisoryResponse)
async def farmer_advisory(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    name: str | None = Query(None),
):
    if lat is None and lon is None and not name:
        raise HTTPException(status_code=400, detail="Provide lat & lon, or a location name")
    try:
        return await farmer_advisory_service.get_farmer_advisory(lat=lat, lon=lon, name=name)
    except weather_service.WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
