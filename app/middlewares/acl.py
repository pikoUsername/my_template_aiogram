from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.utils.db_api.models import UserModel
from app.utils.db_api.models.chat import Chat


class Acl(BaseMiddleware):
    @staticmethod
    async def setup_chat(u: types.User, c: types.Chat, data: dict):
        chat_id = c.id if c else u.id
        user = await UserModel.get(u.id)
        if not user:
            user = await UserModel.create(u)

        chat = await Chat.get(chat_id)
        if not chat:
            chat = await Chat.create(c)

        data['chat'] = chat
        data['user'] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(message.from_user, message.chat, data)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(query.from_user, query.message.chat if query.message else None, data)