from os import name

from aiohttp import web

from app import views

routes = [
    web.get("/", views.HomeView, name="home"),
    web.route("*", "/home", views.HomeView, name="index"),
    web.route("*", "/notes", views.ListCreateNoteView, name="notes_list_create"),
    web.route("*", r"/notes/{id:\d+}", views.DetailNoteView, name="note_detail"),
    web.route("*", "/registration", views.RegistrationView, name="registration"),
    web.route("*", "/login", views.LoginView, name="login"),
    web.route("*", "/logout", views.LogOutView, name="logout"),
]
