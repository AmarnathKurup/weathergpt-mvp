import httpx

from app.config import get_settings
from app.models.schemas import ForecastDay, ForecastHour, ForecastResponse
from app.services.weather_codes import describe_weather_code
from app.services.weather_service import resolve_location, WeatherServiceError
from app.utils.cache import cache

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def get_forecast(
    lat: float | None = None,
    lon: float | None = None,
    name: str | None = None,
    days: int = 7,
) -> ForecastResponse:
    location = await resolve_location(lat, lon, name)
    days = max(1, min(days, 16))

    cache_key = f"forecast:{location.lat:.3f}:{location.lon:.3f}:{days}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    params = {
        "latitude": location.lat,
        "longitude": location.lon,
        "daily": ",".join(
            [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "weather_code",
                "sunrise",
                "sunset",
            ]
        ),
        "hourly": ",".join(
            [
                "temperature_2m",
                "precipitation",
                "precipitation_probability",
                "weather_code",
            ]
        ),
        "forecast_days": days,
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(OPEN_METEO_URL, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise WeatherServiceError(f"Open-Meteo forecast request failed: {e}") from e

    data = resp.json()
    daily_raw = data.get("daily", {})
    hourly_raw = data.get("hourly", {})

    daily = []
    for i, date in enumerate(daily_raw.get("time", [])):
        code = daily_raw.get("weather_code", [None] * len(daily_raw.get("time", [])))[i]
        daily.append(
            ForecastDay(
                date=date,
                temp_max_c=_at(daily_raw, "temperature_2m_max", i),
                temp_min_c=_at(daily_raw, "temperature_2m_min", i),
                precipitation_sum_mm=_at(daily_raw, "precipitation_sum", i),
                precipitation_probability_pct=_at(
                    daily_raw, "precipitation_probability_max", i
                ),
                wind_speed_max_kmh=_at(daily_raw, "wind_speed_10m_max", i),
                weather_code=code,
                condition=describe_weather_code(code),
                sunrise=_at(daily_raw, "sunrise", i),
                sunset=_at(daily_raw, "sunset", i),
            )
        )

    # Limit hourly to the next 48 entries to keep payloads small for the MVP
    hourly = []
    times = hourly_raw.get("time", [])
    for i, t in enumerate(times[:48]):
        code = _at(hourly_raw, "weather_code", i)
        hourly.append(
            ForecastHour(
                time=t,
                temperature_c=_at(hourly_raw, "temperature_2m", i),
                precipitation_mm=_at(hourly_raw, "precipitation", i),
                precipitation_probability_pct=_at(
                    hourly_raw, "precipitation_probability", i
                ),
                weather_code=code,
                condition=describe_weather_code(code),
            )
        )

    result = ForecastResponse(
        location=location.name,
        lat=location.lat,
        lon=location.lon,
        timezone=data.get("timezone", location.timezone),
        daily=daily,
        hourly=hourly,
        source="open-meteo",
    )
    cache.set(cache_key, result, ttl=get_settings().cache_ttl_seconds)
    return result


def _at(d: dict, key: str, i: int):
    values = d.get(key)
    if not values or i >= len(values):
        return None
    return values[i]
