from typing import Union, List, Any

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Dispatcher

__all__ = ("Paginator",)

class InvalidPage(Exception):
    pass


_DEFAULT_KB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("|<<", callback_data="first_page"),
        InlineKeyboardButton("<<", callback_data="pervious_page"),
        InlineKeyboardButton(">>", callback_data="next_page"),
        InlineKeyboardButton(">>|", callback_data="end_page")
    ]
], row_width=4)


class Paginator:
    __slots__ = ("page_list", "per_page", "current_page", "message", "kb", "dp")

    def __init__(self, object_list: list, per_page: int = 5,
                 message: Message = None, kb=None, dp=None):
        self.page_list = object_list
        self.per_page = int(per_page)
        self.current_page = 0
        self.message = message
        self.kb = kb if kb else _DEFAULT_KB
        self.dp = dp if dp else Dispatcher.get_current()

    @property
    def page_range(self) -> range:
        return range(0, len(self.page_list))

    def page(self, page: int) -> Union[Any, List[Any]]:
        if self.per_page == 1:
            return self.page_list[page]
        else:
            base = page * self.per_page
            return self.page_list[base:base + self.per_page]

    def page_number(self):
        return len(self.page_list)

    def next(self):
        self.current_page += 1
        return self.page(self.current_page)

    def pervious(self):
        self.current_page -= 1
        return self.page(self.current_page)

    @property
    def num_pages(self):
        """Return the total number of pages."""
        return len(self.page_list)

    def has_next(self):
        return self.current_page < self.num_pages

    def has_previous(self):
        return self.current_page > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.current_page + 1

    def previous_page_number(self):
        return self.current_page - 1

    async def start(self, m: Message = None):
        if self.message and m is None:
            raise TypeError("Message and arguemnt 'm' is None")

        self.dp.register_callback_query_handler(self.page_kb_handler, state="*")
        await self.show_page(self.current_page)

    async def show_page(self, page: int):
        page = self.page(page)
        return await self.message.edit_text(page, reply_markup=self.kb)

    async def page_kb_handler(self, query: CallbackQuery):
        if query.data == "first_page":
            page = self.page(0)
            self.current_page = 0
        elif query.data == "pervious_page":
            page = self.pervious()
        elif query.data == "next_page":
            page = self.next()  # todo next page check for has_next
        elif query.data == "end_page":
            np = self.num_pages
            page = self.page(np)
            self.current_page = np
        else:
            page = None

        await self.message.edit_text(page, reply_markup=self.kb)
