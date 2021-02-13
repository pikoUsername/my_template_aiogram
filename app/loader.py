from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.utils.executor import Executor

from app.utils.misc.config import load_config

proj_path = Path(__name__).parent.parent
config = load_config(proj_path)

bot = Bot(config['config']['bot']['TOKEN'], parse_mode=ParseMode.HTML)
bot['config'] = config

dp = Dispatcher(bot)
e = Executor(dp)
