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


class Debugger:
    __slots__ = "dp", 'logs_path', "_configured"

    def __init__(self, dp: Dispatcher, logs_fp=None):
        self.dp = dp
        self.logs_path = logs_fp or None
        self._configured = 0  # type: bool

    configured = property(lambda self: self._configured)

    def sort_files(self, files):
        pass

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

    async def read_logs(self, last=0):  # last attr type: bool
        pass

    def setup(self):
        if not self.configured:
            self.dp.register_message_handler()
