import json
import os
from pathlib import Path
from typing import Set

# Конфигурация
MAILING_LIST_PATH = Path("data/mailing_list.json")
MAILING_LIST_PATH.parent.mkdir(exist_ok=True)  # Создаем папку data

# Инициализация списка
mailing_list: Set[int] = set()

def load_mailing_list() -> None:
    """Загружает список подписчиков из файла"""
    global mailing_list
    try:
        if MAILING_LIST_PATH.exists():
            with open(MAILING_LIST_PATH, 'r') as f:
                mailing_list = {int(x) for x in json.load(f)}
            print(f"🌀 Загружено {len(mailing_list)} подписчиков")
    except Exception as e:
        print(f"⚠️ Ошибка загрузки списка: {e}")
        mailing_list = set()

def save_mailing_list() -> None:
    """Сохраняет текущий список подписчиков"""
    try:
        with open(MAILING_LIST_PATH, 'w') as f:
            json.dump(list(mailing_list), f)
    except Exception as e:
        print(f"⚠️ Ошибка сохранения списка: {e}")

def add_to_mailing_list(user_id: int) -> None:
    """Добавляет пользователя в рассылку"""
    mailing_list.add(user_id)
    save_mailing_list()
    print(f"✅ Добавлен подписчик: {user_id}")

def remove_from_mailing_list(user_id: int) -> None:
    """Удаляет пользователя из рассылки"""
    if user_id in mailing_list:
        mailing_list.remove(user_id)
        save_mailing_list()
        print(f"❌ Удален подписчик: {user_id}")

# Автозагрузка при импорте
load_mailing_list()