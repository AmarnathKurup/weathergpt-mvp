from typing import List, Dict, Any
from backend.app.schemas.weather import WarningItem

class WarningParser:
    """
    Parses IMD Official Warning Levels:
    - GREEN  : No warning (Normal conditions)
    - YELLOW : Watch (Be updated)
    - ORANGE : Alert (Be prepared)
    - RED    : Warning (Take action)
    """

    @staticmethod
    def parse_warnings(imd_data: List[Dict[str, Any]]) -> List[WarningItem]:
        warnings = []
        for item in imd_data:
            level = str(item.get("level", "GREEN")).upper()
            if level not in ["GREEN", "YELLOW", "ORANGE", "RED"]:
                level = "GREEN"

            warnings.append(WarningItem(
                level=level,
                category=str(item.get("category", "Weather Warning")),
                headline=str(item.get("headline", "Weather Alert")),
                description=str(item.get("description", "")),
                issued_at=str(item.get("issued_at", "")),
                source="IMD (India Meteorological Department)"
            ))
        return warnings

    @staticmethod
    def get_highest_severity(warnings: List[WarningItem]) -> str:
        levels = [w.level.upper() for w in warnings]
        if "RED" in levels:
            return "RED"
        if "ORANGE" in levels:
            return "ORANGE"
        if "YELLOW" in levels:
            return "YELLOW"
        return "GREEN"
