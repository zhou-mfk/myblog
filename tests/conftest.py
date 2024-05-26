import pytest

from myblog import create_app
from myblog.ext import db


@pytest.fixture()
def app():
    app = create_app("test")

    # other setup can go here
    # 创建表
    with app.app_context():
        db.create_all()

    # TODO: 增加测试数据

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def app_ctx(app):
    with app.app_context():
        yield
