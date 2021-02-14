from aiogram import Dispatcher

from loguru import logger


def setup(dp: Dispatcher):
    from .admin import IsAdminFilter

    logger.info("Setuping Filters...")
    dp.filters_factory.bind(IsAdminFilter)
