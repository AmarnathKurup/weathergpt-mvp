from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import AlertsResponse
from app.services import alert_service
from app.services.weather_service import WeatherServiceError

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=AlertsResponse)
async def alerts(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    name: str | None = Query(None),
):
    if lat is None and lon is None and not name:
        raise HTTPException(status_code=400, detail="Provide lat & lon, or a location name")
    try:
        return await alert_service.get_alerts(lat=lat, lon=lon, name=name)
    except WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
