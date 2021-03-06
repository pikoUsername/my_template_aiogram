"""
Debug tools,
can be used like a admin tools.

Have a functionaliti:
    show logs, and delete
    show how many humans online
    notify raised errors
    and may used like monitoring tool

and, yes it task for todo
"""
from aiogram import Dispatcher


class Debuger:
    __slots__ = "dp", 'logs_path'

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.logs_path = None

    async def read_log(self, fp, filter_):
        """
        Reads Whole log,
        and filters not need things
        """
        # might blockIO
        # but aiofiles.open not working
        f = open(fp)

        def log_filter(x: str):
            return filter_ in x

        try:
            lines = filter(log_filter, f.readlines())
            return lines
        finally:
            f.close()

    async def read_logs(self, last=0):
        pass
