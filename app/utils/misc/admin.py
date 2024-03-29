from app.loader import bot
from app.utils.misc.embed import Embed


async def notify_error(chats, err: Exception):
    e = Embed("Сообщение об Ошибке")
    e.add_field(title=err.__class__.__name__, text=str(err))
    if chats:
        for chat in chats:
            await bot.send_message(chat.get('chat_id'), e.clean_embed())
        return
