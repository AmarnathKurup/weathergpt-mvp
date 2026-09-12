from typing import List, Dict, Tuple
from backend.app.schemas.weather import WeatherSnapshot

class RiskEngine:
    """
    Weather-to-Action Rule & Risk Detection Engine.
    Evaluates factual weather parameters against rule matrices to produce:
    1. Detected Events (e.g., HIGH_RAIN_PROBABILITY, THUNDERSTORM_RISK, HEATWAVE)
    2. Candidate Recommendations / Actions
    """

    @staticmethod
    def evaluate_risk(snapshot: WeatherSnapshot) -> Tuple[List[str], List[str]]:
        events = []
        actions = []

        # Rule 1: High Rain Probability / Precipitation
        if snapshot.rain_probability >= 70 or snapshot.rain > 5.0:
            events.append("EVENING_RAIN_LIKELY" if "17:" in snapshot.timestamp or "18:" in snapshot.timestamp else "HIGH_RAIN_PROBABILITY")
            actions.append("carry_umbrella_or_raincoat")
            actions.append("check_travel_and_road_conditions")

        # Rule 2: Heavy Rain / Flood Risk
        if snapshot.rain >= 15.0:
            events.append("HEAVY_RAINFALL")
            actions.append("avoid_waterlogged_low_lying_areas")
            actions.append("keep_electronic_devices_waterproofed")

        # Rule 3: Severe Weather / Thunderstorm WMO codes 95, 96, 99
        if snapshot.weather_code in [95, 96, 99]:
            events.append("THUNDERSTORM_LIGHTNING_RISK")
            actions.append("avoid_open_grounds_and_tall_trees")
            actions.append("stay_indoors_during_peak_thunderstorm")

        # Rule 4: Extreme Heat / Heatwave
        if snapshot.temperature >= 38.0 or snapshot.feels_like >= 42.0:
            events.append("HEATWAVE_EXPOSURE_RISK")
            actions.append("stay_hydrated_and_drink_water")
            actions.append("limit_direct_sun_exposure_in_afternoon")

        # Rule 5: High Wind Speed
        if snapshot.wind_speed >= 30.0 or snapshot.wind_gust >= 45.0:
            events.append("HIGH_WIND_GUSTS")
            actions.append("secure_loose_outdoor_items")
            actions.append("exercise_caution_on_elevated_highways")

        # Rule 6: High UV Index
        if snapshot.uv_index >= 7.0:
            events.append("HIGH_UV_RADIATION")
            actions.append("apply_sunscreen_and_wear_sunglasses")

        # Rule 7: Fog / Low Visibility
        if snapshot.visibility <= 1000 or snapshot.weather_code in [45, 48]:
            events.append("FOG_LOW_VISIBILITY")
            actions.append("use_fog_lights_and_drive_at_reduced_speed")

        # Include official IMD warning severity events if present
        for warning in snapshot.warnings:
            if warning.level in ["ORANGE", "RED"]:
                events.append(f"IMD_{warning.level}_WARNING_{warning.category.upper().replace(' ', '_')}")
                actions.append("follow_official_imd_and_local_authority_advisories")

        if not events:
            events.append("PLEASANT_WEATHER")
            actions.append("enjoy_the_clear_weather")

        return events, list(set(actions))

risk_engine = RiskEngine()
