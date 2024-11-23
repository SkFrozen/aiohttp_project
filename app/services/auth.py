from aiohttp import web
from aiohttp_session import get_session

from app.db.base import session_maker
from app.middlewares import redis

from .users import get_user_by_credentials


class AuthError(Exception):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class UserAlreadyExistsError(AuthError):
    pass


async def login(request: web.Request, username: str, password: str) -> None:
    async with session_maker() as session:
        user = await get_user_by_credentials(session, username, password)
        if user is None:
            raise InvalidCredentialsError("Invalid login or password")

        session = await get_session(request)
        session["user_id"] = user.id


async def logout(request: web.Request):
    session = await get_session(request)
    result = await redis.delete(f"AIOHTTP_SESSION_{session.identity}")
