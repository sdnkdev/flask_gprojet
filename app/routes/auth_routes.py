from flask import Blueprint
from app.controllers.auth_controller import register, login, show_login, show_register, logout

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)

auth_bp.route("/login", methods=["POST"])(login)

auth_bp.route("/login", methods=["GET"])(show_login)

auth_bp.route("/register", methods=["GET"])(show_register)

auth_bp.route("/logout", methods=["GET"])(logout)

