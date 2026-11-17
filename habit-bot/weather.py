"""Погода от Open-Meteo: запросы и разбор ответов."""
import logging

import aiohttp

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = aiohttp.ClientTimeout(total=5)

logger = logging.getLogger(__name__)

WEATHER_CODES = {
    0: "ясно",
    1: "в основном ясно",
    2: "переменная облачность",
    3: "пасмурно",
    45: "туман",
    48: "туман с изморозью",
    51: "слабая морось",
    53: "морось",
    55: "сильная морось",
    61: "слабый дождь",
    63: "дождь",
    65: "сильный дождь",
    71: "слабый снег",
    73: "снег",
    75: "сильный снег",
    80: "ливень",
    95: "гроза",
}

async def get_json(url: str, params: dict) -> dict:
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

def parse_city(data: dict) -> tuple[str, float, float] | None:
    results = data.get("results")
    if not results:
        return None

    place = results[0]
    name = place.get("name")
    latitude = place.get("latitude")
    longitude = place.get("longitude")
    if name is None or latitude is None or longitude is None:
        return None
    return name, latitude, longitude

def describe_weather(data: dict) -> str | None:
    current = data.get("current")
    if not current:
        return None

    temperature = current.get("temperature_2m")
    code = current.get("weather_code")
    if temperature is None or code is None:
        return None

    degrees = round(temperature)
    if degrees == 0:
        sign = "0"
    else:
        sign = f"{degrees:+d}"
    text = WEATHER_CODES.get(code, "без описания")
    return f"{sign}, {text}"

async def find_city(city: str) -> tuple[str, float, float] | None:
    params = {"name": city, "count": 1, "language": "ru"}
    try:
        data = await get_json(GEO_URL, params)
    except (aiohttp.ClientError, TimeoutError) as error:
        name = type(error).__name__
        logger.warning("Геокодер недоступен для %s: %s", city, name)
        return None

    place = parse_city(data)
    if place is None:
        logger.info("Город не найден: %s", city)
    return place

async def get_weather(latitude: float, longitude: float) -> str | None:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
    }
    try:
        data = await get_json(FORECAST_URL, params)
    except (aiohttp.ClientError, TimeoutError) as error:
        name = type(error).__name__
        logger.warning("Погода недоступна: %s", name)
        return None

    text = describe_weather(data)
    if text is None:
        logger.warning("Неожиданный ответ прогноза")
    return text
