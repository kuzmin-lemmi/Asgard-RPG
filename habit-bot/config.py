"""Настройки проекта: чтение и проверка переменных окружения."""
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "BOT_TOKEN не найден. Проверьте, что файл .env лежит "
        "рядом с bot.py и содержит строку BOT_TOKEN=..."
    )
