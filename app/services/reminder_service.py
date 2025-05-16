from typing import List, Optional
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.core.models.reminders import Reminder
from app.core.models.users import User
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


class ReminderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_reminder(self, user_id: int, title: str, remind_dt: datetime,
                              description: Optional[str] = None) -> Reminder:
        logging.log(logging.INFO, f"Creating reminder for {user_id} {title} {remind_dt} {description}")
        # Check for existing reminder at the same time for merging
        existing = await self._find_existing_reminder(user_id, remind_dt)
        if existing:
            # Merge titles and descriptions or customize merging logic
            existing.title += f" / {title}"
            if description:
                existing.description = (existing.description or "") + f"\n{description}"
            self.session.add(existing)
            await self.session.commit()
            return existing

        reminder = Reminder(
            user_id=user_id,
            title=title,
            dt=remind_dt,
            description=description
        )
        self.session.add(reminder)
        await self.session.commit()
        return reminder

    async def _find_existing_reminder(self, user_id: int, dt: datetime) -> Optional[Reminder]:
        stmt = select(Reminder).where(
            Reminder.user_id == user_id,
            Reminder.dt == dt
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_reminders(self, user_id: int, upcoming: bool = True) -> List[Reminder]:
        now = datetime.now(UTC)
        if upcoming:
            stmt = select(Reminder).where(
                Reminder.user_id == user_id,
                Reminder.datetime >= now
            ).order_by(Reminder.datetime)
        else:
            stmt = select(Reminder).where(
                Reminder.user_id == user_id,
                Reminder.datetime < now
            ).order_by(Reminder.datetime.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_reminder(self, reminder_id: int, **fields) -> Optional[Reminder]:
        stmt = select(Reminder).where(Reminder.id == reminder_id)
        result = await self.session.execute(stmt)
        reminder = result.scalars().first()
        if not reminder:
            return None

        for key, value in fields.items():
            if hasattr(reminder, key):
                setattr(reminder, key, value)

        self.session.add(reminder)
        await self.session.commit()
        return reminder

    async def delete_reminder(self, reminder_id: int) -> bool:
        stmt = select(Reminder).where(Reminder.id == reminder_id)
        result = await self.session.execute(stmt)
        reminder = result.scalars().first()
        if not reminder:
            return False

        await self.session.delete(reminder)
        await self.session.commit()
        return True
