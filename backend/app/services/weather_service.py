from datetime import datetime, timezone

import httpx

from app.config import get_settings
from app.models.schemas import CurrentWeather, GeocodeResult
from app.services import location_service
from app.services.weather_codes import describe_weather_code
from app.utils.cache import cache

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    pass


async def resolve_location(
    lat: float | None, lon: float | None, name: str | None
) -> GeocodeResult:
    try:
        if lat is not None and lon is not None:
            loc = await location_service.reverse_geocode(lat, lon)
            if loc:
                return loc
            return GeocodeResult(name=f"{lat:.2f}, {lon:.2f}", lat=lat, lon=lon)
        if name:
            matches = await location_service.geocode(name, count=1)
            if not matches:
                raise WeatherServiceError(f"Could not find location '{name}'")
            return matches[0]
    except location_service.LocationServiceError as e:
        raise WeatherServiceError(str(e)) from e
    raise WeatherServiceError("Provide either lat/lon or a location name")


async def get_current_weather(
    lat: float | None = None, lon: float | None = None, name: str | None = None
) -> CurrentWeather:
    location = await resolve_location(lat, lon, name)

    cache_key = f"current:{location.lat:.3f}:{location.lon:.3f}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    settings = get_settings()
    params = {
        "latitude": location.lat,
        "longitude": location.lon,
        "current": ",".join(
            [
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
                "wind_direction_10m",
                "is_day",
            ]
        ),
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(OPEN_METEO_URL, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise WeatherServiceError(f"Open-Meteo request failed: {e}") from e

    data = resp.json()
    cur = data.get("current", {})

    result = CurrentWeather(
        location=location.name,
        lat=location.lat,
        lon=location.lon,
        timezone=data.get("timezone", location.timezone),
        temperature_c=cur.get("temperature_2m"),
        apparent_temperature_c=cur.get("apparent_temperature"),
        humidity_pct=cur.get("relative_humidity_2m"),
        wind_speed_kmh=cur.get("wind_speed_10m"),
        wind_direction_deg=cur.get("wind_direction_10m"),
        precipitation_mm=cur.get("precipitation"),
        weather_code=cur.get("weather_code"),
        condition=describe_weather_code(cur.get("weather_code")),
        is_day=bool(cur.get("is_day")) if cur.get("is_day") is not None else None,
        observed_at=cur.get("time") or datetime.now(timezone.utc).isoformat(),
        source="open-meteo",
    )

    # Optional OpenWeather enrichment if a key is configured - purely additive,
    # never blocks the response if it fails or key is absent.
    if settings.openweather_api_key:
        try:
            async with httpx.AsyncClient(timeout=6) as client:
                ow_resp = await client.get(
                    OPENWEATHER_URL,
                    params={
                        "lat": location.lat,
                        "lon": location.lon,
                        "appid": settings.openweather_api_key,
                        "units": "metric",
                    },
                )
            if ow_resp.status_code == 200:
                ow = ow_resp.json()
                # Prefer OpenWeather's human description if present, keep our own as fallback
                desc = (ow.get("weather") or [{}])[0].get("description")
                if desc:
                    result.condition = f"{result.condition} ({desc})"
        except httpx.HTTPError:
            pass  # non-fatal enrichment, ignore silently

    cache.set(cache_key, result, ttl=get_settings().cache_ttl_seconds)
    return result
