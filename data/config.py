from aiogram import Dispatcher, Bot
from environs import Env 
from aiogram.enums import ParseMode



env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL")
ADMINS = []
