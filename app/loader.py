from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from loguru import logger

from app.utils.misc.config import load_config
from .middlewares.i18n import I18nMiddleware

proj_path = Path(__file__).parent.parent
locales_dir = proj_path / "locales"
config = load_config(proj_path / "app")

storage = MemoryStorage()
bot = Bot(config['bot']['TOKEN'], parse_mode=ParseMode.HTML)
bot['config'] = config
dp = Dispatcher(bot, storage=storage)
i18n = I18nMiddleware("bot", locales_dir, default="ru")


def setup():
    from app import filters
    from app import middlewares
    from app.utils.misc import executor
    from app.utils.misc import logging

    logging.setup(proj_path / "logs")
    middlewares.setup(dp)
    filters.setup(dp)
    executor.setup()

    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import app.handlers
