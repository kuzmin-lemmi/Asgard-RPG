"""Состояния диалогов ПривычкаБота."""

from aiogram.fsm.state import State, StatesGroup

class AddHabit(StatesGroup):
    waiting_for_name = State()
    waiting_for_frequency = State()
    waiting_for_time = State()
    waiting_for_confirm = State()
