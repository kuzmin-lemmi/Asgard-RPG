from aiogram import F, Router
from aiogram.types import Message

import texts

router = Router(name="fallback")

@router.message(F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    await message.answer(texts.UNKNOWN_COMMAND)

@router.message(F.text)
async def any_text(message: Message) -> None:
    await message.answer(texts.ANY_TEXT)

@router.message()
async def any_other(message: Message) -> None:
    await message.answer(texts.ANY_OTHER)
