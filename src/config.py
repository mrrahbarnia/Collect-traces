from typing import Any
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

from src.constants import Environment

load_dotenv()


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding='utf-8', extra='ignore'
    )


class Config(CustomBaseSettings):
    POSTGRES_URL: PostgresDsn
    ENVIRONMENT: Environment = Environment.PRODUCTION
    APP_VERSION: str = "0.1"

settings = Config() # type: ignore


class LogConfig(BaseModel):
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "console": {
            "format": '%(asctime)s %(levelname)s %(module)s %(funcName)s %(process)d %(thread)d %(message)s',
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        }
    }
    handlers: dict = {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console',
        }
    }
    loggers: dict = {
        'root': {
            'handlers': ['console'],
            'propagate': False,
        },
        'metrics': {
            'handlers': ['console'],
            'propagate': False,
        }
    }


app_configs: dict[str, Any] = {"title": "Collect-Metrics"}
app_configs["root_path"] = f"{settings.APP_VERSION}"
