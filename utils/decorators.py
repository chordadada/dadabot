from functools import wraps
from aiogram import types
from states.user_states import user_state

def log_activity(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Ищем сообщение среди аргументов
        message = None
        for arg in args:
            if isinstance(arg, types.Message):
                message = arg
                break
        if message is None:
            for arg in kwargs.values():
                if isinstance(arg, types.Message):
                    message = arg
                    break
        
        # Логируем команду
        if message:
            user_id = message.from_user.id
            command = message.text.split()[0] if message.text else "unknown"
            user_state.track_command_usage(user_id, command)
            print(f"[🌀] User {user_id} использовал: {command}")

        # Вызываем оригинальную функцию
        return await func(*args, **kwargs)
    
    return wrapper