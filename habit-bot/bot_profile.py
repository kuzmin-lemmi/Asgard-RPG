"""Демо-версия: меню команд и описание бота, которые видит человек в Telegram.

Вызывается при каждом запуске бота. Значения берутся из texts.py,
поэтому правки, сделанные вручную в BotFather, при запуске перезапишутся.
"""
import logging

from aiogram import Bot
from aiogram.types import BotCommand, MenuButtonCommands

import texts

logger = logging.getLogger(__name__)


async def setup_profile(bot: Bot) -> None:
    try:
        await bot.set_my_commands(
            [BotCommand(command=name, description=text) for name, text in texts.BOT_COMMANDS.items()]
        )
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        await bot.set_my_short_description(short_description=texts.BOT_SHORT_DESCRIPTION)
        await bot.set_my_description(description=texts.BOT_DESCRIPTION)
    except Exception:
        # профиль — не главное: бот должен работать, даже если Telegram не принял описание
        logger.exception("Не удалось обновить меню и описание бота")
