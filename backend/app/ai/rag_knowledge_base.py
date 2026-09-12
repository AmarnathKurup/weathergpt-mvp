from typing import List, Dict

METEOROLOGICAL_KNOWLEDGE = [
    {
        "topic": "IMD Warning Levels",
        "keywords": ["warning", "red", "orange", "yellow", "green", "alert"],
        "content": "IMD Warnings: GREEN (No warning/Normal), YELLOW (Watch - Be updated), ORANGE (Alert - Be prepared), RED (Warning - Take immediate action)."
    },
    {
        "topic": "Rainfall Categories",
        "keywords": ["rain", "heavy", "moderate", "light", "mm"],
        "content": "IMD Rainfall Classification: Light (2.5-15.5 mm/day), Moderate (15.6-64.4 mm/day), Heavy (64.5-115.5 mm/day), Very Heavy (115.6-204.4 mm/day), Extremely Heavy (>204.5 mm/day)."
    },
    {
        "topic": "Thunderstorm Safety",
        "keywords": ["thunderstorm", "lightning", "bajra", "bijli"],
        "content": "Thunderstorm Safety Guidelines: Seek shelter in a sturdy building or hard-topped vehicle. Avoid water bodies, open fields, elevated terrain, wire fences, and tall isolated trees. Unplug sensitive electrical equipment."
    },
    {
        "topic": "Heat Wave Guidelines",
        "keywords": ["heatwave", "heat", "garmi", "loo", "temperature"],
        "content": "Heat Wave Action Plan: Drink ORS, lassi, or lemon water. Wear lightweight, light-colored cotton clothes. Avoid direct sun between 12 PM and 3 PM."
    },
    {
        "topic": "Agricultural Drainage & Irrigation",
        "keywords": ["crop", "farm", "irrigation", "paddy"],
        "content": "Agricultural Rule: When rain probability exceeds 70%, postpone irrigation and chemical application. Ensure field bunds are maintained to drain excess water."
    }
]

class RAGKnowledgeBase:
    @staticmethod
    def retrieve(query: str) -> List[str]:
        q_lower = query.lower()
        retrieved = []
        for item in METEOROLOGICAL_KNOWLEDGE:
            for kw in item["keywords"]:
                if kw in q_lower:
                    retrieved.append(item["content"])
                    break
        return retrieved

rag_knowledge_base = RAGKnowledgeBase()
