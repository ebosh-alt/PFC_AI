from aiogram import Dispatcher, Bot
from environs import Env


env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
link_to_bot = "https://t.me/selling_accounts_test_bot"
SQLALCHEMY_DATABASE_URI = f'sqlite+aiosqlite:///data/database.db'
