import datetime
from typing import Any, Dict

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from .ext import db

"""设置类型映射"""

intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.current_timestamp()),
]


class BaseModel(db.Model):
    """声明基类，用于公共模型, 以及公共查询"""

    __abstract__ = True

    id: Mapped[intpk]
    created_at: Mapped[timestamp]

    @classmethod
    def save(cls, data: Dict):
        new_data = cls(**data)
        db.session.add(new_data)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    @classmethod
    def update(cls, data: Dict):
        cls.update(**data)
        db.session.add(cls)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class User(BaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(128), doc="用户", nullable=True)
    email: Mapped[str] = mapped_column(String(128))

    def __init__(self, *kwargs) -> None:
        super().__init__()
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")


class Post(BaseModel):
    __tablename__ = "post"

    user_id = mapped_column(ForeignKey("user.id"))
    title = mapped_column(Text)
    body = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="posts")
