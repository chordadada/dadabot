import logging
from config.settings import config
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers import commands, messages
from inline import router as inline_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.bot_instance import set_bot_instance

# Настройка логирования
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)

# Красивый вывод в консоль при запуске
print("""
███████╗███████╗██████╗ ██████╗  ██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗
█████╗  █████╗  ██║  ██║██║  ██║██║   ██║
██╔══╝  ██╔══╝  ██║  ██║██║  ██║██║   ██║
██║     ███████╗██████╔╝██████╔╝╚██████╔╝
╚═╝     ╚══════╝╚═════╝ ╚═════╝  ╚═════╝ 
Quantum Dada Engine v1.0 [READY]
""")

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
set_bot_instance(bot)

# Регистрация обработчиков
dp.include_router(commands.router)
dp.include_router(messages.router)
dp.include_router(inline_router)

async def on_startup():
    from handlers.commands import send_daily_horoscope
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_daily_horoscope,
        "cron",
        hour=12
    )
    scheduler.start()
    print("⏰ Планировщик запущен")

if __name__ == '__main__':
    dp.startup.register(on_startup)
    dp.run_polling(bot)
