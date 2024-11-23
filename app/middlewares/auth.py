from aiohttp import web
from aiohttp_session import get_session


async def auth_middleware(app, handler):

    async def wrapper(request: web.Request, *args, **kwargs):
        user_session = await get_session(request)
        user_id = user_session.get("user_id", None)
        request.user_id = user_id

        return await handler(request, *args, **kwargs)

    return wrapper
