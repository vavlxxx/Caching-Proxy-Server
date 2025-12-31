import json
import logging
import logging.config
import os

from src.caching_proxy.config import settings


def get_logging_config() -> dict:
    with open(settings.LOG_CONFIG_FILE, "r") as f:
        config = json.load(f)
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    return config


def configurate_logging() -> None:
    config = get_logging_config()
    logging.config.dictConfig(config)


def get_logger(root_logger_name: str) -> logging.Logger:
    return logging.getLogger(root_logger_name)
