from aiogram import Dispatcher
from loguru import logger

from .throttling import ThrottlingMiddleware
from .acl import Acl
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    logger.info("Setuping Middlewares...")

    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(Acl())
    dp.middleware.setup(ThrottlingMiddleware())
