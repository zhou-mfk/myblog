from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .ext import db


class user(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, doc="用户id")
    username: Mapped[str] = mapped_column(String(128), doc="用户", nullable=True)
    email: Mapped[str] = mapped_column(String(128))


class post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, doc="文章id")
    user_id = mapped_column(ForeignKey("user.id"))
    title = mapped_column(Text)
    body = mapped_column(Text)

    user: Mapped["user"] = relationship(back_populates="posts")
