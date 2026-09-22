"""Crowdsourced ground-truth reports.

Official weather/hazard data can lag reality during fast-moving events
(flash flooding, localized waterlogging, downed trees). This gives people
nearby a way to report what's actually happening on the ground, which both
shows up on the map and can be surfaced by the chat agent alongside official
data - a lightweight "trust but verify" layer.

Stored in-memory only (per MVP scope - no database). Reports are capped and
pruned by age so this doesn't grow unbounded during a long-running dev server.
"""
import math
import uuid
from datetime import datetime, timedelta, timezone

from app.models.schemas import CommunityReport, CommunityReportCreate

VALID_CATEGORIES = {
    "Flooding",
    "Waterlogging",
    "Power Outage",
    "Road Blocked",
    "Heavy Rain",
    "Landslide Risk",
    "Fallen Tree",
    "Other",
}

MAX_REPORTS = 500
REPORT_TTL = timedelta(hours=24)

_reports: list[dict] = []


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _prune() -> None:
    cutoff = datetime.now(timezone.utc) - REPORT_TTL
    global _reports
    _reports = [
        r for r in _reports if datetime.fromisoformat(r["created_at"]) > cutoff
    ][-MAX_REPORTS:]


def add_report(payload: CommunityReportCreate) -> CommunityReport:
    category = payload.category if payload.category in VALID_CATEGORIES else "Other"
    record = {
        "id": str(uuid.uuid4())[:8],
        "lat": payload.lat,
        "lon": payload.lon,
        "category": category,
        "note": (payload.note or "").strip()[:280] or None,
        "location_name": payload.location_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _reports.append(record)
    _prune()
    return CommunityReport(**record)


def get_nearby(lat: float, lon: float, radius_km: float = 25, limit: int = 20) -> list[CommunityReport]:
    _prune()
    results = []
    for r in _reports:
        dist = _haversine_km(lat, lon, r["lat"], r["lon"])
        if dist <= radius_km:
            results.append(CommunityReport(**r, distance_km=round(dist, 1)))
    results.sort(key=lambda r: r.distance_km or 0)
    return results[:limit]
