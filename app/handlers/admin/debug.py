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
from pathlib import Path

from aiogram import Dispatcher, types

try:
    from app.utils.misc.embed import Embed
except (ImportError, ModuleNotFoundError):
    from dataclasses import dataclass

    @dataclass
    class EmptyEmbed:
        title: str
        value: tuple

        __str__ = __repr__ = lambda self: f"{self.title}\n{''.join(self.value)}"

    Embed = EmptyEmbed
    del EmptyEmbed

try:
    from app.loader import i18n
    __ = i18n.gettext
except (ImportError, ModuleNotFoundError):
    # if you want to copy on another project
    # and this project without support of i18n
    __ = str


class Debugger:
    __slots__ = "dp", 'logs_path', "_configured"

    def __init__(self, dp: Dispatcher, logs_fp=None):
        self.dp = dp
        self.logs_path = logs_fp or None
        self._configured = False

    configured = property(lambda self: self._configured)

    def sort_files(self, files):
        pass

    async def read_log(self, fp, filter_):
        """
        Reads Whole log,
        and filters not need things
        """
        # might blocks, IO
        # but aiofiles.open not working
        f = open(fp)

        def log_filter(x: str):
            return filter_.lower() in x.lower()

        try:
            lines = filter(log_filter, f.readlines())
        finally:
            f.close()
        return lines

    async def read_logs(self, last=True, filters=None):
        """
        NOT TESTED
        """
        filters = filters if filters else "INFO"

        if last is False:
            # Magic
            proj_path = Path(__name__).parent.parent / "logs"

            # saving filter result
            # and it s incredible,
            # not efficient way
            # this list can store 1000 lines,
            # of logs or more
            # but, who cares?
            result = []
            for file in proj_path.glob("*"):
                # blocking io, so be careful about it
                # and i m lazy about correcting it.
                log = await self.read_log(file, filters)
                result.append(log)
            return result

    async def get_logs(self, m: types.Message, *_):
        # get_args it s just a args after /command
        # split for split with using space
        args = m.get_args().split()

        # args is not None: exuavelent just args:
        # but it s looks cool
        if args is not None:
            last = bool(args[0])

            try:
                filters = args[1:]
            except IndexError:
                filters = None

            result = await self.read_logs(last, filters)
            return await m.answer("".join(str(v) for v in result))

        await m.answer(__("Нету Логов"))

    def setup(self):
        """
        Setup a all handlers in this class
        """
        if not self.configured:
            self.dp.register_message_handler(self.get_logs, commands="show_logs")

    def unregister(self):
        """
        Unregisters from discpatcher handlers
        """
        self.dp.message_handlers.unregister(self.get_logs)
