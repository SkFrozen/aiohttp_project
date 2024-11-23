from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    notes = relationship("Note", back_populates="author")

    def __str__(self):
        return self.username


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped["User"] = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary="notes_tags", back_populates="notes")

    def __str__(self):
        return self.title


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    description: Mapped[str] = mapped_column(String(100), default="tag description")

    notes = relationship("Note", secondary="notes_tags", back_populates="tags")


class NoteTag(Base):
    __tablename__ = "notes_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    tag_name: Mapped[str] = mapped_column(ForeignKey("tags.name"))
