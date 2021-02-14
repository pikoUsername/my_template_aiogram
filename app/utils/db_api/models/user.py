from typing import List

import asyncpg
from aiogram.types import User

from .._conn.postgres import PostgresConnection


class UserModel(PostgresConnection):
    __slots__ = ()

    @staticmethod
    async def get(id: int) -> asyncpg.Record:
        user = await UserModel._make_request(
            f"SELECT * FROM users WHERE user_id = $1 LIMIT 1;",
            (id,),
            fetch=True
        )
        return user

    @staticmethod
    async def create(user: User):
        sql = (
            "INSERT INTO users(user_id, first_name, conversation)",
            "VALUES ($1, $2, true) RETURNING *;"
        )
        param = (user.id, user.last_name)
        result = await UserModel._make_request(
            "".join(sql), param)
        return result

    @staticmethod
    async def get_admins() -> List[asyncpg.Record]:
        sql = "SELECT * FROM users WHERE is_admin = true;"
        return await UserModel._make_request(sql, fetch=True)
