import asyncio
import logging
from typing import Union, List, TypeVar, Type, Optional

import asyncpg
from aiogram import Bot
from loguru import logger

from .base import RawConnection

__all__ = ("PostgresConnection")

T = TypeVar("T")


class PostgresConnection(RawConnection):
    pool: asyncpg.pool.Pool = None
    logger = logging.getLogger('bot')
    loop = asyncio.get_event_loop()

    @staticmethod
    async def __make_request(
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False,
    ):
        if not PostgresConnection.pool:
            bot = Bot.get_current()
            PostgresConnection.pool = await asyncpg.create_pool(
                **bot['config']['database']
            )

        async with PostgresConnection.pool.acquire() as conn:
            async with conn.transaction():
                if fetch:
                    result = await conn.fetch(sql, *params)
                    return result
                else:
                    await conn.execute(sql, *params)

    @staticmethod
    def _convert_to_model(data: Optional[dict], model: Type[T]) -> Optional[T]:
        return model(**data) if data else None

    @staticmethod
    async def _make_request(
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False,
            model_type: Type[T] = None
    ) -> Optional[Union[List[T], T]]:
        raw = await PostgresConnection.__make_request(sql, params, fetch, mult)
        if raw:
            if mult:
                if model_type:
                    return [PostgresConnection._convert_to_model(i, model_type) for i in raw]
                else:
                    return [i for i in raw]
            else:
                if model_type:
                    return PostgresConnection._convert_to_model(raw, model_type)
                else:
                    return raw
        return [] if mult else None

    def __del__(self):
        logger.info("Closing Postgres Connection...")
        self.loop.run_until_complete(self.pool.close())