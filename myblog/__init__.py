from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

from .blog import bp as blog_bp

db = SQLAlchemy()


def create_app(config_name: None):
    # 创建 Flask 程序实例
    app = Flask(__name__)

    # 使用对象的方式引入配置文件
    if config_name is None:
        config_name = "devlopment"
    app.config.from_object(config[config_name])

    # 引入扩展
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(blog_bp)

    return app
