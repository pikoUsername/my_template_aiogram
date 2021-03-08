from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from loguru import logger

from app.utils.misc.config import load_config
from .middlewares.i18n import I18nMiddleware

__all__ = "setup", "dp", "bot", "config", "i18n", "proj_path", "locales_dir"


# globals ####################################

proj_path = Path(__file__).parent.parent
locales_dir = proj_path / "locales"
config = load_config(proj_path / "app")

storage = MemoryStorage()
bot = Bot(config['bot']['TOKEN'], parse_mode=ParseMode.HTML)
bot['config'] = config
dp = Dispatcher(bot, storage=storage)
i18n = I18nMiddleware("bot", locales_dir, default="en")

# setup #######################################


def setup():
    # importing stuff
    from app import filters
    from app import middlewares
    from app.utils.misc import executor
    from app.utils.misc import logging

    # it s a magic of python, and Path class
    logging.setup(proj_path / "logs")

    # setup middlewares, setup using Dispatcher
    # instead Dispatcher may use Dispatcher.get_current() for get_current dp
    middlewares.setup(dp)

    # filters setup, filters setup to Dispatcher
    # First When Handler type triggers, then aiogram check out
    # a filters, to, and check something
    # and if filters dont skiped, and etc.
    # then, handler will activate
    filters.setup(dp)

    # you can use, instead executor.setup use
    # just dispatcher.start_polling() but this meth,
    # not so cool, like executor.start_polling() or webhook
    # and yes, executor supports webhooks.
    # webhooks like subsribing in youtube, but instead youtube bot subrcibes to server events
    # and when on server someting happend, so server sends request, and bot handles this,
    # and return response
    executor.setup()

    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    from app import handlers
    from app.handlers import admin

    admin.setup(dp, proj_path / "logs")
