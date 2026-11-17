from datetime import date, timedelta

from aiogram import F, Router, html
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

import clock
import database
import keyboards
import texts
import weather
from streak import count_streak

router = Router(name="habits")

STATS_DAYS = 30

async def build_today_screen(
    user_id: int,
    day: date,
    page: int,
) -> tuple[str, InlineKeyboardMarkup | None]:
    habits = await database.get_habits(user_id)
    done_ids = await database.get_done_ids(user_id, day)

    text = texts.build_today_text(
        day=day,
        done=await database.count_done(user_id, day),
        total=len(habits),
    )

    markup = keyboards.habits_keyboard(
        habits,
        done_ids=done_ids,
        page=page,
    )

    return text, markup

async def edit_today_message(
    message: Message,
    user_id: int,
    day: date,
    page: int,
) -> None:
    text, markup = await build_today_screen(user_id, day, page)

    try:
        await message.edit_text(
            text,
            reply_markup=markup,
        )
    except TelegramBadRequest as error:
        if "message is not modified" not in str(error):
            raise

@router.message(Command("today"))
@router.message(F.text == texts.BTN_TODAY)
async def cmd_today(message: Message) -> None:
    day = clock.today()
    text, markup = await build_today_screen(
        message.from_user.id,
        day,
        page=0,
    )

    await message.answer(
        text,
        reply_markup=markup,
    )

@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    day = clock.today()
    text, markup = await build_today_screen(
        message.from_user.id,
        day,
        page=0,
    )

    await message.answer(
        text,
        reply_markup=markup,
    )

@router.message(Command("stats"))
@router.message(F.text == texts.BTN_STATS)
async def cmd_stats(message: Message) -> None:
    user_id = message.from_user.id
    today = clock.today()
    since = today - timedelta(days=STATS_DAYS - 1)
    monday = today - timedelta(days=today.weekday())

    rows = await database.get_stats(user_id, since, today)
    if not rows:
        await message.answer(texts.EMPTY_TODAY)
        return

    week_done = {}
    for row in await database.get_stats(user_id, monday, today):
        week_done[row["id"]] = row["done"]

    lines = [texts.STATS_TITLE.format(days=STATS_DAYS)]
    for row in rows:
        days = await database.get_mark_days(user_id, row["id"], today)
        week = week_done[row["id"]]
        lines.append(
            texts.STATS_LINE.format(
                name=html.quote(row["name"]),
                done=row["done"],
                streak=count_streak(days, today),
                week=week,
                goal=row["frequency"],
                mark=" ✅" if week >= row["frequency"] else "",
            )
        )

    await message.answer("\n".join(lines))

@router.message(Command("city"))
async def cmd_city(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer(texts.CITY_USAGE)
        return

    query = command.args.strip()
    place = await weather.find_city(query)
    if place is None:
        await message.answer(
            texts.CITY_NOT_FOUND.format(city=html.quote(query))
        )
        return

    city, latitude, longitude = place
    await database.set_city(message.from_user.id, city, latitude, longitude)
    await message.answer(texts.CITY_SAVED.format(city=html.quote(city)))

async def build_morning_text(user_id: int, day: date) -> str:
    place = await database.get_city(user_id)
    if place is None:
        weather_line = texts.NO_CITY
    else:
        forecast = await weather.get_weather(
            place["latitude"], place["longitude"]
        )
        if forecast is None:
            weather_line = texts.NO_WEATHER
        else:
            weather_line = texts.WEATHER_LINE.format(
                city=html.quote(place["city"]),
                weather=forecast,
            )

    habits = await database.get_habits(user_id)
    done_ids = await database.get_done_ids(user_id, day)
    if not habits:
        habits_text = texts.EMPTY_TODAY
    else:
        lines = []
        for habit in habits:
            mark = "✅" if habit["id"] in done_ids else "⬜"
            lines.append(f"{mark} {html.quote(habit['name'])}")
        habits_text = "\n".join(lines)

    return texts.MORNING.format(weather=weather_line, habits=habits_text)

@router.message(Command("morning"))
@router.message(F.text == texts.BTN_MORNING)
async def cmd_morning(message: Message) -> None:
    text = await build_morning_text(message.from_user.id, clock.today())
    await message.answer(text)

@router.callback_query(F.data.startswith("page_"))
async def switch_page(callback: CallbackQuery) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer(
            texts.CB_MESSAGE_UNAVAILABLE,
            show_alert=True,
        )
        return

    page_text = callback.data.removeprefix("page_")

    if not page_text.isdigit():
        await callback.answer(
            texts.CB_OLD_BUTTON,
            show_alert=True,
        )
        return

    page = int(page_text)
    day = clock.today()

    await edit_today_message(
        callback.message,
        user_id=callback.from_user.id,
        day=day,
        page=page,
    )

    await callback.answer()

@router.callback_query(F.data.startswith("toggle_"))
async def toggle_habit_from_list(
    callback: CallbackQuery,
) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer(
            texts.CB_MESSAGE_UNAVAILABLE,
            show_alert=True,
        )
        return

    payload = callback.data.removeprefix("toggle_")
    parts = payload.split("_")

    if (
        len(parts) != 2
        or not parts[0].isdigit()
        or not parts[1].isdigit()
    ):
        await callback.answer(
            texts.CB_OLD_BUTTON,
            show_alert=True,
        )
        return

    habit_id = int(parts[0])
    page = int(parts[1])

    habit = await database.get_habit(callback.from_user.id, habit_id)

    if habit is None:
        await callback.answer(
            texts.CB_HABIT_GONE,
            show_alert=True,
        )
        return

    day = clock.today()
    marked = await database.toggle_mark(habit_id, day)

    await edit_today_message(
        callback.message,
        user_id=callback.from_user.id,
        day=day,
        page=page,
    )

    if marked:
        await callback.answer(texts.CB_MARKED)
    else:
        await callback.answer(texts.CB_UNDONE)

@router.callback_query()
async def old_callback(callback: CallbackQuery) -> None:
    await callback.answer(
        texts.CB_OLD_BUTTON,
        show_alert=True,
    )
