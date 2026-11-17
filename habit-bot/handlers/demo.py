"""Демо-версия: команда «Как устроен бот». В коде курса этого файла нет."""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import LinkPreviewOptions, Message

import texts

router = Router(name="demo")


@router.message(Command("inside"))
@router.message(F.text == texts.BTN_INSIDE)
async def cmd_inside(message: Message) -> None:
    await message.answer(
        texts.INSIDE,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
