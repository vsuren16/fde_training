import logging
from logging.config import dictConfig
from pathlib import Path

from app.core.config import get_settings


def configure_logging(log_level: str) -> None:
    settings = get_settings()
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / settings.log_file_name

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "json",
                    "filename": str(log_path),
                    "maxBytes": settings.log_max_bytes,
                    "backupCount": settings.log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "root": {
                "level": log_level,
                "handlers": ["console", "file"],
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
