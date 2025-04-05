import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers import commands, messages
import os
from dotenv import load_dotenv

# Явная загрузка .env
load_dotenv()

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
    token=os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML")
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
dp.include_router(commands.router)
dp.include_router(messages.router)
# dp.message.register(commands.cmd_start, F.text == "/start")
# dp.message.register(messages.handle_message)
# dp.include_router(commands_router)

if __name__ == '__main__':
    print("🟢 Бот запущен. Ожидание квантовых взаимодействий...")
    dp.run_polling(bot)