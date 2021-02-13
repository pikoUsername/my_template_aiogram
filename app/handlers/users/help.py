from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, ChatType

from app.loader import dp
from app.utils.misc.throttling import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), ChatType.PRIVATE)
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))
