from flask import Blueprint, abort, current_app, make_response, render_template, request
from sqlalchemy import select

from myblog.ext import db
from myblog.models import Post
from myblog.utils import redirect_back

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["BLOG_POST_PER_PAGE"]
    pagination = db.paginate(
        select(Post).order_by(Post.created_at.desc()),
        page=page,
        per_page=per_page,
    )
    posts = pagination.items
    return render_template("blog/index.html", pagination=pagination, posts=posts)


@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")


@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    return render_template("blog/category.html")


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = db.get_or_404(Post, post_id)

    return render_template("blog/post.html", post=post)


@blog_bp.route("/change_theme/<theme_name>")
def change_theme(theme_name):
    if theme_name not in current_app.config["BLOG_THEMES"].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie("theme", theme_name, max_age=30 * 24 * 60 * 60)
    return response
