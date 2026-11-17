"""Напоминания: бот сам пишет пользователям по расписанию."""
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, html
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup

import clock
import database
import demo
import keyboards
import texts
from handlers.habits import build_morning_text

MORNING_TIME = "07:30"
CATCH_UP = timedelta(minutes=15)

logger = logging.getLogger(__name__)

def is_due(remind_time: str, now: datetime) -> bool:
    hours, minutes = remind_time.split(":")
    planned = now.replace(
        hour=int(hours), minute=int(minutes), second=0, microsecond=0
    )
    return planned <= now < planned + CATCH_UP

async def deliver(
    bot: Bot,
    user_id: int,
    text: str,
    markup: InlineKeyboardMarkup | None = None,
) -> None:
    try:
        await bot.send_message(user_id, text, reply_markup=markup)
    except TelegramForbiddenError:
        logger.warning("Пользователь %s заблокировал бота", user_id)

async def send_due(bot: Bot, now: datetime) -> None:
    day = now.date()

    await demo.send_nudges(bot, now, deliver)

    if is_due(MORNING_TIME, now):
        for user_id in await database.get_user_ids():
            if await database.mark_sent(user_id, "morning", day):
                text = await build_morning_text(user_id, day)
                await deliver(bot, user_id, text)

    for habit in await database.get_all_habits():
        if not is_due(habit["remind_time"], now):
            continue

        user_id = habit["user_id"]
        done_ids = await database.get_done_ids(user_id, day)
        if habit["id"] in done_ids:
            continue

        if await database.mark_sent(user_id, f"habit_{habit['id']}", day):
            await deliver(
                bot,
                user_id,
                texts.REMINDER.format(name=html.quote(habit["name"])),
                keyboards.reminder_keyboard(habit["id"], habit["name"]),
            )

async def reminder_loop(bot: Bot) -> None:
    while True:
        try:
            await send_due(bot, clock.now())
        except Exception:
            logger.exception("Сбой в цикле напоминаний, повтор через минуту")
        await asyncio.sleep(60 - clock.now().second)
