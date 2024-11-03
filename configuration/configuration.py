import os
from dataclasses import dataclass


@dataclass
class TelegramApi:
    token: str
    admin_login: str


@dataclass
class DatabaseConfig:
    dsn: str


@dataclass
class Configuration:
    db: DatabaseConfig


def load_config() -> Configuration:
    db_dsn = os.environ.get("DB_DSN")
    db_config = DatabaseConfig(db_dsn)
    return Configuration(db=db_config)
