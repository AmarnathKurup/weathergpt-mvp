import pytest
from backend.app.services.weather_service import weather_service

@pytest.mark.asyncio
async def test_get_current_weather():
    snapshot = await weather_service.get_current_weather(location_query="700001")
    assert snapshot is not None
    assert snapshot.temperature is not None
    assert snapshot.location.pincode == "700001"
    assert snapshot.weather_desc is not None

@pytest.mark.asyncio
async def test_get_weather_forecast():
    forecast = await weather_service.get_forecast(location_query="Delhi")
    assert forecast is not None
    assert len(forecast.hourly) > 0
    assert len(forecast.daily) > 0
