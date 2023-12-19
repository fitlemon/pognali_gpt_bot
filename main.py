import asyncio
import logging


import loader
from handlers import router
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter

register_adapter(dict, Json)
# import env config file


async def main():
    bot = loader.bot
    dp = loader.dp
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
