from datetime import datetime

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_session
from app.core.config import DB_FILEPATH, BOT_TOKEN
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

from app.core.models.users import User

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


async def register_user(user_id: int, username: str, chat_id: int, session: AsyncSession):
    user = User(tg_id=user_id, username=username, chat_id=chat_id)
    session.add(user)
    await session.commit()


async def test():
    await db_session.global_init(DB_FILEPATH)
    async with db_session.create_session() as db_sess:
        reminder_service = ReminderService(db_sess)
        notification_service = NotificationService(bot)
        await reminder_service.create_reminder(940091786, "Test", datetime.now(), "Description")
        await notification_service.start()


async def start_polling():
    await dp.start_polling(bot)


async def main():
    tasks = [
        asyncio.create_task(test()),
        asyncio.create_task(start_polling())
    ]
    await asyncio.gather(*tasks)


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    await db_session.global_init(DB_FILEPATH)
    async with db_session.create_session() as db_sess:
        await register_user(message.from_user.id, message.from_user.username, message.chat.id, db_sess)
    await message.reply("Hi!\nNow you're registered! :3")
    logging.log(logging.INFO, f"{message.from_user.id} {message.text}")


@dp.message(Command("new"))
async def process_new_command(message: types.Message):
    pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.log(logging.INFO, "Bot stopped")
