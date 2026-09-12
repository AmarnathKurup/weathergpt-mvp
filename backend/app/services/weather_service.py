from typing import Dict, Any, List
from backend.app.providers.open_meteo_provider import OpenMeteoProvider
from backend.app.providers.imd_provider import IMDProvider
from backend.app.providers.weather_normalizer import WeatherNormalizer
from backend.app.location.location_engine import location_engine
from backend.app.schemas.weather import WeatherSnapshot, ForecastResponse, ForecastHourlyItem, ForecastDailyItem

class WeatherService:
    def __init__(self):
        self.open_meteo = OpenMeteoProvider()
        self.imd = IMDProvider()

    async def get_current_weather(self, location_query: str = None, lat: float = None, lon: float = None) -> WeatherSnapshot:
        loc = await location_engine.resolve_location(location_query, lat, lon)
        om_data = await self.open_meteo.get_current_weather(loc.latitude, loc.longitude)
        imd_warns_raw = await self.imd.get_district_warnings(loc.state or "West Bengal", loc.district or "Kolkata")

        # Parse IMD warning items
        from backend.app.alerts.warning_parser import WarningParser
        imd_warnings = WarningParser.parse_warnings(imd_warns_raw)

        return WeatherNormalizer.normalize_open_meteo(om_data, loc, imd_warnings)

    async def get_forecast(self, location_query: str = None, lat: float = None, lon: float = None) -> ForecastResponse:
        loc = await location_engine.resolve_location(location_query, lat, lon)
        om_data = await self.open_meteo.get_forecast(loc.latitude, loc.longitude)
        current_snapshot = await self.get_current_weather(location_query, lat, lon)

        hourly_raw = om_data.get("hourly", {})
        daily_raw = om_data.get("daily", {})

        hourly_items = []
        times = hourly_raw.get("time", [])
        temps = hourly_raw.get("temperature_2m", [])
        rain_probs = hourly_raw.get("precipitation_probability", [])
        rains = hourly_raw.get("precipitation", [])
        winds = hourly_raw.get("wind_speed_10m", [])
        codes = hourly_raw.get("weather_code", [])

        for i in range(min(24, len(times))):
            hourly_items.append(ForecastHourlyItem(
                time=times[i],
                temperature=temps[i] if i < len(temps) else 25.0,
                rain_probability=rain_probs[i] if i < len(rain_probs) else 0.0,
                rain_mm=rains[i] if i < len(rains) else 0.0,
                wind_speed=winds[i] if i < len(winds) else 10.0,
                weather_code=codes[i] if i < len(codes) else 0,
                weather_desc="Hourly forecast"
            ))

        daily_items = []
        d_dates = daily_raw.get("time", [])
        d_tmax = daily_raw.get("temperature_2m_max", [])
        d_tmin = daily_raw.get("temperature_2m_min", [])
        d_rain_prob = daily_raw.get("precipitation_probability_max", [])
        d_precip = daily_raw.get("precipitation_sum", [])
        d_codes = daily_raw.get("weather_code", [])

        for i in range(min(7, len(d_dates))):
            daily_items.append(ForecastDailyItem(
                date=d_dates[i],
                temp_max=d_tmax[i] if i < len(d_tmax) else 30.0,
                temp_min=d_tmin[i] if i < len(d_tmin) else 20.0,
                rain_probability=d_rain_prob[i] if i < len(d_rain_prob) else 0.0,
                precipitation_sum=d_precip[i] if i < len(d_precip) else 0.0,
                weather_code=d_codes[i] if i < len(d_codes) else 0,
                weather_desc="Daily forecast",
                uv_index_max=7.5
            ))

        return ForecastResponse(
            location=loc,
            current=current_snapshot,
            hourly=hourly_items,
            daily=daily_items
        )

weather_service = WeatherService()
