from typing import Dict, Any, List
from backend.app.schemas.weather import WeatherSnapshot

class ContextBuilder:
    @staticmethod
    def build_context(
        user_query: str,
        occupation: str,
        language: str,
        snapshot: WeatherSnapshot,
        events: List[str],
        actions: List[str],
        rag_context: List[str]
    ) -> Dict[str, Any]:
        return {
            "query": user_query,
            "user": {
                "occupation": occupation,
                "language": language
            },
            "location": {
                "name": snapshot.location.name,
                "pincode": snapshot.location.pincode,
                "district": snapshot.location.district,
                "state": snapshot.location.state,
                "latitude": snapshot.location.latitude,
                "longitude": snapshot.location.longitude
            },
            "weather_facts": {
                "temperature": snapshot.temperature,
                "feels_like": snapshot.feels_like,
                "rain_probability": snapshot.rain_probability,
                "rain_mm": snapshot.rain,
                "wind_kmh": snapshot.wind_speed,
                "humidity": snapshot.humidity,
                "uv_index": snapshot.uv_index,
                "weather_desc": snapshot.weather_desc,
                "source": snapshot.source,
                "model": snapshot.model,
                "timestamp": snapshot.timestamp
            },
            "warnings": [w.dict() for w in snapshot.warnings],
            "detected_events": events,
            "recommended_actions": actions,
            "rag_knowledge": rag_context
        }

context_builder = ContextBuilder()
