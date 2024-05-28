from aiogram import Dispatcher, Bot
from environs import Env


env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL")
