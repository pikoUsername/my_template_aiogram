# https://github.com/aiogram/bot/blob/master/app/middlewares/i18n.py yeah
from dataclasses import dataclass, field
from typing import Any, Tuple

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):
    __slots__ = ()

    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇺🇸", "English"),
        "ru": LanguageData("🇷🇺", "Русский"),
    }

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        data: dict = args[-1]
        if "chat" in data:
            user = data['user']
            user_lang = user.get('user_lang', self.default)
            return user_lang

        return self.default
