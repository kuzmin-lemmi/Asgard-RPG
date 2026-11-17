"""Ошибка в любом хэндлере: ответ пользователю и подробная запись в журнал."""
import logging

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent

import texts

router = Router(name="errors")
logger = logging.getLogger(__name__)

@router.errors()
async def on_error(event: ErrorEvent) -> None:
    update = event.update
    if update.message is not None:
        user_id = update.message.from_user.id
        what = update.message.text
    elif update.callback_query is not None:
        user_id = update.callback_query.from_user.id
        what = update.callback_query.data
    else:
        user_id = None
        what = None

    logger.error(
        "Ошибка в хэндлере: пользователь %s, событие %r",
        user_id,
        what,
        exc_info=event.exception,
    )

    try:
        if update.message is not None:
            await update.message.answer(texts.ERROR)
        elif update.callback_query is not None:
            await update.callback_query.answer(texts.ERROR, show_alert=True)
    except TelegramAPIError:
        logger.warning("Не удалось сообщить пользователю %s об ошибке", user_id)
