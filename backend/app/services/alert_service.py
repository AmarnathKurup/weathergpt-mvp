import httpx

from app.models.schemas import AlertsResponse, WeatherAlert
from app.services.forecast_service import get_forecast
from app.services.weather_service import get_current_weather
from app.utils.cache import cache

NWS_ALERTS_URL = "https://api.weather.gov/alerts/active"


def _is_probably_us(lat: float, lon: float) -> bool:
    # Rough continental US + Alaska/Hawaii bounding check - good enough for an MVP
    return (24.0 <= lat <= 72.0 and -170.0 <= lon <= -66.0)


async def _fetch_nws_alerts(lat: float, lon: float) -> list[WeatherAlert]:
    """NOAA's National Weather Service alerts API - free, no key, US-only coverage."""
    if not _is_probably_us(lat, lon):
        return []
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(
                NWS_ALERTS_URL,
                params={"point": f"{lat},{lon}"},
                headers={"User-Agent": "WeatherGPT-MVP (demo, contact: dev@example.com)"},
            )
        if resp.status_code != 200:
            return []
        data = resp.json()
    except httpx.HTTPError:
        return []

    alerts = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        alerts.append(
            WeatherAlert(
                id=str(props.get("id", "")),
                event=props.get("event", "Alert"),
                severity=props.get("severity", "Unknown"),
                headline=props.get("headline", props.get("event", "Weather Alert")),
                description=(props.get("description") or "")[:800],
                start=props.get("onset"),
                end=props.get("ends"),
                source="NOAA-NWS",
            )
        )
    return alerts


def _generate_hazard_alerts(current, forecast) -> list[WeatherAlert]:
    """Simple threshold-based hazard detection derived from current + forecast data.

    This is our fallback/global hazard layer for regions (like India) where a
    free, structured government alerts API isn't readily available for an MVP.
    """
    generated: list[WeatherAlert] = []

    if current.temperature_c is not None and current.temperature_c >= 40:
        generated.append(
            WeatherAlert(
                id="heat-current",
                event="Extreme Heat",
                severity="Severe" if current.temperature_c >= 45 else "Moderate",
                headline=f"High temperature of {current.temperature_c:.0f}°C",
                description=(
                    "Current temperature is very high. Stay hydrated, avoid "
                    "prolonged sun exposure, and watch for heat-stroke symptoms."
                ),
                source="WeatherGPT-Analysis",
            )
        )

    if current.wind_speed_kmh is not None and current.wind_speed_kmh >= 50:
        generated.append(
            WeatherAlert(
                id="wind-current",
                event="High Wind",
                severity="Severe" if current.wind_speed_kmh >= 80 else "Moderate",
                headline=f"Strong winds at {current.wind_speed_kmh:.0f} km/h",
                description="Secure loose outdoor objects and avoid high-sided vehicles.",
                source="WeatherGPT-Analysis",
            )
        )

    for day in forecast.daily:
        if day.precipitation_sum_mm is not None and day.precipitation_sum_mm >= 64:
            generated.append(
                WeatherAlert(
                    id=f"rain-{day.date}",
                    event="Heavy Rainfall",
                    severity="Severe" if day.precipitation_sum_mm >= 115 else "Moderate",
                    headline=f"Heavy rain expected on {day.date} "
                    f"({day.precipitation_sum_mm:.0f} mm)",
                    description=(
                        "Possible localized flooding and waterlogging. "
                        "Avoid low-lying and flood-prone areas."
                    ),
                    start=day.date,
                    end=day.date,
                    source="WeatherGPT-Analysis",
                )
            )
        if day.weather_code in (95, 96, 99):
            generated.append(
                WeatherAlert(
                    id=f"storm-{day.date}",
                    event="Thunderstorm",
                    severity="Moderate",
                    headline=f"Thunderstorms possible on {day.date}",
                    description="Risk of lightning, gusty winds, and short bursts of heavy rain.",
                    start=day.date,
                    end=day.date,
                    source="WeatherGPT-Analysis",
                )
            )

    return generated


async def get_alerts(
    lat: float | None = None, lon: float | None = None, name: str | None = None
) -> AlertsResponse:
    current = await get_current_weather(lat=lat, lon=lon, name=name)
    forecast = await get_forecast(lat=lat, lon=lon, name=name, days=5)

    cache_key = f"alerts:{current.lat:.3f}:{current.lon:.3f}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    official = await _fetch_nws_alerts(current.lat, current.lon)
    generated = _generate_hazard_alerts(current, forecast)

    result = AlertsResponse(
        location=current.location,
        lat=current.lat,
        lon=current.lon,
        alerts=official,
        generated=generated,
    )
    cache.set(cache_key, result, ttl=900)
    return result
