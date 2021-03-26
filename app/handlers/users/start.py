from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app.loader import dp, i18n

_ = i18n.gettext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(_('Привет, {}!').format(message.from_user.full_name))

