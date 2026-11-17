from aiogram import F, Router, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database
import demo
import keyboards
import texts
from states import AddHabit

router = Router(name="guard")

BACK_STEPS = {
    "add_back_name": (AddHabit.waiting_for_name, texts.ASK_NAME, None),
    "add_back_frequency": (AddHabit.waiting_for_frequency, texts.ASK_FREQUENCY, "name"),
    "add_back_time": (AddHabit.waiting_for_time, texts.ASK_TIME, "frequency"),
}

@router.message(StateFilter(AddHabit), Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.ADD_CANCELLED)

@router.message(Command("cancel"))
async def cmd_cancel_nothing(message: Message) -> None:
    await message.answer(texts.NOTHING_TO_CANCEL)

@router.message(StateFilter(AddHabit), F.text.startswith("/"))
@router.message(StateFilter(AddHabit), F.text.in_(texts.MENU_BUTTONS))
async def command_during_dialog(message: Message) -> None:
    await message.answer(texts.COMMAND_IN_DIALOG)

@router.callback_query(StateFilter(AddHabit), F.data == "add_cancel")
async def cancel_button(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if not isinstance(callback.message, Message):
        await callback.answer(texts.ADD_CANCELLED, show_alert=True)
        return

    await callback.message.edit_text(texts.ADD_CANCELLED)
    await callback.answer()

@router.callback_query(AddHabit.waiting_for_confirm, F.data == "add_save")
async def save_button(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    if await demo.limit_reached(callback.from_user.id):
        await state.clear()
        if isinstance(callback.message, Message):
            await callback.message.edit_text(texts.DEMO_LIMIT)
        await callback.answer()
        return

    habit = await database.add_habit(
        user_id=callback.from_user.id,
        name=data["name"],
        frequency=data["frequency"],
        remind_time=data["time"],
    )
    await state.clear()

    if not isinstance(callback.message, Message):
        await callback.answer(
            texts.HABIT_CREATED.format(name=habit["name"]),
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        texts.HABIT_CREATED.format(name=html.quote(habit["name"]))
    )
    await callback.answer()

@router.callback_query(StateFilter(AddHabit), F.data.in_(BACK_STEPS))
async def back_button(callback: CallbackQuery, state: FSMContext) -> None:
    step, question, back_to = BACK_STEPS[callback.data]
    await state.set_state(step)

    if not isinstance(callback.message, Message):
        await callback.answer(question, show_alert=True)
        return

    await callback.message.edit_text(
        question,
        reply_markup=keyboards.step_keyboard(back_to),
    )
    await callback.answer()

@router.callback_query(F.data.startswith("add_"))
async def dialog_button_late(callback: CallbackQuery) -> None:
    await callback.answer(texts.CB_DIALOG_OVER, show_alert=True)
