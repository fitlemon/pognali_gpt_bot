import asyncio
import logging
from environs import Env

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand


from handlers import router
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter

register_adapter(dict, Json)
# import env config file
env = Env()
env.read_env()


async def main():
    bot = Bot(token=env("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
