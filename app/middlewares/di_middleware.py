from contextvars import ContextVar
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DIMiddleware(BaseMiddleware):
    def __init__(self, di_context, container):
        super().__init__()
        self.di_context = di_context
        self.container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        self.di_context.set(self.container)
        return await handler(event, data)
