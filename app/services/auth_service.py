from app.models.user import User
from app.utils.jwt_helper import generate_token

from app import db

def register_user(data):

    user = User(
        prenom=data["prenom"],
        nom=data["nom"],
        email=data["email"],
        mot_de_passe=data["password"],
        role='user'
    )

   
    existe_user = User.query.filter_by(email=data["email"]).first()
    if existe_user:
        return {"message": "Utilisateur déjà existant"}

    db.session.add(user)

    db.session.commit()

    return {"message": "Utilisateur créé"}

def login_user(data):

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"message": "Utilisateur introuvable"}

    if user.mot_de_passe != password:
        return {"message": "Mot de passe incorrect"}

    token = generate_token(user)

    return {
        "message": "Connexion réussie",
        "token": token,
        "role": user.role
    }