from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import ForecastResponse
from app.services import forecast_service
from app.services.weather_service import WeatherServiceError

router = APIRouter(prefix="/api/forecast", tags=["forecast"])


@router.get("", response_model=ForecastResponse)
async def forecast(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    name: str | None = Query(None),
    days: int = Query(7, ge=1, le=16),
):
    if lat is None and lon is None and not name:
        raise HTTPException(status_code=400, detail="Provide lat & lon, or a location name")
    try:
        return await forecast_service.get_forecast(lat=lat, lon=lon, name=name, days=days)
    except WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
