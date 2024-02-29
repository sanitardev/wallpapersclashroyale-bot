from aiogram import executor
from dispatcher import dp
from filters import IsAdmin
from middleware import ThrottlingMiddleware
import handlers


if __name__ == '__main__':
    dp.bind_filter(IsAdmin)
    dp.setup_middleware(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True)