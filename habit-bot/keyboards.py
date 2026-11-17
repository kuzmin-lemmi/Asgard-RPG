from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import texts

PAGE_SIZE = 3

def total_pages(total_items: int, page_size: int) -> int:
    pages = (total_items + page_size - 1) // page_size
    return max(1, pages)

def safe_page(page: int, pages: int) -> int:
    return max(0, min(page, pages - 1))

def habits_keyboard(
    habits: list[dict],
    done_ids: set[int],
    page: int,
) -> InlineKeyboardMarkup | None:
    if not habits:
        return None

    pages = total_pages(len(habits), PAGE_SIZE)
    page = safe_page(page, pages)

    start = page * PAGE_SIZE
    chunk = habits[start:start + PAGE_SIZE]

    builder = InlineKeyboardBuilder()

    for habit in chunk:
        mark = "✅" if habit["id"] in done_ids else "⬜"

        builder.button(
            text=f"{mark} {habit['name']}",
            callback_data=f"toggle_{habit['id']}_{page}",
        )

    builder.adjust(1)

    if page == 0 and pages > 1:
        builder.row(
            InlineKeyboardButton(
                text="➡️",
                callback_data="page_1",
            )
        )

    elif page == pages - 1 and pages > 1:
        builder.row(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"page_{page - 1}",
            )
        )

    elif pages > 1:
        builder.row(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"page_{page - 1}",
            ),
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"page_{page + 1}",
            ),
        )

    return builder.as_markup()

def step_keyboard(back_to: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if back_to is not None:
        builder.button(text="◀️ Назад", callback_data=f"add_back_{back_to}")
    builder.button(text="✖️ Отмена", callback_data="add_cancel")
    builder.adjust(2)
    return builder.as_markup()

def confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Сохранить", callback_data="add_save")
    builder.button(text="◀️ Назад", callback_data="add_back_time")
    builder.button(text="✖️ Отмена", callback_data="add_cancel")
    builder.adjust(1, 2)
    return builder.as_markup()

def reminder_keyboard(habit_id: int, name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"⬜ {name}", callback_data=f"toggle_{habit_id}_0")
    return builder.as_markup()

def main_keyboard() -> ReplyKeyboardMarkup:
    """Демо-версия: постоянные кнопки внизу экрана."""
    builder = ReplyKeyboardBuilder()
    for text in (texts.BTN_TODAY, texts.BTN_ADD, texts.BTN_STATS, texts.BTN_MORNING, texts.BTN_HELP, texts.BTN_INSIDE):
        builder.button(text=text)
    builder.adjust(2, 2, 2)
    return builder.as_markup(
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder=texts.KEYBOARD_HINT,
    )
