import os
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.executor import Executor
from aiogram import types

from app.loader import dp, bot
from app.utils.db_api.models.user import UserModel

__all__ = ("setup", "runner")

runner = Executor(dp)


async def notify_all_owner(dp):
    admins = await UserModel.get_admins()
    for admin in admins:
        with suppress(TelegramAPIError):
            bot.send_message(admin.user_id, "Bot Started")


async def setup_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('help', 'Справка | Help'),
        types.BotCommand('start', 'Начать разговор | Start consersation')
    ])


def setup():
    runner.on_startup(setup_commands)
    if os.getenv("NOTIFY_ALL_OWNER", None):
        runner.on_startup(notify_all_owner)
