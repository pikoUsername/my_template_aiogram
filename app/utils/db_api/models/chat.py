from aiogram import types

from .._conn.postgres import PostgresConnection

__all__ = "Chat",


class Chat(PostgresConnection):
    __slots__ = ()

    @staticmethod
    async def get(cid: int):
        c = await Chat._make_request(
            "SELECT * FROM users WHERE user_id = $1 LIMIT 1;",
            (cid,), fetch=True)
        return c

    @staticmethod
    async def create(chat: types.Chat):
        sql = "INSERT INTO chats(chat_id, title, type) VALUES ($1, $2, $3) RETURNING *;"
        c = await Chat._make_request(sql, (chat.id, chat.title, chat.type))
        return c

    @staticmethod
    async def get_admin_chats():
        sql = "SELECT c.* FROM chats AS c WHERE is_admin_chat = true AND notify_errors = true;"
        result = await Chat._make_request(sql, fetch=True)
        return result
