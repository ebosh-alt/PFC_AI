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




ai_rt = router
