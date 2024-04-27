import logging
from aiogram.types import Message, CallbackQuery
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class Logging:
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        if type(event.message) is Message:
            logging.info(
                f'{["@" + event.message.from_user.username, event.message.from_user.id]}'
                f' - message - {event.message.text}')
        else:
            logging.info(
                f'{["@" + event.callback_query.from_user.username, event.callback_query.from_user.id]}'
                f' - callback_query - {event.callback_query.data}')

        result = await handler(event, data)
        return result
