import os

from aiogram.utils.executor import Executor

from app.loader import dp

runner = Executor(dp)


async def notify_all_owner(dp):
    pass


async def setup():
    if os.getenv("NOTIFY_ALL_OWNER", None):
        runner.on_startup(notify_all_owner)
