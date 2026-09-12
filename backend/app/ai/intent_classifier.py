import re
from typing import Dict, Any

INTENT_PATTERNS = {
    "RAIN_QUERY": r"\b(rain|raining|drizzle|shower|thunderstorm|downpour|umbrella|raincoat|barsat|baaris|bristi)\b",
    "TEMPERATURE_QUERY": r"\b(temp|temperature|hot|cold|heat|degree|celsius|garmi|thand)\b",
    "WARNING_QUERY": r"\b(warning|alert|cyclone|flood|danger|storm|red alert|orange alert|imd alert)\b",
    "AGRICULTURE_ADVISORY": r"\b(crop|farm|farmer|kisan|irrigation|harvest|field|sowing|paddy|wheat|fertilizer)\b",
    "TRAVEL_ADVISORY": r"\b(travel|drive|flight|commute|road|train|college|office|leaving|trip|journey)\b",
    "HEALTH_WEATHER": r"\b(health|uv|sunburn|dehydration|asthma|allergy|air quality|aqi|skin)\b",
    "MARINE_QUERY": r"\b(sea|ocean|fisherman|fishing|wave|coastal|tide|port)\b",
    "AVIATION_QUERY": r"\b(flight|pilot|visibility|wind gust|aviation|landing)\b",
    "CLIMATE_QUERY": r"\b(climate|historical|trend|anomaly|last year|past 10 years|global warming)\b",
    "FORECAST": r"\b(tomorrow|forecast|next week|evening|tonight|later|weekend|future)\b",
    "CURRENT_WEATHER": r"\b(now|current|today|right now|present|weather|aaj)\b"
}

class IntentClassifier:
    @staticmethod
    def classify(query: str) -> str:
        q_lower = query.lower().strip()

        for intent, pattern in INTENT_PATTERNS.items():
            if re.search(pattern, q_lower):
                return intent

        return "GENERAL_WEATHER_QUERY"

intent_classifier = IntentClassifier()
