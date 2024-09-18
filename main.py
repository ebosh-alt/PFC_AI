import asyncio
import logging
from contextlib import suppress

from data.config import bot, dp
from entities.database.base import create_async_database
from handlers import routers
from services import middleware
from services.OpenAI import ChatGPT

logger = logging.getLogger(__name__)


async def main() -> None:
    await create_async_database()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await dp.start_polling(bot)
    # s = ChatGPT.create_assistant()
    # print(s)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
