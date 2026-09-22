import httpx

from app.models.schemas import GeocodeResult
from app.utils.cache import cache

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
REVERSE_URL = "https://geocoding-api.open-meteo.com/v1/reverse"


class LocationServiceError(Exception):
    pass


async def geocode(name: str, count: int = 5) -> list[GeocodeResult]:
    """Resolve a place name to lat/lon using Open-Meteo geocoding (free, no key)."""
    key = f"geocode:{name.lower()}:{count}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    params = {"name": name, "count": count, "language": "en", "format": "json"}
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(GEOCODE_URL, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise LocationServiceError(f"Geocoding request failed: {e}") from e

    data = resp.json()
    results = []
    for item in data.get("results", []) or []:
        results.append(
            GeocodeResult(
                name=item.get("name", name),
                country=item.get("country"),
                admin1=item.get("admin1"),
                lat=item["latitude"],
                lon=item["longitude"],
                timezone=item.get("timezone"),
            )
        )
    cache.set(key, results, ttl=3600)
    return results


async def reverse_geocode(lat: float, lon: float) -> GeocodeResult | None:
    """Best-effort reverse geocode. Falls back to coordinate label if unavailable."""
    key = f"reverse:{lat:.3f}:{lon:.3f}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    params = {"latitude": lat, "longitude": lon, "language": "en", "format": "json"}
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(REVERSE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError:
            data = {}

    results = data.get("results") or []
    if results:
        item = results[0]
        result = GeocodeResult(
            name=item.get("name", f"{lat:.2f},{lon:.2f}"),
            country=item.get("country"),
            admin1=item.get("admin1"),
            lat=lat,
            lon=lon,
            timezone=item.get("timezone"),
        )
    else:
        result = GeocodeResult(name=f"{lat:.2f}, {lon:.2f}", lat=lat, lon=lon)

    cache.set(key, result, ttl=3600)
    return result
