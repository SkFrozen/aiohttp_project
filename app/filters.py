from aiohttp import web
from sqlalchemy.sql import func

from .models import Note, Tag


def get_note_filter(request: web.Request):
    return {
        "search": request.query.get("search", ""),
        "author": request.query.get("author", ""),
        "date_from": request.query.get("date_from", ""),
        "date_to": request.query.get("date_to", ""),
        "tags": request.query.get("tags", []),
    }


def filter_notes(query, filters):
    if filters["search"]:
        query = query.where(
            Note.title.ilike(f"%{filters['search']}%")
            | Note.content.ilike(f"%{filters['search']}%")
        )

    if filters["author"]:
        query = query.where(Note.author_id == filters["author"])

    if filters["date_from"]:
        query = query.where(Note.created_at >= filters["date_from"])

    if filters["date_to"]:
        query = query.where(Note.created_at <= filters["date_to"])

    if filters["tags"]:
        tags = list(map(str.lower, filters[tags]))
        query = query.where(func.lower(Tag.name).in_(tags))

    return query
