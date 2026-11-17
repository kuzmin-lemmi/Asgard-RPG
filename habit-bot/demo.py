"""Демо-версия для презентации курса: лимит привычек и одно сообщение на 3-й день.

В коде курса этого модуля нет.
"""
import logging
from datetime import date, datetime, timedelta
from typing import Any, Awaitable, Callable

import aiosqlite
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, User

import clock
import database
import texts

MAX_HABITS = 3
NUDGE_AFTER_DAYS = 3
NUDGE_TIME = "12:00"

logger = logging.getLogger(__name__)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS demo_users (
    user_id    INTEGER PRIMARY KEY,
    first_seen TEXT    NOT NULL,
    nudged     INTEGER NOT NULL DEFAULT 0
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(database.DB_PATH) as db:
        await db.executescript(CREATE_TABLE)
        await db.commit()


async def remember_user(user_id: int, day: date) -> None:
    async with aiosqlite.connect(database.DB_PATH) as db:
        await db.execute(
            "INSERT INTO demo_users (user_id, first_seen) VALUES (?, ?) "
            "ON CONFLICT DO NOTHING",
            (user_id, day.isoformat()),
        )
        await db.commit()


class TrackUsers(BaseMiddleware):
    """Запоминает день, когда человек впервые написал боту."""

    def __init__(self) -> None:
        self.known: set[int] = set()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is not None and user.id not in self.known:
            try:
                await remember_user(user.id, clock.today())
                self.known.add(user.id)
            except Exception:
                logger.exception("Не удалось запомнить пользователя %s", user.id)
        return await handler(event, data)


async def limit_reached(user_id: int) -> bool:
    return len(await database.get_habits(user_id)) >= MAX_HABITS


async def users_to_nudge(day: date) -> list[int]:
    border = (day - timedelta(days=NUDGE_AFTER_DAYS)).isoformat()
    async with aiosqlite.connect(database.DB_PATH) as db:
        cursor = await db.execute(
            "SELECT d.user_id FROM demo_users d "
            "WHERE d.nudged = 0 AND d.first_seen <= ? "
            "AND EXISTS (SELECT 1 FROM habits h WHERE h.user_id = d.user_id)",
            (border,),
        )
        rows = await cursor.fetchall()
    return [row[0] for row in rows]


async def mark_nudged(user_id: int) -> bool:
    async with aiosqlite.connect(database.DB_PATH) as db:
        cursor = await db.execute(
            "UPDATE demo_users SET nudged = 1 WHERE user_id = ? AND nudged = 0",
            (user_id,),
        )
        await db.commit()
    return cursor.rowcount == 1


async def send_nudges(bot: Bot, now: datetime, deliver) -> None:
    """Одно сообщение про курс тем, кто пользуется ботом 3 дня. Вызывается из send_due()."""
    from reminders import is_due

    if not is_due(NUDGE_TIME, now):
        return
    for user_id in await users_to_nudge(now.date()):
        if await mark_nudged(user_id):
            await deliver(bot, user_id, texts.DEMO_NUDGE)
