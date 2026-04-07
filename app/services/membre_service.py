from app import db
from app.models.membre import Membre
from app.models.user import User
from flask import jsonify

def ajouter_membre_espace(espace_id, user_email, role, current_user_id):
    # Vérifier si l'appelant est admin de cet espace ou admin de la plateforme
    admin_check = Membre.query.filter_by(user_id=current_user_id, espace_id=espace_id).first()
    platform_admin = User.query.get(current_user_id).role == 'admin'
    
    if not platform_admin and (not admin_check or admin_check.role != 'admin'):
        return jsonify({"message": "Accès refusé: Seuls les administrateurs peuvent ajouter des membres"}), 403

    # Trouver l'utilisateur par email
    user_to_add = User.query.filter_by(email=user_email).first()
    if not user_to_add:
        return jsonify({"message": f"L'utilisateur avec l'email {user_email} n'existe pas"}), 404

    # Vérifier si déjà membre
    if Membre.query.filter_by(user_id=user_to_add.id, espace_id=espace_id).first():
        return jsonify({"message": "L'utilisateur est déjà membre de cet espace"}), 400

    # Création du membre
    nouveau_membre = Membre(
        user_id=user_to_add.id,
        espace_id=espace_id,
        role=role
    )
    db.session.add(nouveau_membre)
    db.session.commit()

    return jsonify({"message": "Membre ajouté avec succès"}), 201

def retirer_membre_espace(membre_id, current_user_id):
    membre_a_retirer = Membre.query.get(membre_id)
    if not membre_a_retirer:
        return jsonify({"message": "Membre non trouvé"}), 404

    # Vérifier si l'appelant est admin de cet espace ou admin plateforme
    admin_check = Membre.query.filter_by(user_id=current_user_id, espace_id=membre_a_retirer.espace_id).first()
    platform_admin = User.query.get(current_user_id).role == 'admin'
    
    if not platform_admin and (not admin_check or admin_check.role != 'admin'):
        # Un utilisateur peut se retirer lui-même même s'il n'est pas admin
        if membre_a_retirer.user_id != current_user_id:
            return jsonify({"message": "Accès refusé"}), 403

    # Empêcher de retirer le dernier admin (optionnel mais recommandé)
    if membre_a_retirer.role == 'admin':
        admin_count = Membre.query.filter_by(espace_id=membre_a_retirer.espace_id, role='admin').count()
        if admin_count <= 1:
            return jsonify({"message": "Impossible de retirer le dernier administrateur de l'espace"}), 400

    db.session.delete(membre_a_retirer)
    db.session.commit()

    return jsonify({"message": "Membre retiré avec succès"}), 200

def changer_role_membre(membre_id, nouveau_role, current_user_id):
    membre_concerne = Membre.query.get(membre_id)
    if not membre_concerne:
        return jsonify({"message": "Membre non trouvé"}), 404

    # Vérifier si l'appelant est admin (espace ou plateforme)
    admin_check = Membre.query.filter_by(user_id=current_user_id, espace_id=membre_concerne.espace_id).first()
    platform_admin = User.query.get(current_user_id).role == 'admin'
    
    if not platform_admin and (not admin_check or admin_check.role != 'admin'):
        return jsonify({"message": "Accès refusé"}), 403

    membre_concerne.role = nouveau_role
    db.session.commit()

    return jsonify({"message": "Rôle mis à jour avec succès"}), 200
