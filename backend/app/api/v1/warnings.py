from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.weather import WarningResponse
from backend.app.services.weather_service import weather_service

router = APIRouter(prefix="/warnings", tags=["Warnings & Alerts"])

@router.get("", response_model=WarningResponse)
async def get_warnings(
    location: Optional[str] = Query(None, description="PIN code or district"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    snapshot = await weather_service.get_current_weather(location, lat, lon)
    return WarningResponse(
        location=snapshot.location,
        active_warnings=snapshot.warnings,
        highest_severity="RED" if any(w.level == "RED" for w in snapshot.warnings) else (
            "ORANGE" if any(w.level == "ORANGE" for w in snapshot.warnings) else (
                "YELLOW" if any(w.level == "YELLOW" for w in snapshot.warnings) else "GREEN"
            )
        ),
        total_warnings=len(snapshot.warnings)
    )
