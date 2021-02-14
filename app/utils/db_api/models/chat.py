from aiogram import types

from .._conn.postgres import PostgresConnection


class Chat(PostgresConnection):
    @staticmethod
    async def get(cid: int):
        c = await Chat._make_request(
            "SELECT * FROM users WHERE user_id = $1;",
            (cid,), fetch=True)
        return c

    @staticmethod
    async def create(chat: types.Chat):
        sql = "INSERT INTO chats(chat_id, title, type) VALUES ($1, $2, $3) RETURNING *;"
        c = await Chat._make_request(sql, (chat.id, chat.title, chat.type))
        return c
