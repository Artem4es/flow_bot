from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH = Path()  # При условии запуска проекта из /solana_bot


class BotSettings(BaseModel):
    token: str


class RedisSettings(BaseSettings):
    host: str
    port: int


class LogSettings(BaseSettings):
    folder: str
    file: str


class UserSettings(BaseSettings):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    bot: BotSettings
    log: LogSettings
    redis: RedisSettings
    user: UserSettings


settings = Settings()
