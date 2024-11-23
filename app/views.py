from aiohttp import web
from aiohttp_jinja2 import template

from app.filters import get_note_filter
from app.services.auth import AuthError, UserNotFoundError, login, logout
from app.services.notes import (
    create_note,
    get_filtered_notes,
    get_note,
    get_notes,
    get_tags,
)
from app.services.users import create_user
from app.tools import is_valid_user_data


class HomeView(web.View):

    @template("index.html")
    async def get(self):
        notes = await get_notes()
        print(notes)
        return {"notes": notes}


class ListCreateNoteView(web.View):

    @template("list_create_note.html")
    async def get(self):

        try:
            note_fitler = get_note_filter(self.request)
            notes = await get_filtered_notes(self.request.user_id, note_fitler)
            tags = await get_tags()

        except ValueError:
            return web.HTTPMovedPermanently("/login")
        return {"notes": notes, "tags": tags}

    @template("list_create_note.html")
    async def post(self):
        data = await self.request.post()

        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags")
        try:
            await create_note(title, content, self.request.user_id, tags=tags)

        except ValueError:
            return web.HTTPMovedPermanently("/login")

        return web.HTTPMovedPermanently("/notes")


class DetailNoteView(web.View):

    @template("note_view.html")
    async def get(self):
        id = int(self.request.match_info.get("id"))
        note = await get_note(id)
        return {"note": note}


class RegistrationView(web.View):

    @template("registration.html")
    async def get(self):
        return {}

    @template("registration.html")
    async def post(self):
        data = await self.request.post()
        msg = is_valid_user_data(data)

        if isinstance(msg, str):
            return {"error": msg}

        username = data.get("usernameInput")
        password = data["passwordInput"]
        email = data["emailInput"]

        try:
            await create_user(username=username, password=password, email=email)
        except ValueError:
            return {"error": "Username already exists"}

        return web.HTTPMovedPermanently("/login")


class LoginView(web.View):

    @template("login.html")
    async def get(self):
        return {}

    @template("login.html")
    async def post(self):
        user_data = await self.request.post()

        try:
            await login(
                self.request, user_data["usernameInput"], user_data["passwordInput"]
            )
        except AuthError as exc:
            return {"error": exc}
        return web.HTTPMovedPermanently("/notes")


class LogOutView(web.View):
    @template("logout.html")
    async def get(self):

        await logout(self.request)
        self.request.user_id = None
        return {}
