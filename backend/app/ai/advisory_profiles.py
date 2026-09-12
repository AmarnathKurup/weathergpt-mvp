from typing import Dict, List

PROFILE_RULES: Dict[str, Dict[str, str]] = {
    "student": {
        "RAIN": "Rain is likely during college/evening transit. Carry an umbrella or raincoat in your bag.",
        "THUNDERSTORM": "Avoid open campus areas or standing under tall trees during lightning.",
        "HEAT": "Stay hydrated during afternoon outdoor classes or commuting."
    },
    "farmer": {
        "RAIN": "Heavy rain expected. Delay pesticide spraying/fertilizer application and monitor field drainage.",
        "THUNDERSTORM": "Move livestock and farm equipment to sheltered structures away from open fields.",
        "HEAT": "Schedule harvesting/irrigation during early morning or late evening to prevent crop moisture loss."
    },
    "fisherman": {
        "RAIN": "Rough sea conditions and heavy downpour expected. Check local coastal IMD bulletins.",
        "THUNDERSTORM": "Avoid venturing into deep sea or coastal waters due to high squally wind risks.",
        "HEAT": "Ensure adequate cold storage ice for fish catch preservation."
    },
    "driver": {
        "RAIN": "Road visibility may decrease and hydroplaning risk increases. Maintain safe distance.",
        "FOG": "Dense fog likely. Use low-beam fog lights and drive at reduced speed.",
        "HEAT": "Check vehicle tire pressure and engine coolant levels before long highway journeys."
    },
    "delivery_worker": {
        "RAIN": "Rainfall likely. Use waterproof covers for delivery parcels and wear high-visibility rain gear.",
        "HEAT": "Take short shaded hydration breaks every hour during peak afternoon shifts."
    },
    "senior_citizen": {
        "HEAT": "High heat index. Avoid outdoor morning/afternoon walks between 11 AM and 4 PM.",
        "COLD": "Cold wave conditions. Wear layered warm clothing and keep indoors well ventilated."
    },
    "general": {
        "RAIN": "Rain probability is high. Plan outdoor activities accordingly and carry protective gear.",
        "HEAT": "Warm and humid conditions expected. Drink plenty of water."
    }
}

class AdvisoryProfiles:
    @staticmethod
    def get_advisory(occupation: str, events: List[str]) -> List[str]:
        occ = occupation.lower().strip() if occupation else "general"
        rules = PROFILE_RULES.get(occ, PROFILE_RULES["general"])
        advisories = []

        for event in events:
            if "RAIN" in event and "RAIN" in rules:
                advisories.append(rules["RAIN"])
            elif "THUNDERSTORM" in event and "THUNDERSTORM" in rules:
                advisories.append(rules["THUNDERSTORM"])
            elif "HEAT" in event and "HEAT" in rules:
                advisories.append(rules["HEAT"])
            elif "FOG" in event and "FOG" in rules:
                advisories.append(rules["FOG"])

        if not advisories and "general" in PROFILE_RULES:
            advisories.append("Weather conditions are stable. Continue daily activities with standard awareness.")

        return list(set(advisories))

advisory_profiles = AdvisoryProfiles()
