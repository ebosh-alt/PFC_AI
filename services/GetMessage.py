from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from jinja2 import Environment, PackageLoader, select_autoescape

from data.config import bot


def get_text(text: str) -> str:
    text = text.replace("_", r"\_")
    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")
    text = text.replace("[", r"\[")
    text = text.replace("]", r"\]")
    text = text.replace("<", r"\<")
    text = text.replace(">", r"\>")
    text = text.replace("(", r"\(")
    text = text.replace(")", r"\)")
    text = text.replace("#", "")
    text = text.replace("+", r"\+")
    text = text.replace("-", r"\-")
    text = text.replace(".", r"\.")
    text = text.replace("!", r"\!")
    text = text.replace("=", r"\=")
    text = text.replace("|", r"\|")
    text = text.replace("**", "*")
    return text


def get_mes(path: str, **kwargs):
    env = Environment(
        loader=PackageLoader(package_name='main', package_path="messages", encoding="utf-8"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    if ".md" not in path:
        path = path + '.md'
    tmpl = env.get_template(path)
    return tmpl.render(kwargs)


async def send_mes(id, response):
    try:
        text = get_text(response)
        if len(text) > 4096:
            count_message = len(text) // 4096
            for i in range(count_message + 1):
                await bot.send_message(chat_id=id,
                                       text=text[i * 4096:(i + 1) * 4096],
                                       parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await bot.send_message(chat_id=id,
                                   text=text,
                                   parse_mode=ParseMode.MARKDOWN_V2)
    except TelegramBadRequest:
        text = response
        if len(text) > 4096:
            count_message = len(text) // 4096
            for i in range(count_message + 1):
                await bot.send_message(chat_id=id,
                                       text=text[i * 4096:(i + 1) * 4096])
        else:
            await bot.send_message(chat_id=id,
                                   text=text)
