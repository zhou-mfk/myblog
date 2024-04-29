from flask import Blueprint

bp = Blueprint("blog", __name__, url_prefix="/")


@bp.route("/")
@bp.route("/index")
def index():
    return "hello"
