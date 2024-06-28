import asyncio
import logging
from contextlib import suppress

from data.config import dp, bot, ADMINS

from handlers import routers
from entity.database.base import create_async_database
from entity.database import users, User
from services import middleware
from multiprocessing import Process


logger = logging.getLogger(__name__)

#ФУНКЦИЯ ДОБАВЛЕНИЯ АДМИНОВ
# async def add_admins() -> None:
#     for adm in ADMINS:
#         if await admins.in_(id=adm):
#             pass
#         else:
#             admin = Admin(id=adm)
#             await admins.new(admin=admin)


async def main() -> None:
    await create_async_database()
    # await add_admins()
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
