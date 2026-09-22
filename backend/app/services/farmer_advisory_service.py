"""Turns raw forecast numbers into plain-language farming decisions.

Simple rule-based thresholds (not a crop model) - the goal for this MVP is
to demonstrate the pattern (weather data -> domain-specific actionable advice)
rather than build an agronomy engine. Real deployment would want
crop-specific and soil-specific rules.
"""
from app.models.schemas import FarmerAdvisoryResponse
from app.services.forecast_service import get_forecast
from app.services.weather_service import get_current_weather


async def get_farmer_advisory(
    lat: float | None = None, lon: float | None = None, name: str | None = None
) -> FarmerAdvisoryResponse:
    current = await get_current_weather(lat=lat, lon=lon, name=name)
    forecast = await get_forecast(lat=lat, lon=lon, name=name, days=3)

    summary: list[str] = []
    today = forecast.daily[0] if forecast.daily else None
    next_3d_rain = sum(d.precipitation_sum_mm or 0 for d in forecast.daily[:3])
    rain_soon = (today.precipitation_probability_pct or 0) >= 60 if today else False

    # Spraying (pesticide/fertilizer) advice
    if rain_soon:
        spray_advice = (
            "Hold off on spraying pesticide or fertilizer today - rain is likely "
            "and will wash it off before it takes effect."
        )
    elif current.wind_speed_kmh is not None and current.wind_speed_kmh >= 25:
        spray_advice = (
            "Winds are a bit strong for spraying right now - drift risk is high. "
            "Early morning or evening, when wind usually drops, is a better window."
        )
    else:
        spray_advice = "Conditions look reasonable for spraying today - low rain and wind risk."
    summary.append(spray_advice)

    # Irrigation advice
    if next_3d_rain >= 20:
        irrigation_advice = (
            f"About {next_3d_rain:.0f}mm of rain is expected over the next 3 days - "
            "you can likely skip irrigation for now."
        )
    elif next_3d_rain >= 5:
        irrigation_advice = (
            f"Only light rain expected (~{next_3d_rain:.0f}mm over 3 days) - "
            "monitor soil moisture, partial irrigation may still be needed."
        )
    else:
        irrigation_advice = "Little to no rain expected in the next 3 days - plan for irrigation."
    summary.append(irrigation_advice)

    # Livestock heat stress advice
    max_temp = max((d.temp_max_c for d in forecast.daily[:3] if d.temp_max_c is not None), default=None)
    if max_temp is not None and max_temp >= 38:
        livestock_advice = (
            f"Temperatures reaching {max_temp:.0f}°C in the next few days - ensure livestock "
            "have shade, ventilation, and constant access to water."
        )
    elif max_temp is not None and max_temp >= 33:
        livestock_advice = "Warm days ahead - keep an eye on water availability for animals."
    else:
        livestock_advice = "No significant heat stress risk for livestock expected."
    summary.append(livestock_advice)

    return FarmerAdvisoryResponse(
        location=current.location,
        spray_advice=spray_advice,
        irrigation_advice=irrigation_advice,
        livestock_advice=livestock_advice,
        summary=summary,
    )
