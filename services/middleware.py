import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class Logging:
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        if event.message:
            name = "@" + event.message.from_user.username if event.message.from_user.username \
                else event.message.from_user.first_name
            logging.info(f'{[name, event.message.from_user.id]} - message - {event.message.text}')
        elif event.callback_query:
            name = "@" + event.callback_query.from_user.username if event.callback_query.from_user.username \
                else event.callback_query.from_user.first_name
            logging.info(
                f'{[name, event.callback_query.from_user.id]} - callback_query - {event.callback_query.data}')

        result = await handler(event, data)
        return result
