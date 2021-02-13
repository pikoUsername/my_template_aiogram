import asyncpg

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
    async def create(user_id: int, name: str):
        sql = (
            f"INSERT INTO users(user_id, first_name)",
            "VALUES ($1, $2) RETURNING *;"
        )
        param = (user_id, name)
        result = await UserModel._make_request(
            "".join(sql), param)
        return result
