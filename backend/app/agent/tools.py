"""Weather tools exposed to the LLM via function/tool calling.

Each tool wraps a real backend service call - the agent never invents
weather data itself, it must call these to get real numbers.
"""
from typing import Any

from app.knowledge import knowledge_base
from app.services import (
    alert_service,
    analysis_service,
    community_service,
    farmer_advisory_service,
    forecast_service,
    location_service,
)
from app.services import weather_service

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": (
                "Get the current/live weather conditions for a location. "
                "Use this whenever the user asks what the weather is right now."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "City or place name, e.g. 'Thiruvananthapuram' or 'Paris'",
                    },
                    "lat": {"type": "number", "description": "Latitude, if known"},
                    "lon": {"type": "number", "description": "Longitude, if known"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": (
                "Get the multi-day (and hourly) weather forecast for a location. "
                "Use for questions about tomorrow, this week, or upcoming days."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {"type": "string"},
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "days": {
                        "type": "integer",
                        "description": "Number of forecast days requested (1-16)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_alerts",
            "description": (
                "Get active weather alerts, warnings, and hazards for a location "
                "(storms, heat, heavy rain, wind, etc.)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {"type": "string"},
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_weather",
            "description": (
                "Get a synthesized plain-language analysis/summary of current "
                "conditions, short-term trend, and hazards for a location."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {"type": "string"},
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "geocode_location",
            "description": "Resolve a place name to coordinates, or find matching places for an ambiguous name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Place name to search for"},
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_meteorology_knowledge",
            "description": (
                "Search a local knowledge base of meteorological/climate/disaster "
                "domain knowledge (IMD practices, heatwaves, monsoons, cyclones, "
                "flood/heat safety, AQI, etc). Use for 'what is/how does/why' "
                "conceptual questions, not for live data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The topic or question to search for"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_community_reports",
            "description": (
                "Get recent crowdsourced ground-truth reports (flooding, waterlogging, "
                "power outages, blocked roads, etc.) reported by nearby users. Use this "
                "when asked about real/current on-the-ground conditions, which official "
                "data can lag behind during fast-moving events."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "radius_km": {"type": "number", "description": "Search radius in km, default 25"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_farmer_advisory",
            "description": (
                "Get farming-specific advice (pesticide/fertilizer spraying window, "
                "irrigation need, livestock heat stress) derived from the forecast. "
                "Use when the user asks about farming, crops, spraying, irrigation, or livestock."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {"type": "string"},
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                },
                "required": [],
            },
        },
    },
]


async def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Dispatch a tool call by name and return a JSON-serializable result."""
    lat = arguments.get("lat")
    lon = arguments.get("lon")
    location_name = arguments.get("location_name")

    if name == "get_current_weather":
        result = await weather_service.get_current_weather(lat=lat, lon=lon, name=location_name)
        return result.model_dump()

    if name == "get_forecast":
        days = arguments.get("days", 5)
        result = await forecast_service.get_forecast(
            lat=lat, lon=lon, name=location_name, days=days
        )
        payload = result.model_dump()
        # Trim hourly for token efficiency in the LLM context
        payload["hourly"] = payload["hourly"][:12]
        return payload

    if name == "get_alerts":
        result = await alert_service.get_alerts(lat=lat, lon=lon, name=location_name)
        return result.model_dump()

    if name == "analyze_weather":
        result = await analysis_service.analyze(lat=lat, lon=lon, name=location_name)
        return result.model_dump()

    if name == "geocode_location":
        results = await location_service.geocode(arguments["name"])
        return {"matches": [r.model_dump() for r in results]}

    if name == "search_meteorology_knowledge":
        entries = knowledge_base.search(arguments["query"])
        return {"results": entries}

    if name == "get_community_reports":
        if lat is None or lon is None:
            return {"error": "lat/lon required for community reports"}
        radius_km = arguments.get("radius_km", 25)
        reports = community_service.get_nearby(lat, lon, radius_km=radius_km)
        return {"reports": [r.model_dump() for r in reports]}

    if name == "get_farmer_advisory":
        result = await farmer_advisory_service.get_farmer_advisory(
            lat=lat, lon=lon, name=location_name
        )
        return result.model_dump()

    return {"error": f"Unknown tool: {name}"}
