__all__ = ["Post", "Admin", "Category", "Comment"]

from flask import Flask

from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.core.commands import register_commands
from myblog.core.ext import bootstrap, ckeditor, csrf, db, login_manager, migrate
from myblog.models import Admin, Category, Comment, Post
from myblog.settings import config


def create_app(config_name: str = "dev"):
    # 创建 Flask 程序实例
    app = Flask(__name__)

    # 使用对象的方式引入配置文件
    app.config.from_object(config[config_name])

    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.add_url_rule("/", endpoint="index")

    # 引入扩展
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    # mail.init_app(app)
    # toolbar.init_app(app)
    migrate.init_app(app, db)
    # register_logging(app)
    register_commands(app)
    # register_errors(app)
    # register_template_handlers(app)
    # register_request_handlers(app)
    # register_shell_handlers(app)

    return app
