"""Время бота: один часовой пояс для всех его часов."""
from datetime import date, datetime
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Europe/Moscow")

def now() -> datetime:
    return datetime.now(TIMEZONE)

def today() -> date:
    return now().date()
