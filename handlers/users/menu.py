import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start(message: Message | CallbackQuery):
    id = message.from_user.id


menu_rt = router
