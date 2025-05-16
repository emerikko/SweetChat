from datetime import datetime

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import db_session
from app.core.config import DB_FILEPATH, BOT_TOKEN
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

from app.core.models.users import User

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


async def check_user_registration(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first() is not None


async def register_user(user_id: int, username: str, session: AsyncSession):
    user = User(user_id=user_id, username=username)
    session.add(user)
    await session.commit()


async def start_polling():
    await dp.start_polling(bot)


async def start_notification_service():
    notification_service = NotificationService(bot)
    await notification_service.start()


async def main():
    tasks = [
        asyncio.create_task(db_session.global_init(DB_FILEPATH)),
        asyncio.create_task(start_notification_service()),
        asyncio.create_task(start_polling())
    ]
    await asyncio.gather(*tasks)


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    async with db_session.create_session() as db_sess:
        await register_user(message.from_user.id, message.from_user.username, db_sess)
    await message.reply("Hi!\nNow you're registered! :3")
    logging.log(logging.INFO, f"{message.from_user.id} {message.text}")


@dp.message(Command("new"))
async def process_new_command(message: types.Message):
    async with db_session.create_session() as db_sess:
        if not await check_user_registration(message.from_user.id, db_sess):
            await message.reply("You're not registered yet :(\nUse /start first")
            return
        reminder_service = ReminderService(db_sess)
        await reminder_service.create_reminder(message.from_user.id, "Title", datetime.now(), "Description")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.log(logging.INFO, "Bot stopped")
