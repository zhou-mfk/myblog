from flask import Flask

from config import config

from . import blog
from .ext import db, migrate
from .models import post, user


def create_app(config_name: None):
    # 创建 Flask 程序实例
    app = Flask(__name__)

    # 使用对象的方式引入配置文件
    if config_name is None:
        config_name = "devlopment"
    app.config.from_object(config[config_name])

    # 引入扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
