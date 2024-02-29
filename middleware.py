from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram import types
import time
import asyncio
from typing import Union
from dispatcher import *
from utils.ending import ending

class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_',):
        self.limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throtlle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return
        dp = Dispatcher.get_current()
        limit = getattr(handler, "throttling_rate_limit", self.limit)
        key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")   
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)
            raise CancelHandler()

    async def on_process_message(self, message, data):
        await self.throtlle(message)
        
    async def on_process_callback_query(self, message, data):
        await self.throtlle(message)

    @staticmethod
    async def target_throttled(target: Union[types.Message, types.CallbackQuery], 
                            throttled: Throttled, dispatcher: Dispatcher, key: str):
        msg = target.message if isinstance(target, types.CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await msg.reply("Слишком часто, не так быстро.")
            return
        elif throttled.exceeded_count == 3:
            await msg.reply(f"Слишком много запросов, попробуйте через {int(delta)} {ending('секунду', 'секунды', 'секунд', int(delta))}")
            return
        await asyncio.sleep(delta)
    
def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return  
    return decorator