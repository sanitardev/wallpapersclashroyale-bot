from config import ADMIN
from aiogram import types
from aiogram.dispatcher.filters import Filter


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        return message.from_user.id == int(ADMIN)
