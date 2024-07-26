__all__ = ["Post", "Admin", "Category", "Comment"]

from flask import Flask

from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.config import config
from myblog.core.ext import db, migrate
from myblog.models import Admin, Category, Comment, Post


def create_app(config_name: str = "dev"):
    # 创建 Flask 程序实例
    app = Flask(__name__)

    # 使用对象的方式引入配置文件
    app.config.from_object(config[config_name])

    # 引入扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.add_url_rule("/", endpoint="index")

    return app
