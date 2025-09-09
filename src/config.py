# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""

    # Указываем pydantic, что нужно прочитать переменные из .env файла
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
