from aiogram import Dispatcher
from loguru import logger

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    logger.info("Setuping Middlewares...")

    dp.middleware.setup(ThrottlingMiddleware())
