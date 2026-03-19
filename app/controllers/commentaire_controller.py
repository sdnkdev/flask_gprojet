from flask import request, jsonify
from app.services.commentaire_service import (
    ajouter_commentaire, lister_commentaires_tache, supprimer_commentaire
)

def ajouter_commentaire_controller(current_user):
    data = request.get_json()
    if not data or not data.get('contenu') or not data.get('tache_id'):
        return jsonify({"message": "Contenu et tache_id sont requis"}), 400
    try:
        return ajouter_commentaire(data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def lister_commentaires_controller(tache_id, current_user):
    try:
        return lister_commentaires_tache(tache_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def supprimer_commentaire_controller(id, current_user):
    try:
        return supprimer_commentaire(id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
