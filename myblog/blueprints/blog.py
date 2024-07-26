from flask import Blueprint

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    return "hello"
