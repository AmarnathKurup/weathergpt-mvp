from fastapi import APIRouter, Query
from typing import Dict, Any
from backend.app.services.climate_service import climate_service

router = APIRouter(prefix="/climate", tags=["Climate Analytics"])

@router.get("/trend")
async def get_climate_trend(location: str = Query("Kolkata", description="Location name or PIN")):
    return await climate_service.get_historical_trends(location)
