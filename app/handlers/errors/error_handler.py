import logging

from app.loader import dp
from app.utils.db_api.models import Chat

log = logging.getLogger(__name__)


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted)

    if isinstance(exception, CantDemoteChatCreator):
        log.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        log.debug('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        log.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        log.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        log.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        log.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        log.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        log.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        log.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        log.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    else:
        from app.utils.misc import admin
        # := is just syntax sugar
        # it s equavelent to:
        # >>> func = getattr(Chat, 'get_admin_chats', None)
        # >>> if func:
        # ...     # do something
        # ...
        if func := getattr(Chat, 'get_admin_chats', None):
            chats = await func()
            await admin.notify_error(chats, exception)

    log.exception(f'Update: {update} \n{exception}')
