import os

# 根目录
basedir = os.path.abspath(os.path.dirname(__file__))


# config class
class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY") or "this is myblog."

    # sqlalchemy config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 是否自动提交到数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # 使用 mysql 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/myblog"
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    # 使用 mysql 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/test_myblog"
    SQLALCHEMY_ECHO = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/myblog"


config = {
    "dev": DevelopmentConfig,
    "test": TestConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
}
