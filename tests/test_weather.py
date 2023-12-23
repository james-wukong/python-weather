# import pytest
from src.api.weather import Weather

def test_weather_fetch_weather_data():
    weather = Weather()
    data = weather.fetch_weather_data()
    assert data[0] == 200
    assert data[1] != False

