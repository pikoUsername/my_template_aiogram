from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from app.loader import dp, i18n

_ = i18n.gettext


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = _('Список команд: \n'
             '/start - Начать диалог\n'
             '/help - Получить справку\n')
    await message.answer(text)
