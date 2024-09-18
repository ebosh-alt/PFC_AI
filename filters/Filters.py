import datetime

from aiogram.filters import Filter
from aiogram.types import Message, User

from entities.database import users


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        ...


class ExpiredSubscription(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        user = await users.get(event_from_user.id)
        current_time = datetime.datetime.now()
        if user.available_request is None:
            user.available_request = 0
            await users.update(user)
            return False
        elif user.available_request > 0 and user.expired_date_subscription >= current_time:
            return False
        else:
            return True
