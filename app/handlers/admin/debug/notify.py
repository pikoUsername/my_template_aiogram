from aiogram import types

from ._imports import Chat, __


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
