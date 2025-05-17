from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command

from app.core import db_session
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

from app.core.utils import check_user_registration, register_user


class NewReminder(StatesGroup):
    new_reminder = State()
    new_reminder_dt = State()
    new_reminder_description = State()


new_router = Router()


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
