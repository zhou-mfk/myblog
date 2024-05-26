# 如果导入了未使用则配置在此处
__all__ = ["Post", "User"]

# from typing import Optional

import click
from flask import Flask, render_template

from config import config

from . import blog
from .ext import db, migrate
from .models import Post, User


def create_app(config_name: str | None):
    # 创建 Flask 程序实例
    app = Flask(__name__)

    # 使用对象的方式引入配置文件
    if config_name is None:
        config_name = "dev"
    app.config.from_object(config[config_name])

    # 增加心跳地址
    @app.route("/check_health")
    def check_health():
        return "Status: OK"

    register_logging(app)
    # 引入扩展
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    register_commands(app)
    register_errors(app)

    return app


def register_logging(app: Flask) -> None:
    pass


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")


def register_commands(app: Flask) -> None:

    # 添加用户
    @app.cli.command
    @click.option("--username", prompt=True, help="用户名 用于登录使用")
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="用户的密码",
    )
    @click.option("--email", prompt=True, help="用户的邮箱地址")
    def add_user(username, password, email):
        user = User.query.filter_by(**{"username": username}).first()
        if user:
            click.echo(f"用户: {username} 名字已存在.")
            click.echo(f"开始更新{username} 用户信息: password: ******, email: {email}")
            user.update({"email": email, "password": password})
        else:
            user = User(username=username, password=password, email=email)
            user.save()
            click.echo(f"用户: {username} 增加完成.")

    @app.cli.command
    @click.option("--post", default=50, help="增加 posts, 默认是 50 条")
    def forge(post):
        """Generate fake data"""
        # TODO: 生成假数据
        pass


def register_errors(app: Flask) -> None:
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    # TODO: use flask wtf
    # @app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     return render_template('error/400.html', description=e.description), 400
