from flask import Blueprint, current_app, render_template, request
from sqlalchemy import select

from myblog.core.ext import db
from myblog.models import Post

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["POST_PER_PAGE"]
    pagination = db.paginate(
        select(Post).order_by(Post.created_at.desc()), page=page, per_page=per_page
    )
    posts = pagination.items
    return render_template("blog/index.html", pagination=pagination, posts=posts)
