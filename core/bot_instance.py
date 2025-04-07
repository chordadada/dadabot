from aiogram import Bot

_bot_instance = None

def set_bot_instance(bot: Bot):
    global _bot_instance
    _bot_instance = bot

def get_bot() -> Bot:
    if _bot_instance is None:
        raise RuntimeError("Bot instance not initialized!")
    return _bot_instance