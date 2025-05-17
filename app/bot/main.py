from datetime import datetime

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import db_session
from app.core.config import DB_FILEPATH, BOT_TOKEN
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

from app.core.models.users import User

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

new_router = Router()
dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


class NewReminder(StatesGroup):
    new_reminder = State()
    new_reminder_dt = State()
    new_reminder_description = State()


async def check_user_registration(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first() is not None


async def register_user(user_id: int, username: str, session: AsyncSession):
    user = User(user_id=user_id, username=username)
    session.add(user)
    await session.commit()


async def start_polling():
    dp.include_router(new_router)
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


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    async with db_session.create_session() as db_sess:
        if await check_user_registration(message.from_user.id, db_sess):
            await message.reply("You're already registered :3")
            return
        await register_user(message.from_user.id, message.from_user.username, db_sess)
    await message.reply("Hi!\nNow you're registered! :3")


@dp.message(Command("reminders"))
async def process_reminders_command(message: types.Message):
    async with db_session.create_session() as db_sess:
        if not await check_user_registration(message.from_user.id, db_sess):
            await message.reply("You're not registered yet :(\nUse /start first")
            return
        reminder_service = ReminderService(db_sess)
        reminders = await reminder_service.get_reminders(message.from_user.id)
        if not reminders:
            await message.reply("You have no reminders :(")
            return
        answer = "Your reminders:\n"
        for reminder in reminders:
            answer += (f"Reminder: *{reminder.title}* {reminder.description}\n")
        await message.reply(f"{answer}", parse_mode="Markdown")


@new_router.message(Command("new"))
@new_router.message(Command("new_reminder"))
@new_router.message(F.text.casefold() == "new")
async def process_new_command(message: types.Message, state: FSMContext):
    async with db_session.create_session() as db_sess:
        if not await check_user_registration(message.from_user.id, db_sess):
            await message.reply("You're not registered yet :(\nUse /start first")
            return
    await state.set_state(NewReminder.new_reminder)
    await message.reply("Enter title")


@new_router.message(Command("skip"))
@new_router.message(F.text.casefold() == "skip")
async def skip_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != NewReminder.new_reminder_description.state:
        await message.reply("You cannot skip this stage! >:C")
        await state.set_state(current_state)
        return
    data = await state.get_data()
    title = data["title"]
    remind_dt = data["remind_dt"]
    await state.clear()
    async with db_session.create_session() as db_sess:
        reminder_service = ReminderService(db_sess)
        await reminder_service.create_reminder(message.from_user.id, title, remind_dt)
    await message.reply("Reminder created :3")


@new_router.message(NewReminder.new_reminder)
async def process_new_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await state.set_state(NewReminder.new_reminder_dt)
    await message.reply("Enter date (DD.MM.YYYY HH:MM)")


@new_router.message(NewReminder.new_reminder_dt)
async def process_new_reminder_dt(message: Message, state: FSMContext):
    try:
        remind_dt = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.reply("Invalid date format :(\nTry again")
        await state.set_state(NewReminder.new_reminder_dt)
        return
    await state.update_data(remind_dt=remind_dt)
    await state.set_state(NewReminder.new_reminder_description)
    await message.reply("Enter description (optional. Use /skip to skip)")


@new_router.message(NewReminder.new_reminder_description)
async def process_new_reminder_description(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    remind_dt = data["remind_dt"]
    description = message.text
    await state.clear()
    async with db_session.create_session() as db_sess:
        reminder_service = ReminderService(db_sess)
        await reminder_service.create_reminder(message.from_user.id, title, remind_dt, description)
    await message.reply("Reminder created :3")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.log(logging.INFO, "Bot stopped")
