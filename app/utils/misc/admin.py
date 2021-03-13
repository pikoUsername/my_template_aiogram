from app.loader import bot
from app.utils.misc.embed import Embed


async def notify_error(chats: list, err: Exception):
    e = Embed("Сообщение об Ошибке")
    e.add_field(title=err.__class__.__name__, text=str(err.__cause__))
    if chats is not None:
        for chat in chats:
            await bot.send_message(chat.chat_id, str(e))
        return
