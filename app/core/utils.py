from sqlalchemy import select
from app.core.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession


async def check_user_registration(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first() is not None


async def register_user(user_id: int, username: str, session: AsyncSession):
    user = User(user_id=user_id, username=username)
    session.add(user)
    await session.commit()
