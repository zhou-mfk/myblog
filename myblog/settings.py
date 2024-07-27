import os

# 根目录
basedir = os.path.abspath(os.path.dirname(__file__))


# config class
class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY") or "this is myblog."

    # sqlalchemy config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 是否自动提交到数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # blog settings
    POST_PER_PAGE = 10
    MANAGE_POST_PER_PAGE = 15
    COMMENT_PER_PAGE = 15

    ENABLE_CSRF = True
    FILE_UPLOADER = "admin.upload_image"

    THEMES = {"default": "Default", "perfect_blue": "Perfect Blue"}

    SLOW_QUERY_THRESHOLD = 1

    UPLOAD_PATH = os.getenv("UPLOAD_PATH", f"{basedir}/uploads")
    ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
    LOGGING_PATH = os.getenv("GREYBOOK_LOGGING_PATH", f"{basedir}/logs/myblog.log")
    ERROR_EMAIL_SUBJECT = "[MYBLOG] Application Error"


class DevelopmentConfig(Config):
    DEBUG = True
    # 使用 mysql 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/myblog"
    SQLALCHEMY_ECHO = True

    # SQLALCHEMY连接sqlite数据库
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-database.sqlite')


class TestConfig(Config):
    # 使用 mysql 数据库
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:redhat@localhost/myblog"


config = {
    "dev": DevelopmentConfig,
    "test": TestConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
}
