__all__ = ["Post", "User"]

from myblog.ext import db
from myblog.models import Post, User  # type ignore


def test_connect_db(app_ctx):
    result = db.session.execute("SELECT 1")
    assert result is not None
    assert result[0] == 1


def test_user_model(app_ctx):
    pass


def test_post_model(app_ctx):
    pass
