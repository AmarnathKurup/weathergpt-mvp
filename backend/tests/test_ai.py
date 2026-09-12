import pytest
from backend.app.ai.intent_classifier import intent_classifier
from backend.app.alerts.risk_engine import risk_engine
from backend.app.schemas.weather import WeatherSnapshot, LocationInfo
from backend.app.services.weathergpt_service import weathergpt_service
from backend.app.schemas.chat import ChatRequest

def test_intent_classification():
    assert intent_classifier.classify("Will it rain this evening?") == "RAIN_QUERY"
    assert intent_classifier.classify("Is there a cyclone warning?") == "WARNING_QUERY"
    assert intent_classifier.classify("What is the crop advisory for paddy?") == "AGRICULTURE_ADVISORY"

def test_risk_engine():
    dummy_snapshot = WeatherSnapshot(
        location=LocationInfo(name="Test"),
        rain_probability=85.0,
        rain=12.0,
        weather_code=95
    )
    events, actions = risk_engine.evaluate_risk(dummy_snapshot)
    assert "HIGH_RAIN_PROBABILITY" in events or "EVENING_RAIN_LIKELY" in events
    assert "THUNDERSTORM_LIGHTNING_RISK" in events
    assert len(actions) > 0

@pytest.mark.asyncio
async def test_weathergpt_pipeline():
    req = ChatRequest(
        query="Will it rain today?",
        location="700001",
        occupation="student",
        language="en"
    )
    res = await weathergpt_service.process_chat_query(req)
    assert res is not None
    assert res.intent == "RAIN_QUERY"
    assert res.answer is not None
    assert res.why_explainability is not None
    assert res.why_explainability.temperature is not None
