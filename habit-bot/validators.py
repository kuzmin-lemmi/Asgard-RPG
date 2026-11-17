"""Проверка ответов в диалоге создания привычки."""

MAX_NAME_LENGTH = 50

def parse_frequency(text: str) -> int | None:
    try:
        number = int(text)
    except ValueError:
        return None

    if number < 1 or number > 7:
        return None
    return number

def clean_name(text: str) -> str | None:
    name = text.strip()
    if not name or len(name) > MAX_NAME_LENGTH:
        return None
    return name

def parse_time(text: str) -> str | None:
    parts = text.split(":")
    if len(parts) != 2:
        return None

    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        return None

    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return None
    return f"{hours:02d}:{minutes:02d}"
