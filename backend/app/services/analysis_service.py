from app.models.schemas import AlertsResponse, AnalysisResponse, CurrentWeather, ForecastResponse
from app.services.alert_service import get_alerts
from app.services.forecast_service import get_forecast
from app.services.weather_service import get_current_weather


def compute_risk_score(
    current: CurrentWeather, forecast: ForecastResponse, alerts: AlertsResponse
) -> tuple[int, str, list[str]]:
    """A simple composite 0-100 hazard score combining heat, wind, rain, and
    active alerts into one number - intended to give people a fast "how
    concerned should I be right now" read without parsing raw numbers.

    This is a transparent, rule-based score (not a black box) so the
    contributing factors can be shown alongside it.
    """
    score = 0
    factors: list[str] = []

    # Heat contribution
    if current.temperature_c is not None:
        if current.temperature_c >= 45:
            score += 35
            factors.append("Extreme heat")
        elif current.temperature_c >= 40:
            score += 25
            factors.append("High heat")
        elif current.temperature_c >= 35:
            score += 10
            factors.append("Warm conditions")

    # Wind contribution
    if current.wind_speed_kmh is not None:
        if current.wind_speed_kmh >= 80:
            score += 25
            factors.append("Damaging winds")
        elif current.wind_speed_kmh >= 50:
            score += 15
            factors.append("Strong winds")
        elif current.wind_speed_kmh >= 30:
            score += 5

    # Rain contribution - look at today's forecast
    if forecast.daily:
        today = forecast.daily[0]
        if today.precipitation_sum_mm is not None:
            if today.precipitation_sum_mm >= 115:
                score += 25
                factors.append("Extremely heavy rain expected")
            elif today.precipitation_sum_mm >= 64:
                score += 15
                factors.append("Heavy rain expected")
            elif today.precipitation_sum_mm >= 15:
                score += 5

    # Active alerts contribution (official + generated)
    all_alerts = alerts.alerts + alerts.generated
    for a in all_alerts:
        sev = a.severity.lower()
        if "extreme" in sev or "severe" in sev:
            score += 20
        elif "moderate" in sev:
            score += 10
        else:
            score += 5
    if all_alerts:
        factors.append(f"{len(all_alerts)} active alert(s)")

    score = min(score, 100)

    if score >= 75:
        level = "Severe"
    elif score >= 50:
        level = "High"
    elif score >= 25:
        level = "Moderate"
    else:
        level = "Low"

    if not factors:
        factors.append("No significant hazard factors")

    return score, level, factors


async def analyze(
    lat: float | None = None, lon: float | None = None, name: str | None = None
) -> AnalysisResponse:
    current = await get_current_weather(lat=lat, lon=lon, name=name)
    forecast = await get_forecast(lat=lat, lon=lon, name=name, days=3)
    alerts = await get_alerts(lat=lat, lon=lon, name=name)

    highlights: list[str] = []

    highlights.append(
        f"Currently {current.condition.lower() if current.condition else 'unknown'} "
        f"at {current.temperature_c}°C (feels like {current.apparent_temperature_c}°C)."
    )

    if forecast.daily:
        today = forecast.daily[0]
        highlights.append(
            f"Today's range: {today.temp_min_c}°C to {today.temp_max_c}°C, "
            f"{today.precipitation_probability_pct or 0:.0f}% chance of precipitation."
        )
        if len(forecast.daily) > 1:
            trend = [d.temp_max_c for d in forecast.daily if d.temp_max_c is not None]
            if len(trend) >= 2:
                if trend[-1] > trend[0] + 2:
                    highlights.append("Temperatures are trending warmer over the coming days.")
                elif trend[-1] < trend[0] - 2:
                    highlights.append("Temperatures are trending cooler over the coming days.")

    all_alerts = alerts.alerts + alerts.generated
    if all_alerts:
        events = ", ".join(sorted({a.event for a in all_alerts}))
        highlights.append(f"Active hazard watch: {events}.")
    else:
        highlights.append("No significant weather hazards detected right now.")

    risk_score, risk_level, risk_factors = compute_risk_score(current, forecast, alerts)

    summary = " ".join(highlights)

    return AnalysisResponse(
        location=current.location,
        summary=summary,
        highlights=highlights,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_factors=risk_factors,
    )
