from flask import Blueprint

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POSt"])
def login(): ...


@auth_bp.route("/logout")
def logout(): ...
