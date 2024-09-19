import asyncio
import datetime
import logging
from contextlib import suppress

from data.config import bot, dp
from entities.database import users
from entities.database.base import create_async_database
from handlers import routers
from services import middleware

logger = logging.getLogger(__name__)


async def test():
    await create_async_database()
    user = await users.get(147548604)
    user.available_request = 50
    user.expired_date_subscription = datetime.datetime.now() + datetime.timedelta(days=30)
    await users.update(user)


async def main():
    await create_async_database()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
