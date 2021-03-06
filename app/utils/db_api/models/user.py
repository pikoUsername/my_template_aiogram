import asyncpg
from aiogram.types import User

from .._conn.postgres import PostgresConnection

__all__ = "UserModel",


class UserModel(PostgresConnection):
    __slots__ = ()

    @staticmethod
    async def get(id: int) -> asyncpg.Record:
        sql = "SELECT * FROM users WHERE user_id = $1 LIMIT 1;"
        user = await UserModel._make_request(
            sql, (id,), fetch=True)

        return user

    @staticmethod
    async def create(user: User):
        sql = (
            "INSERT INTO users(user_id, first_name, conversation)",
            "VALUES ($1, $2, true) RETURNING *;"
        )
        param = user.id, user.first_name
        result = await UserModel._make_request(
            "".join(sql), param)
        return result

    @staticmethod
    async def get_admins():
        sql = "SELECT u.* FROM users u WHERE u.is_admin = $1;"
        return await UserModel._make_request(sql, (True,))
