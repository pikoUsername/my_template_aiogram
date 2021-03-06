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
import os
from contextlib import suppress
from pathlib import Path

from aiogram import Dispatcher, types

try:
    from app.utils.db_api.models import Chat
except ImportError:
    Chat = None

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
    __slots__ = "dp", 'logs_path', "_configured", "_notify_errors"

    def __init__(self, dp: Dispatcher, logs_fp=None):
        self.dp = dp
        self.logs_path = logs_fp or None

        self._configured = False

    configured = property(lambda self: self._configured)

    @staticmethod
    def last_file(fp: Path):
        """
        Get last log from /logs/ folder
        :return:
        """
        logs_list = os.listdir(fp)
        full_list = [os.path.join(fp, i) for i in logs_list]
        time_sorted_list = sorted(full_list, key=os.path.getmtime)
        with suppress(IndexError):
            return fp / time_sorted_list[-1]

    async def read_log(self, fp: Path, filter_):
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
        logs_path = Path(__name__).parent.parent / "logs"

        if last is False:
            # Magic
            logs_path = self.logs_path or logs_path

            # saving filter result
            # and it s incredible,
            # not efficient way
            # this list can store 1000 lines,
            # of logs or more
            # but, who cares?
            result = []
            for file in logs_path.glob("*"):
                # blocking io, so be careful about it
                # and i m lazy about correcting it.
                log = await self.read_log(file, filters)
                result.append(log)
            return result

        log = await self.read_log(Path(self.last_file(logs_path)), filters)
        return log

    async def get_logs(self, message: types.Message, *_):
        # get_args it s just a args after /command
        # split for split with using space
        args = message.get_args().split()

        # args is not None: exuavelent just args:
        # but it s looks cool
        if args is not None:
            last = bool(args[0])

            try:
                filters = args[1:]
            except IndexError:
                filters = None

            result = await self.read_logs(last, filters)
            return await message.answer("".join(str(v) for v in result))

        await message.answer(__("Нету Логов..."))

    if Chat:
        @staticmethod
        async def notify_errors(message: types.Message, chat):
            if not chat.is_admin_chat:
                await message.answer(__("Это не админский Чат"))
                return

            try:
                # any stuff in as message args
                # became True
                notify = bool(message.get_args().split()[0])
            except IndexError:
                # if user, or admin wont to write args of commands
                # so, IndexError will raise, and except catch error
                # and notify will False
                notify = False

            sql = "UPDATE chats SET notify_errors = $1 WHERE chat_id = $2;"
            await Chat._make_request(sql, (not notify, message.chat.id,))
            await message.answer(__("Успех, этот канал будет уведомлятся об ошибках, если они появятся."))
    else:
        @staticmethod
        async def notify_errors(message: types.Message):
            return await message.answer("No Chat model Found.")

    def _reg(self, *args, **kwargs):
        if 'is_admin' != kwargs:
            kwargs['is_admin'] = True
        self.dp.register_message_handler(*args, **kwargs)

    def setup(self):
        """
        Setup a all handlers in this class
        """
        if not self.configured:
            self._reg(self.get_logs, commands="show_logs")
            self._reg(self.notify_errors, commands="notify_errors")

    def unregister(self):
        """
        Unregisters from discpatcher handlers
        """
        _unreg = self.dp.message_handlers.unregister
        _unreg(self.get_logs)
        _unreg(self.notify_errors)

