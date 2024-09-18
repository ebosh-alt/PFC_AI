import logging

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message

from data.config import bot, BASE_PATH
from entities.database import users
from services.GetMessage import send_mes
from services.OpenAI import ChatGPT

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.photo)
async def analysis(message: Message):
    id = message.from_user.id
    user = await users.get(id)
    # logger.info(message.photo)
    path_file = f"{BASE_PATH}{id}_{message.photo[-1].file_id}.png"
    await bot.download(
        message.photo[-1],
        destination=path_file)
    logger.info("Downloaded file")
    await bot.send_chat_action(chat_id=id, action=ChatAction.TYPING, request_timeout=3)
    # answer = await ChatGPT.analysis(path_file=path_file,
    #                                 vector_store_id=user.vector_store_id,
    #                                 user_id=id,
    #                                 thread_id=user.thread_id)
    answer = ChatGPT.vision(path_file)
    logger.info(f"Get answer: {answer}")
    await send_mes(id, answer)
    user.available_request -= 1
    await users.update(user)

ai_rt = router
