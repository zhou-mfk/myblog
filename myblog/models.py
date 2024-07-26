import datetime
from typing import Dict, List, Optional

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated
from werkzeug.security import check_password_hash, generate_password_hash

from myblog.core.ext import db

"""设置类型映射"""

intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.current_timestamp()),
]


class BaseModel(db.Model):  # type: ignore
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


class Admin(BaseModel):
    __tablename__ = "admin"

    username: Mapped[str] = mapped_column(String(20), doc="用户", nullable=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    blog_title: Mapped[str] = mapped_column(String(60))
    blog_sub_title: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(30))
    custom_footer: Mapped[Optional[str]] = mapped_column(Text)
    custom_css: Mapped[Optional[str]] = mapped_column(Text)
    custom_js: Mapped[Optional[str]] = mapped_column(Text)

    @property
    def password(self):
        raise AttributeError("Write-only property")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(BaseModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(30), unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="category")


class Post(BaseModel):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(60))
    body: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    can_comment: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(back_populates="posts")

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )


class Comment(BaseModel):
    __tablename__ = "comment"

    author: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(255))
    site: Mapped[Optional[str]] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    from_admin: Mapped[bool] = mapped_column(default=False)
    reviewed: Mapped[bool] = mapped_column(default=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    replied_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comment.id"))
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="replied", cascade="all, delete-orphan"
    )
    replied: Mapped["Comment"] = relationship(
        back_populates="replies", remote_side="comment.id"
    )
