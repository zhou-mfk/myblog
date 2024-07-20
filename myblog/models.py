import datetime
from typing import Dict, List, Optional

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


class Admin(BaseModel):

    __tablename__ = "admin"

    username: Mapped[str] = mapped_column(String(20))
    password_hash: Mapped[str] = mapped_column(String(256))
    blog_title: Mapped[str] = mapped_column(String(60))
    blog_sub_title: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(30))
    about: Mapped[str] = mapped_column(Text)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return check_password_hash(self.password, password)


class Category(BaseModel):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(String(30), unique=True)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="category")


class Post(BaseModel):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text)
    # 关联分类
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all"
    )  # 级联删除


class Comment(BaseModel):
    __tablename__ = "comments"

    author: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(254))
    site: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    from_admin: Mapped[bool] = mapped_column(default=False)
    reviewed: Mapped[bool] = mapped_column(default=False)
    # 关联文章
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    # 邻接表列关系  即评论的评论
    replied_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"))
    replied: Mapped["Comment"] = relationship(back_populates="replieds", remote_side="Comment.id")  # type: ignore
    replieds: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="replied", cascade="all"
    )
