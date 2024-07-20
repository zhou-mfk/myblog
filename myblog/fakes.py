import random

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from myblog.ext import db
from myblog.models import Admin, Category, Comment, Post

fake = Faker()


def fake_admin():
    admin = Admin(
        username="admin",
        blog_title="myblog",
        blog_sub_title="Thanks",
        name="ZhouLS",
        about="This is my blog -> myblog",
    )
    admin.password = "hello"
    db.session.add(admin)
    db.session.commit()


def fake_categories(count: int = 10):
    # 增加默认分类
    category = Category(name="Default")
    db.session.add(category)
    i = 0
    while i < count - 1:
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):

    for _ in range(count):
        cateory_count = db.session.scalars(select(func.count(Category.id))).one()
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=db.session.get(Category, random.randint(1, cateory_count)),
            created_at=fake.date_time_this_year(),
        )
        db.session.add(post)
    db.session.commit()


def fake_comment(count=500):
    for _ in range(count):
        post_count = db.session.scalars(select(func.count(Post.id))).one()
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            created_at=fake.date_this_year(),
            reviewed=random.choice([True, True, True, True, False]),
            from_admin=random.choice([False, False, False, False, True]),
            post=db.session.get(Post, random.randint(1, post_count)),
        )
        if comment.from_admin:
            comment.author = "ZhouLS"
            comment.email = "zhou_mfk@163.com"
            comment.site = "https://myblog.com"
            comment.reviewed = True
        db.session.add(comment)
    db.session.commit()


def fake_replies(count=50):
    for _ in range(count):
        comment_count = db.session.scalars(select(func.count(Comment.id))).one()
        replied = db.session.get(Comment, random.randint(1, comment_count))
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            created_at=fake.date_this_year(),
            reviewed=True,
            replied=replied,
            post=replied.post,
        )
        db.session.add(comment)
    db.session.commit()
