from .ext import db


class user(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, comment="用户id")
    username = db.Column(db.String(128), unique=True, comment="用户")
    email = db.Column(db.String(128), unique=True, comment="email")


class post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, comment="用户id")
    title = db.Column(db.Text)
    body = db.Column(db.Text)
