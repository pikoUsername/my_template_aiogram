from typing import List, Type, TypeVar, Union

__all__ = ("RawConnection",)

T = TypeVar("T")


class RawConnection:
    @staticmethod
    async def __make_request(
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False
    ):
        raise NotImplementedError

    @staticmethod
    async def _make_request(
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False,
            model_type: Type[T] = None
    ):
        raise NotImplementedError