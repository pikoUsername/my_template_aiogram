try:
    from app.utils.db_api.models import Chat
except (ImportError, ModuleNotFoundError):
    Chat = None

try:
    from app.utils.misc.embed import Embed
except (ImportError, ModuleNotFoundError):
    from dataclasses import dataclass

    @dataclass
    class EmptyEmbed:
        title: str
        value: tuple

        __str__ = __repr__ = lambda self: f"{self.title}\n{''.join(self.value)}"

    Embed = EmptyEmbed
    del EmptyEmbed

try:
    from app.loader import i18n
    __ = i18n.gettext
except (ImportError, ModuleNotFoundError):
    # if you want to copy on another project
    # and this project without support of i18n
    __ = str
