from flask import Blueprint, render_template
from sqlalchemy import select

from myblog.ext import db
from myblog.models import Post

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    posts = db.session.execute(select(Post).order_by(Post.created_at.desc())).scalars()
    return render_template("blog/index.html", posts=posts)


@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")


@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    return render_template("blog/category.html")


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    return render_template("blog/post.html")
