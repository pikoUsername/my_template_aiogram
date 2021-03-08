from app.loader import bot
from app.utils.misc.embed import Embed


async def notify_error(chats, err):
    e = Embed("Сообщение об Ошибке")
    e.add_field(title=err.__name__, text=err.__cause__)

    for chat in chats:
        await bot.send_message(chat.chat_id, str(e))
