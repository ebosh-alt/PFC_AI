import datetime
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entities.database import users, User
from services.GetMessage import get_mes
from services.OpenAI import ChatGPT

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    free = False
    if user is None:
        vector_store = ChatGPT.create_vector_store(id)
        thread = ChatGPT.create_thread()
        await users.new(User(
            id=id,
            expired_date_subscription=datetime.datetime.now() + datetime.timedelta(days=30),
            vector_store_id=vector_store.id,
            thread_id=thread.id
        ))
        user = await users.get(id)
    if user.available_request is None:
        free = True
    await bot.send_message(
        chat_id=id,
        text=get_mes("start_mes", free=free),
    )


menu_rt = router
