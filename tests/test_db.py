__all__ = ["Post", "User"]
from sqlalchemy import text

from myblog.ext import db
from myblog.models import Post, User  # type ignore


def test_connect_db(app_ctx):
    result = db.session.execute(text("SELECT 1")).first()

    assert result is not None
    assert result[0] == 1


def test_user_model(app_ctx):
    pass


def test_post_model(app_ctx):
    pass
