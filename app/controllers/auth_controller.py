from flask import request, jsonify, render_template, redirect, url_for, flash, current_app
from app.services.auth_service import register_user, login_user
import jwt


def register():
    # L'inscription publique est désormais désactivée dans le modèle entreprise
    flash("L'inscription publique est désactivée. Contactez votre administrateur.", "warning")
    return redirect(url_for("auth.show_login"))

def login():
    data = request.form.to_dict()
    result = login_user(data)

    if "token" in result:
       
        response = redirect(url_for("main.home_route"))
        response.set_cookie('access_token', result['token'], httponly=True, max_age=86400)
        return response

    flash(result.get("message", "Identifiants invalides"), "danger")
    return redirect(url_for("auth.show_login"))

def logout():
    response = redirect(url_for("auth.show_login"))
    response.delete_cookie('access_token')
    flash("Vous avez été déconnecté", "info")
    return response

def show_login():
    token = request.cookies.get("access_token")
    if token:
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return redirect(url_for("main.home_route"))
        except:
            pass
    return render_template("login.html")

def show_register():
    # Rediriger vers la connexion car l'inscription est privée
    flash("Veuillez vous connecter pour accéder à l'application.", "info")
    return redirect(url_for("auth.show_login"))

