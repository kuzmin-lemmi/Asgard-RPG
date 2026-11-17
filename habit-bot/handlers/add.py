from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import demo
import keyboards
import texts
import validators
from states import AddHabit

router = Router(name="add")

@router.message(Command("add"))
@router.message(F.text == texts.BTN_ADD)
async def cmd_add(message: Message, state: FSMContext) -> None:
    if await demo.limit_reached(message.from_user.id):
        await message.answer(texts.DEMO_LIMIT)
        return

    await state.set_state(AddHabit.waiting_for_name)
    await message.answer(
        texts.ASK_NAME,
        reply_markup=keyboards.step_keyboard(),
    )

@router.message(AddHabit.waiting_for_name, F.text)
async def habit_name_entered(message: Message, state: FSMContext) -> None:
    name = validators.clean_name(message.text)
    if name is None:
        await message.answer(
            texts.ERR_NAME,
            reply_markup=keyboards.step_keyboard(),
        )
        return

    await state.update_data(name=name)
    await state.set_state(AddHabit.waiting_for_frequency)
    await message.answer(
        texts.ASK_FREQUENCY,
        reply_markup=keyboards.step_keyboard("name"),
    )

@router.message(AddHabit.waiting_for_frequency, F.text)
async def habit_frequency_entered(message: Message, state: FSMContext) -> None:
    frequency = validators.parse_frequency(message.text)
    if frequency is None:
        await message.answer(
            texts.ERR_FREQUENCY,
            reply_markup=keyboards.step_keyboard("name"),
        )
        return

    await state.update_data(frequency=frequency)
    await state.set_state(AddHabit.waiting_for_time)
    await message.answer(
        texts.ASK_TIME,
        reply_markup=keyboards.step_keyboard("frequency"),
    )

@router.message(AddHabit.waiting_for_time, F.text)
async def habit_time_entered(message: Message, state: FSMContext) -> None:
    time = validators.parse_time(message.text)
    if time is None:
        await message.answer(
            texts.ERR_TIME,
            reply_markup=keyboards.step_keyboard("frequency"),
        )
        return

    await state.update_data(time=time)
    data = await state.get_data()
    await state.set_state(AddHabit.waiting_for_confirm)

    await message.answer(
        texts.CONFIRM.format(
            name=html.quote(data["name"]),
            frequency=data["frequency"],
            time=html.quote(data["time"]),
        ),
        reply_markup=keyboards.confirm_keyboard(),
    )

@router.message(AddHabit.waiting_for_confirm)
async def confirm_text(message: Message) -> None:
    await message.answer(
        texts.CONFIRM_USE_BUTTONS,
        reply_markup=keyboards.confirm_keyboard(),
    )
