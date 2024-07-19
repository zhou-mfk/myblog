import os

# 根目录
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# config class
class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY", "this is myblog.")

    # sqlalchemy config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 是否自动提交到数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLOG_POST_PER_PAGE = 10
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(Config):
    DEBUG = True
    # 使用 mysql 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/myblog"
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    # 使用 sqlite memory 数据库
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/test_myblog"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
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
