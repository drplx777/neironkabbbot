import os
import asyncio
from aiogram import Bot, Dispatcher
import logging
import threading
from core.config import config_loader

from app.admin import admin
from app.user import user
from app.database.models import async_main

#логгер(потом удалить)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def start_etcd_watcher():
    try:
        config_loader.watch_changes()
    except Exception as e:
        logger.error(f"ETCD watcher thread failed: {str(e)}")



async def main():
    config_loader.initialize()
    watcher_thread = threading.Thread(
        target=start_etcd_watcher,
        name='etcd_watcher',
        daemon=True
    )
    watcher_thread.start()
    
    bot = Bot(token=config_loader.get('/config/bot_token'))
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