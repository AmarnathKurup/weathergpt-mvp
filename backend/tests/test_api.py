import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"

def test_current_weather_endpoint():
    res = client.get("/api/v1/weather/current?location=700001")
    assert res.status_code == 200
    data = res.json()
    assert "temperature" in data
    assert data["location"]["pincode"] == "700001"

def test_chat_endpoint():
    payload = {
        "query": "Will it rain when I leave college?",
        "location": "700001",
        "occupation": "student",
        "language": "en"
    }
    res = client.post("/api/v1/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert "why_explainability" in data

def test_pincode_endpoint():
    res = client.get("/api/v1/location/pincode/700001")
    assert res.status_code == 200
    assert res.json()["pincode"] == "700001"
