import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation

import bot_profile
import database
import demo
import reminders
from config import TOKEN
from handlers import add, common, errors, fallback, guard, habits
from handlers import demo as demo_handlers

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

async def main() -> None:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    await database.init_db()
    await demo.init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(events_isolation=SimpleEventIsolation())

    dp.update.outer_middleware(demo.TrackUsers())

    dp.include_router(errors.router)
    dp.include_router(guard.router)
    dp.include_router(common.router)
    dp.include_router(habits.router)
    dp.include_router(add.router)
    dp.include_router(demo_handlers.router)
    dp.include_router(fallback.router)

    await bot_profile.setup_profile(bot)
    reminder_task = asyncio.create_task(reminders.reminder_loop(bot))

    print("ПривычкаБот запущен. Ctrl+C для остановки.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("ПривычкаБот остановлен.")
