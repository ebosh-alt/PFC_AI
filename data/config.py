from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
DATABASE_URL = env("DATABASE_URL")
OPENAI_API_KEY = env("OPENAI_API_KEY")
ASSISTANT = env("ASSISTANT")
BASE_PATH = "./photo/"
