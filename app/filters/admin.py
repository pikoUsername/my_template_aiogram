from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class IsAdminFilter(BoundFilter):
    # key, uses in handler registration
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, _) -> bool:
        # ctx_data stores a data, from middlewares, and etc
        user = ctx_data.get()['user']
        return user.is_admin
