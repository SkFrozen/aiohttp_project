from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import session_maker
from app.models import User
from app.tools import check_password, hash_password


async def create_user(email: str, username: str, password: str) -> None:
    async with session_maker() as session:
        hashed_pass = hash_password(password)
        user = User(email=email, username=username, password=hashed_pass)
        session.add(user)
        try:
            await session.flush()
            await session.commit()
        except:
            await session.rollback()
            raise ValueError


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    if user_id is None:
        return None

    query = select(User).where(User.id == user_id)
    return await session.scalar(query)


async def is_username_exists(session: AsyncSession, username: str) -> bool:
    query = select(User.id).where(User.username == username)

    user_id = await session.scalar(query)
    return bool(user_id)


async def get_user_by_credentials(
    session: AsyncSession, username: str, password: str
) -> User | None:
    query = select(User).where(User.username == username)
    user = await session.scalar(query)
    if user is None:
        return None
    if not check_password(password, user.password):
        return None
    return user
