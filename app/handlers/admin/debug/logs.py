import os
from pathlib import Path
from contextlib import suppress

from aiogram import types, Dispatcher

from ._imports import __


# noinspection PyMethodMayBeStatic
class Logs:
    __slots__ = "logs_path",

    def __init__(self, logs_path: Path = None):
        self.logs_path = logs_path

    def last_file(self, fp: Path):
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
        filters = filters if filters else "INFO"
        logs_path = Path(__name__).parent.parent / "logs"

        if last is False:
            logs_path = self.logs_path or logs_path

            # saving filter result and it s incredible, not efficient way
            # this list can store 1000 lines, of logs or more, but who cares?
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

    def setup(self, dp: Dispatcher):
        dp.register_message_handler(self.get_logs, commands="logs", is_admin=True)
