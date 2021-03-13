import sys
import logging
from typing import List
from pathlib import Path

from loguru import logger


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


# noinspection PyArgumentList
def setup(lgp: Path, ignore: List[str] = None):
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(lgp / "file_{time}.log", format="{time} {message}", rotation="10 MB")
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    if ignore:
        for i in ignore:
            logger.disable(i)
