from typing import Dict, Any, List
from datetime import datetime
from backend.app.schemas.weather import WeatherSnapshot, LocationInfo, WarningItem

WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog and depositing rime fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

class WeatherNormalizer:
    @staticmethod
    def normalize_open_meteo(
        data: Dict[str, Any],
        location: LocationInfo,
        imd_warnings: List[WarningItem] = []
    ) -> WeatherSnapshot:
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})

        wmo_code = int(current.get("weather_code", 0))
        weather_desc = WMO_CODE_MAP.get(wmo_code, "Partly cloudy")

        # Extract current or max rain probability from hourly forecast
        rain_probs = hourly.get("precipitation_probability", [0])
        current_rain_prob = rain_probs[0] if rain_probs else 0.0
        uv_indices = hourly.get("uv_index", [0.0])
        current_uv = uv_indices[0] if uv_indices else 0.0

        sunrises = daily.get("sunrise", ["06:00"])
        sunsets = daily.get("sunset", ["18:00"])

        sunrise_str = sunrises[0].split("T")[-1] if "T" in sunrises[0] else sunrises[0]
        sunset_str = sunsets[0].split("T")[-1] if "T" in sunsets[0] else sunsets[0]

        snapshot = WeatherSnapshot(
            location=location,
            timestamp=datetime.utcnow().isoformat(),
            temperature=round(float(current.get("temperature_2m", 25.0)), 1),
            feels_like=round(float(current.get("apparent_temperature", 25.0)), 1),
            humidity=round(float(current.get("relative_humidity_2m", 60.0)), 1),
            pressure=round(float(current.get("surface_pressure", 1013.0)), 1),
            wind_speed=round(float(current.get("wind_speed_10m", 10.0)), 1),
            wind_direction=round(float(current.get("wind_direction_10m", 180.0)), 1),
            wind_gust=round(float(current.get("wind_gusts_10m", 15.0)), 1),
            cloud_cover=round(float(current.get("cloud_cover", 20.0)), 1),
            rain=round(float(current.get("rain", current.get("precipitation", 0.0))), 2),
            rain_probability=round(float(current_rain_prob), 1),
            weather_code=wmo_code,
            weather_desc=weather_desc,
            uv_index=round(float(current_uv), 1),
            sunrise=sunrise_str,
            sunset=sunset_str,
            warnings=imd_warnings,
            source="IMD + Open-Meteo",
            model="ECMWF / GFS Operational",
            confidence=0.96
        )

        return snapshot
