from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger

from .acl import Acl
# from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    from ..loader import i18n

    logger.info("Setuping Middlewares...")

    # dp.middleware.setup(ThrottlingMiddleware(.4))
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(Acl())
    dp.middleware.setup(i18n)
