# 如果导入了未使用则配置在此处
__all__ = ["Post", "Admin", "Category", "Comment"]

import click
from flask import Flask, render_template
from sqlalchemy import select

from myblog.blueprints.admin import admin_bp
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.ext import bootstrap, ckeditor, db, migrate, moment
from myblog.models import Admin, Category, Comment, Post
from myblog.settings import config


def create_app(config_name: str | None):
    # 使用对象的方式引入配置文件
    if config_name is None:
        config_name = "dev"

    # 创建 Flask 程序实例
    app = Flask("myblog")

    app.config.from_object(config[config_name])

    # 增加心跳地址
    @app.route("/check_health")
    def check_health():
        return "Status: OK"

    # 引入日志
    register_logging(app)

    # 引入扩展
    register_extensions(app)

    # 注册蓝图
    register_blueprints(app)

    register_commands(app)
    if config_name != "test":
        register_errors(app)

    register_template_context(app)

    return app


def register_logging(app: Flask) -> None:
    pass


def register_extensions(app: Flask) -> None:
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    ckeditor.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.add_url_rule("/", endpoint="index")


def register_commands(app: Flask) -> None:
    # 添加用户
    @app.cli.command("forge")
    @click.option(
        "--category", default=10, help="Quantify of categories, default is 10."
    )
    @click.option("--post", default=50, help="增加 posts, 默认是 50 条")
    @click.option("--comment", default=500, help="生成评论， 默认是500条")
    @click.option("--reply", default=50, help="回复评论")
    def forge(category, post, comment, reply):
        """Generate fake data"""
        from myblog.fakes import (
            fake_admin,
            fake_categories,
            fake_comment,
            fake_posts,
            fake_replies,
        )

        # 生成假数据
        db.drop_all()
        db.create_all()

        click.echo("admin user")
        fake_admin()

        click.echo("Categories")
        fake_categories(category)

        click.echo("Posts")
        fake_posts(post)

        click.echo("comment")
        fake_comment(comment)

        click.echo("gen reply")
        fake_replies(reply)

        click.echo("Done.")


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
    #     return render_template("error/400.html", description=e.description), 400


def register_template_context(app: Flask):
    @app.context_processor
    def make_template_context():
        admin = db.session.execute(select(Admin)).first()
        categories = db.session.execute(
            select(Category).order_by(Category.name)
        ).scalars()
        return dict(admin=admin, categories=categories)
