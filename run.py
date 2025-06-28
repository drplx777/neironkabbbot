import os
import asyncio
from aiogram import Bot, Dispatcher
import logging
import threading
from core.config import get

from app.admin import admin
from app.user import user
from app.database.models import async_main

#логгер(потом удалить)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    env_bot_token = get('/neiro/ENV_BOT_TOKEN')
    bot = Bot(token=env_bot_token)
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    logger.info("Stating bot")
    await async_main()
    logger.info("database models checked")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass