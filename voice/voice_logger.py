"""
voice/voice_logger.py

Production Logging Framework for Voice Module.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class VoiceLogger:
    """
    Singleton Logger.

    Features
    --------
    ✔ Rotating Logs
    ✔ Console Logs
    ✔ File Logs
    ✔ Thread Safe
    ✔ Production Ready
    """

    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:

        if cls._logger:
            return cls._logger

        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("jarvis.voice")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",

            datefmt="%Y-%m-%d %H:%M:%S"

        )

        file_handler = RotatingFileHandler(

            filename=log_dir / "voice.log",

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"

        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        logger.propagate = False

        cls._logger = logger

        return logger

    @classmethod
    def set_level(cls, level: int):

        logger = cls.get_logger()

        logger.setLevel(level)

        for handler in logger.handlers:
            handler.setLevel(level)