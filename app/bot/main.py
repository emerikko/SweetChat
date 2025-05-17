import asyncio

from app.core.utils import check_user_registration, register_user

from app.core import db_session
from app.core.config import DB_FILEPATH, BOT_TOKEN
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

from app.bot.states.new_reminder_route import new_router

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


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

# ugh idk just comment for a commit yk
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.log(logging.INFO, "Bot stopped")
