import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram import Bot

from app.core import db_session
from app.core.models.reminders import Reminder
from app.core.models.users import User

CHECK_INTERVAL = 10


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def start(self):
        while True:
            try:
                await self.check_and_notify()
            except Exception as e:
                logging.exception("Error while checking reminders: %s", e)
            await asyncio.sleep(CHECK_INTERVAL)

    async def check_and_notify(self):
        now = datetime.now()
        lookahead = now + timedelta(seconds=CHECK_INTERVAL)

        async with db_session.create_session() as session:
            reminders = await self._get_reminders(session, lookahead)
            for reminder in reminders:
                await self._notify_user(reminder, session)

    async def _get_reminders(self, session: AsyncSession, end: datetime):
        stmt = select(Reminder).where(
            Reminder.dt <= end,
            Reminder.is_active.is_(True),
            Reminder.notified.is_(False),
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def _notify_user(self, reminder: Reminder, session: AsyncSession):
        stmt = select(User).where(User.user_id == reminder.user_id)
        user = await session.execute(stmt)
        user = user.scalars().first()
        if user is None:
            logging.log(logging.WARN, f"User {reminder.user_id} not found")
            return
        message = f"⏰ Reminder: *{reminder.title}*"
        if reminder.description:
            message += f"\n{reminder.description}"

        await self.bot.send_message(
            chat_id=user.user_id,
            text=message,
            parse_mode="Markdown"
        )

        reminder.is_active = False
        await session.commit()
