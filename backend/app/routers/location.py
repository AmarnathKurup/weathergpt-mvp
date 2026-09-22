from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import GeocodeResult
from app.services import location_service

router = APIRouter(prefix="/api/location", tags=["location"])


@router.get("", response_model=list[GeocodeResult])
async def search_location(q: str = Query(..., min_length=1, description="Place name to search")):
    try:
        return await location_service.geocode(q)
    except location_service.LocationServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/reverse", response_model=GeocodeResult)
async def reverse(lat: float, lon: float):
    result = await location_service.reverse_geocode(lat, lon)
    if result is None:
        raise HTTPException(status_code=404, detail="Could not resolve location")
    return result
