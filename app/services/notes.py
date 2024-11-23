from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import array_agg

from app.db.base import session_maker
from app.filters import filter_notes
from app.models import Note, NoteTag, Tag, User

from .auth import UserNotFoundError
from .users import get_user_by_id


async def get_note(note_id: int):

    async with session_maker() as session:
        query = select(Note).where(Note.id == note_id)
        note = await session.execute(query)
        note = note.scalar()
        if note is None:
            raise ValueError
        return note


async def get_notes():
    async with session_maker() as session:
        query = (
            select(
                Note.id,
                Note.title,
                User.username,
                array_agg(Tag.name).label("tags"),
                Note.created_at,
            )
            .join(User, Note.author_id == User.id)
            .join(NoteTag, Note.id == NoteTag.note_id)
            .join(Tag, NoteTag.tag_name == Tag.name)
            .group_by(Note.id, User.username)
            .order_by(Note.created_at.desc())
            .limit(10)
        )
        result = await session.execute(query)

        return [
            {
                "id": row[0],
                "title": row[1],
                "username": row[2],
                "tags": row[3],
                "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S"),
            }
            for row in result
        ]


async def get_filtered_notes(user_id: int, filters: dict):

    async with session_maker() as session:
        user = await get_user_by_id(session, user_id)

        if user is None:
            raise ValueError

        notes = await get_user_notes(session, user_id, filters)

        return notes


async def get_user_notes(
    session: AsyncSession, user_id: int, filters: dict | None = None
) -> list[dict]:
    """Get user notes with filtering and pagination."""
    query = (
        select(
            Note.id,
            Note.title,
            User.username,
            array_agg(Tag.name).label("tags"),
            Note.created_at,
        )
        .where(Note.author_id == user_id)
        .join(User, Note.author_id == User.id)
        .join(NoteTag, Note.id == NoteTag.note_id)
        .join(Tag, NoteTag.tag_name == Tag.name)
        .group_by(Note.id, User.username)
        .order_by(Note.created_at.desc())
    )

    if filters is not None:
        query = filter_notes(query, filters)

    result = await session.execute(query)

    return [
        {
            "id": row[0],
            "title": row[1],
            "username": row[2],
            "tags": row[3],
            "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S"),
        }
        for row in result
    ]


async def create_note(title: str, content: str, user_id: int, tags: str):

    async with session_maker() as session:
        user = await get_user_by_id(session, user_id)
        if user is None:
            raise ValueError
        lst_tags = list(map(str.strip, tags.split(",")))
        tags = await get_or_create_tags(session, lst_tags)
        note = Note(title=title, content=content, author_id=user_id, tags=tags)
        session.add(note)
        await session.flush()
        await session.commit()

        return note


async def get_or_create_tags(
    session: AsyncSession, tags: list[str], commit: bool = False
):
    result = []

    for tag_name in tags:
        stored_tag_result = await session.execute(
            select(Tag).where(Tag.name.ilike(tag_name))
        )
        stored_tag: Tag | None = stored_tag_result.scalar_one_or_none()

        if stored_tag is not None:
            result.append(stored_tag)
        else:
            tag = Tag(name=tag_name)
            session.add(tag)
            result.append(tag)

    if commit:
        for tag in result:
            await session.flush()
        session.commit()

    return result


async def get_tags():
    async with session_maker() as session:
        result = await session.execute(select(Tag))
        return result.scalars().all()
