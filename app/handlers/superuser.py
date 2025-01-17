from typing import Iterable

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from functools import partial

from app.models.config import Config


async def is_superuser(message: Message, superusers: Iterable[int]) -> bool:
    return message.from_user.id in superusers


async def exception(message: Message):
    raise RuntimeError(message.text)


async def leave_chat(message: Message, bot: Bot):
    await bot.leave_chat(message.chat.id)


async def get_dump(_: Message, config: Config, bot: Bot):
    with open(config.db.db_path, 'rb') as f:
        await bot.send_document(config.dump_chat_id, BufferedInputFile(f.read(), "karma.db"))


def setup_superuser(bot_config: Config) -> Router:
    router = Router(name=__name__)
    is_superuser_ = partial(is_superuser, superusers=bot_config.superusers)
    router.message.filter(is_superuser_)

    router.message.register(exception, Command(commands="exception"))
    router.message.register(leave_chat, Command(commands="get_out"))
    router.message.register(get_dump, Command(commands="dump"))

    return router
