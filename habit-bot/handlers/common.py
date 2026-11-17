from aiogram import F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import keyboards
import texts

router = Router(name="common")

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = html.quote(message.from_user.first_name)
    await message.answer(
        texts.GREETING.format(name=name),
        reply_markup=keyboards.main_keyboard(),
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(texts.MENU, reply_markup=keyboards.main_keyboard())

@router.message(Command("help"))
@router.message(F.text == texts.BTN_HELP)
async def cmd_help(message: Message) -> None:
    await message.answer(texts.HELP)

@router.message(F.text.lower().in_({"привет", "здравствуй"}))
async def greeting(message: Message) -> None:
    await message.answer(texts.GREETING_SHORT)
