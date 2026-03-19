import jwt
from functools import wraps
from flask import request, jsonify, current_app, redirect, url_for, flash
from app.models.user import User

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if "access_token" in request.cookies:
            token = request.cookies.get("access_token")
        elif "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            flash("Veuillez vous connecter pour accéder à cette page", "warning")
            return redirect(url_for("auth.show_login"))

        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            current_user = User.query.get(data["user_id"])
            if not current_user:
                 flash("Utilisateur introuvable", "danger")
                 return redirect(url_for("auth.show_login"))
        except:
            flash("Session expirée ou invalide", "danger")
            return redirect(url_for("auth.show_login"))

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):

    @wraps(f)
    def decorated(current_user, *args, **kwargs):

        if current_user.role != "admin":
            flash("Accès réservé aux administrateurs", "danger")
            return redirect(url_for("main.home_route"))

        return f(current_user, *args, **kwargs)

    return decorated
