import logging
from config.settings import config
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers import commands, messages

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

# Регистрация обработчиков
dp.include_router(commands.router)
dp.include_router(messages.router)

if __name__ == '__main__':
    print("🟢 Бот запущен. Ожидание квантовых взаимодействий...")
    dp.run_polling(bot)