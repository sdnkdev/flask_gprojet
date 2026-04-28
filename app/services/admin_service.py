from app.models.user import User
from app.services.auth_service import register_user
from app import db
from flask import jsonify

def creer_employe(data, current_user_id):
    """Permet à un admin de créer un compte pour un employé."""
    admin = User.query.get(current_user_id)
    if not admin or admin.role != 'admin':
        return jsonify({"message": "Accès refusé : Seuls les administrateurs peuvent créer des comptes"}), 403
    
  
    result = register_user(data)
    
    if result.get("message") == "Utilisateur déjà existant":
        return jsonify(result), 400
        
    return jsonify({"message": "Compte employé créé avec succès"}), 201

def lister_tous_les_utilisateurs(current_user_id):
    """Liste tous les utilisateurs de l'entreprise pour l'admin."""
    admin = User.query.get(current_user_id)
    if not admin or admin.role != 'admin':
        return None, 403
    
    users = User.query.all()
    return users, 200
