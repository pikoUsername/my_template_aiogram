import time

from loguru import logger as log

from app.utils.misc import admin
from app.loader import dp
from app.utils.db_api.models import Chat


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    chats = await Chat.get_admin_chats()
    await admin.notify_error(chats, exception)
    log.exception(f'Update: {update} \n{exception}')
    return True
