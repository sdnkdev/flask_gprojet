from flask import request, jsonify, render_template, redirect, url_for, flash
from app.services.auth_service import register_user, login_user


def register():
    data = request.form.to_dict()
    
    if data.get("password") != data.get("confirm_password"):
        flash("Les mots de passe ne correspondent pas", "danger")
        return redirect(url_for("auth.show_register"))

    result = register_user(data)
    
    if "error" in result or "message" in result and result.get("message") != "Utilisateur créé":
        flash(result.get("message", "Erreur lors de l'inscription"), "danger")
        return redirect(url_for("auth.show_register"))
    
    flash("Compte créé avec succès ! Connectez-vous.", "success")
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
    if "access_token" in request.cookies:
        return redirect(url_for("main.home_route"))
    return render_template("login.html")

def show_register():
    if "access_token" in request.cookies:
        return redirect(url_for("main.home_route"))
    return render_template("register.html")

