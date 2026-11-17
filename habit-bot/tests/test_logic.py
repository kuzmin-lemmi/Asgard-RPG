from datetime import datetime

from reminders import is_due
from weather import describe_weather

def test_morning_on_time():
    assert is_due("07:30", datetime(2026, 11, 2, 7, 30))

def test_too_late():
    assert not is_due("07:30", datetime(2026, 11, 2, 7, 45))

def test_weather_without_current():
    assert describe_weather({"generationtime_ms": 0.2}) is None

def test_weather_zero_without_sign():
    data = {"current": {"temperature_2m": -0.4, "weather_code": 3}}
    assert describe_weather(data) == "0, пасмурно"
