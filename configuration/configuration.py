import os
from dataclasses import dataclass


@dataclass
class TelegramApi:
    token: str
    admin_id: str


@dataclass
class DatabaseConfig:
    dsn: str


@dataclass
class Configuration:
    db: DatabaseConfig
    telegram: TelegramApi


def load_config() -> Configuration:
    db_dsn = os.environ.get("DB_DSN")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    admin_id = os.environ.get("TELEGRAM_ADMIN_ID")
    db_config = DatabaseConfig(db_dsn)
    telegram_api = TelegramApi(bot_token, admin_id)
    return Configuration(db=db_config, telegram=telegram_api)
