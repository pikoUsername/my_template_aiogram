from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.utils.db_api.models import UserModel, Chat


class Acl(BaseMiddleware):
    """
    Creating a User and Chat
    """
    # a bit memory saving
    __slots__ = ()

    @staticmethod
    async def setup_chat(u: types.User, c: types.Chat, data: dict):
        """
        Setups to data user, and chat model
        and you can get in handler models

        :param u: Telegram user
        :param c: telegram chat
        :param data:
        :return: None
        """
        chat_id = c.id if c else u.id
        user = await UserModel.get(u.id)
        if not user:
            await UserModel.create(u)
            user = UserModel.get(u.id)

        chat = await Chat.get(chat_id)
        if not chat:
            await Chat.create(c)
            chat = await Chat.get(chat_id)

        data['chat'] = chat
        data['user'] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(message.from_user, message.chat, data)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(query.from_user, query.message.chat if query.message else None, data)
