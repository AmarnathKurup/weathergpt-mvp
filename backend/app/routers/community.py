from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import CommunityReport, CommunityReportCreate
from app.services import community_service

router = APIRouter(prefix="/api/community", tags=["community"])


@router.post("/reports", response_model=CommunityReport)
async def create_report(payload: CommunityReportCreate):
    if not (-90 <= payload.lat <= 90) or not (-180 <= payload.lon <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates")
    return community_service.add_report(payload)


@router.get("/reports", response_model=list[CommunityReport])
async def list_reports(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float = Query(25, ge=1, le=200),
):
    return community_service.get_nearby(lat, lon, radius_km=radius_km)
