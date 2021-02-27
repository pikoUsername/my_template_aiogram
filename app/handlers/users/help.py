from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from app.loader import dp
from app.utils.misc.embed import Embed


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = (
        '/start - Начать диалог',
        '/help - Получить справку'
    )

    e = Embed("Список Команд:")
    for t in text:
        cmd, desc = t.split("-")
        e.add_field(cmd, desc)

    await message.answer(e.clean_embed)
