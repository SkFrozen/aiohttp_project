import aiohttp_jinja2
from aiohttp import web
from jinja2 import FileSystemLoader

import app.tools.cription
from app.middlewares import auth_middleware, redis_session_middleware
from app.urls import routes

app = web.Application(
    middlewares=[
        redis_session_middleware,
        auth_middleware,
    ],
)


aiohttp_jinja2.setup(
    app,
    loader=FileSystemLoader("templates"),
    context_processors=[
        aiohttp_jinja2.request_processor,
    ],
)

app.router.add_routes(routes)

web.run_app(app, host="localhost", port=8000)
