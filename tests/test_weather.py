# src/tests/test_weather.py
import pytest
from weather_app import fetch_weather_by_city, WeatherError

class DummyResp:
    status_code = 200
    def json(self):
        return {"name":"TestCity","main":{"temp":25,"feels_like":24,"humidity":40},"weather":[{"description":"clear sky"}],"wind":{"speed":1.5}}

def test_fetch_weather_success(monkeypatch):
    monkeypatch.setattr("weather_node.requests.get", lambda *a, **k: DummyResp())
    data = fetch_weather_by_city("TestCity")
    assert data["city"] == "TestCity"
    assert "temp" in data

def test_fetch_weather_no_key(monkeypatch):
    # temporarily unset key
    import weather_node, config
    old = config.settings.OPENWEATHER_API_KEY
    config.settings.OPENWEATHER_API_KEY = ""
    with pytest.raises(WeatherError):
        fetch_weather_by_city("Nowhere")
    config.settings.OPENWEATHER_API_KEY = old
