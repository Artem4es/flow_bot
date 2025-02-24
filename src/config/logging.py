from logging import config

from src.config.bot import BASE_PATH, settings

LOG_FORMAT = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d)- %(message)s"
LOG_FILE_PATH = BASE_PATH / settings.log.folder / settings.log.file
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "ignore_patterns": ["*.log"],
    "formatters": {"standard": {"format": LOG_FORMAT}},
    "handlers": {
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_PATH,
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 1,  # всего сохраняет 2 файла по maxBytes
            "encoding": "utf8",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    # "loggers": {
    #     "sqlalchemy.engine": {
    #         "handlers": ["console", "file"],
    #         "level": "INFO",
    #         "propagate": False,
    #     },
    # },
}


def setup_logging() -> None:
    config.dictConfig(LOGGING_CONFIG)
