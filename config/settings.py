from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os

# Загружаем переменные окружения
load_dotenv()

class Settings(BaseSettings):
    # Основные настройки
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ADMIN_IDS: List[int] = Field(default_factory=list, env="ADMIN_IDS")
    TRANSLATION_KEY: str = Field("", env="TRANSLATION_KEY")  # Для MyMemory API
    MAX_CHAOS_LEVEL: int = Field(100, env="MAX_CHAOS_LEVEL")
    IMGUR_CLIENT_ID: str = Field("", env="IMGUR_CLIENT_ID")
    NASA_API_KEY: str = Field("", env="NASA_API_KEY")
    # Настройки логирования
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    # Дополнительные параметры
    DEBUG: bool = Field(False, env="DEBUG")
    MAX_FILE_SIZE: int = Field(20_971_520, env="MAX_FILE_SIZE")  # 20 MB
    RESET_TIMEOUT: int = Field(300, env="RESET_TIMEOUT")
    QUANTUM_CHANCE: float = Field(0.15, env="QUANTUM_CHANCE")
    INLINE_ENABLED: bool = True
		
    @validator("ADMIN_IDS", pre=True)
    def split_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        elif isinstance(v, list):
            return v
        else:
            return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создаем экземпляр настроек
config = Settings()

import logging
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)