from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from backend.app.schemas.location import PincodeDetails, LocationResolveResponse
from backend.app.location.pincode_service import pincode_service
from backend.app.location.location_engine import location_engine

router = APIRouter(prefix="/location", tags=["Location & Geospatial"])

@router.get("/pincode/{pin}", response_model=PincodeDetails)
async def get_pincode_details(pin: str):
    res = pincode_service.get_by_pincode(pin)
    if not res:
        raise HTTPException(status_code=404, detail=f"Pincode {pin} not found in India Post directory.")
    return res

@router.get("/search", response_model=List[PincodeDetails])
async def search_locations(q: str = Query(..., description="Post office, district or state name")):
    return pincode_service.search_by_name(q)

@router.get("/resolve", response_model=LocationResolveResponse)
async def resolve_location(
    q: Optional[str] = Query(None, description="PIN code or city name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    loc = await location_engine.resolve_location(q, lat, lon)
    return LocationResolveResponse(
        query=q or "coords",
        resolved_name=loc.name,
        pincode=loc.pincode,
        district=loc.district,
        state=loc.state,
        latitude=loc.latitude,
        longitude=loc.longitude
    )
