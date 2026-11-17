"""Хранилище ПривычкаБота в базе SQLite."""
from datetime import date

import aiosqlite

DB_PATH = "habits.db"

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS habits (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    frequency   INTEGER NOT NULL,
    remind_time TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS marks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id    INTEGER NOT NULL,
    marked_date TEXT    NOT NULL,
    UNIQUE (habit_id, marked_date)
);

CREATE TABLE IF NOT EXISTS users (
    user_id   INTEGER PRIMARY KEY,
    city      TEXT    NOT NULL,
    latitude  REAL    NOT NULL,
    longitude REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS sent (
    user_id INTEGER NOT NULL,
    kind    TEXT    NOT NULL,
    day     TEXT    NOT NULL,
    UNIQUE (user_id, kind, day)
);
"""

async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(CREATE_TABLES)
        await db.commit()

async def add_habit(
    user_id: int, name: str, frequency: int, remind_time: str
) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO habits (user_id, name, frequency, remind_time) "
            "VALUES (?, ?, ?, ?)",
            (user_id, name, frequency, remind_time),
        )
        await db.commit()
    return {
        "id": cursor.lastrowid,
        "name": name,
        "frequency": frequency,
        "remind_time": remind_time,
    }

async def get_habits(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, name, frequency, remind_time FROM habits "
            "WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]

async def get_habit(user_id: int, habit_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, name, frequency, remind_time FROM habits "
            "WHERE id = ? AND user_id = ?",
            (habit_id, user_id),
        )
        row = await cursor.fetchone()
    if row is None:
        return None
    return dict(row)

async def toggle_mark(habit_id: int, day: date) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM marks WHERE habit_id = ? AND marked_date = ?",
            (habit_id, day.isoformat()),
        )
        if cursor.rowcount > 0:
            await db.commit()
            return False

        await db.execute(
            "INSERT INTO marks (habit_id, marked_date) VALUES (?, ?)",
            (habit_id, day.isoformat()),
        )
        await db.commit()
        return True

async def count_done(user_id: int, day: date) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) "
            "FROM marks m "
            "JOIN habits h ON h.id = m.habit_id "
            "WHERE h.user_id = ? AND m.marked_date = ?",
            (user_id, day.isoformat()),
        )
        row = await cursor.fetchone()
    return row[0]

async def get_stats(user_id: int, since: date, until: date) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT h.id, h.name, h.frequency, COUNT(m.id) AS done "
            "FROM habits h "
            "LEFT JOIN marks m ON m.habit_id = h.id "
            "AND m.marked_date >= ? AND m.marked_date <= ? "
            "WHERE h.user_id = ? "
            "GROUP BY h.id, h.name, h.frequency "
            "ORDER BY done DESC, h.id",
            (since.isoformat(), until.isoformat(), user_id),
        )
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]

async def get_mark_days(user_id: int, habit_id: int, today: date) -> list[date]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT m.marked_date "
            "FROM marks m "
            "JOIN habits h ON h.id = m.habit_id "
            "WHERE m.habit_id = ? AND h.user_id = ? AND m.marked_date <= ? "
            "ORDER BY m.marked_date DESC",
            (habit_id, user_id, today.isoformat()),
        )
        rows = await cursor.fetchall()

    days = []
    for row in rows:
        days.append(date.fromisoformat(row[0]))
    return days

async def get_done_ids(user_id: int, day: date) -> set[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT m.habit_id "
            "FROM marks m "
            "JOIN habits h ON h.id = m.habit_id "
            "WHERE h.user_id = ? AND m.marked_date = ?",
            (user_id, day.isoformat()),
        )
        rows = await cursor.fetchall()

    done_ids = set()
    for row in rows:
        done_ids.add(row[0])
    return done_ids

async def set_city(
    user_id: int, city: str, latitude: float, longitude: float
) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (user_id, city, latitude, longitude) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT (user_id) DO UPDATE SET "
            "city = excluded.city, "
            "latitude = excluded.latitude, "
            "longitude = excluded.longitude",
            (user_id, city, latitude, longitude),
        )
        await db.commit()

async def get_city(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT city, latitude, longitude FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
    if row is None:
        return None
    return dict(row)

async def mark_sent(user_id: int, kind: str, day: date) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO sent (user_id, kind, day) VALUES (?, ?, ?) "
            "ON CONFLICT DO NOTHING",
            (user_id, kind, day.isoformat()),
        )
        await db.commit()
    return cursor.rowcount == 1

async def get_all_habits() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, user_id, name, remind_time FROM habits ORDER BY id"
        )
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]

async def get_user_ids() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT DISTINCT user_id FROM habits ORDER BY user_id"
        )
        rows = await cursor.fetchall()

    user_ids = []
    for row in rows:
        user_ids.append(row[0])
    return user_ids
