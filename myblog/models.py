import datetime
from typing import Dict, List

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated
from werkzeug.security import check_password_hash, generate_password_hash

from myblog.ext import db

"""设置类型映射"""

intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.current_timestamp()),
]


class BaseModel(db.Model):  # type: ignore[name-defined]
    """声明基类，用于公共模型, 以及公共查询"""

    __abstract__ = True

    id: Mapped[intpk]
    created_at: Mapped[timestamp]

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def update(self, data: Dict) -> None:
        if data:
            fields = [x for x in self.__dict__.keys() if not x.startswith("_")]
            for k, v in data.items():
                if k not in fields:
                    print(f"WARN: Field `{k}` may not be saved!")
                else:
                    if k == "password":
                        v = generate_password_hash(v)
                    setattr(self, k, v)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), doc="用户", nullable=True)
    email: Mapped[str] = mapped_column(String(128))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return check_password_hash(self.password, password)


class Post(BaseModel):
    __tablename__ = "posts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="posts")
