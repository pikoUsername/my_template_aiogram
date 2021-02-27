from __future__ import annotations

from typing import List, TypeVar, Type, Union, Any

__all__ = "Embed", "Field"

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.callback_data import CallbackData

from app.utils.misc.html import strong

T = TypeVar("T")  # slut type


class InvalidPage(Exception):
    pass


_DEFAULT_KB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("<<", callback_data="pervious_page"),
        InlineKeyboardButton(">>", callback_data="next_page"),
    ]
], row_width=4)

pagination_call = CallbackData("paginator", "key", "page")


class Embed:
    __slots__ = "_title", "value", "fields", "_fields_len"
    """
    Embed like discord, but more worse,
    maybe added pagination, for embed
    """
    def __init__(self, title: str, value=tuple()):
        if not isinstance(value, list):
            value = "".join(value)

        self.value = value if not value else f"{value}\n"

        self._title = title
        self.fields: List[Field] = []
        self._fields_len = 0

    # properties

    @property
    def title(self) -> str:
        return strong(self._title)

    @property
    def clean_embed(self) -> str:
        result = [self.title, self.value]

        for r in self.fields:
            res = r.get_embed()
            result.append(res)

        return "\n".join(result)

    # methods

    def add_field(self, title: str, text: str) -> None:
        field_to_add = self._create_field(
            index=self._fields_len,
            embed=self,
            title=title,
            text=text
        )
        self.fields.append(field_to_add)
        self._fields_len += 1

    @staticmethod
    def _create_field(*args, **kwargs) -> Field:
        field = Field(*args, **kwargs)
        return field

    def change_field(self, index: int, **kwargs):
        f = self.fields[index]
        f_dir = [a for a in f.__dir__() if not a.startswith("__")]
        for k, v in kwargs.items():
            if k in f_dir:
                setattr(f, k, v)
        self.fields[index] = f
        return self.fields[index]

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        self = cls.__new__(cls)

        self.title = data.get("title", None)
        self.value = data.get("value", None)

        return self


class EmbedFieldPaginator(Embed):
    """
    Embed Paginator created like django paginator, but a it difference.
    """
    __slots__ = "_current_field", "per_field"

    def __init__(self, per_page: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._current_field = 0
        self.per_field = per_page

    def get_field(self, page: int):
        try:
            return self.fields[page:self.per_field]
        except IndexError as exc:
            if self.fields:
                if self.has_pervious_page():
                    return self.get_field(page - 1)
            raise exc

    def has_pervious_page(self) -> bool:
        return self._current_field > 1

    def has_next_page(self) -> bool:
        return self._current_field <= self._fields_len

    def next(self) -> Field:
        field = self.get_field(self._current_field + 1)
        self._current_field += 1
        return field

    def pervious(self) -> Field:
        if self._current_field < 1:
            field = self.get_field(self._current_field - 1)
            self._current_field -= 1
        else:
            field = self.get_field(self._current_field)
        return field

    def __iter__(self):
        if self.has_next_page():
            return iter(self.next())


class Field:
    __slots__ = "text", "index", "embed", "title"

    def __init__(
        self,
        embed: Union[Embed, EmbedFieldPaginator],
        title: str,
        text: str,
        index: int = 0
    ) -> None:
        self.title = title
        self.text = text
        # for embed paginator
        self.index = index
        self.embed = embed

    def get_embed(self) -> str:
        _title = strong(self.title)
        return f"{_title}\n{self.text}"

    @classmethod
    def from_dict(cls, **kwargs: Any) -> T:
        a = cls.__new__(cls)

        d = [elem for elem in dir(a)
             if not elem.startswith("__") and not callable(elem)]

        for k, v in kwargs.items():
            if k in d:
                setattr(a, k, v)

        return a

    __str__ = get_embed
    __repr__ = get_embed

