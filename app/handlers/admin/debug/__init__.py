"""
Debug tools,
can be used like a admin tools.

Have a functionaliti:
    notify raised errors, and show them

and, yes it task for todo
"""
from aiogram import Dispatcher

from .logs import Logs
from .notify import notify_errors


def setup(dp: Dispatcher, logs_path):
    _reg = dp.register_message_handler

    log_handler = Logs(logs_path)
    log_handler.setup(dp)
    _reg(notify_errors, commands="notify_errors", is_admin=True)
