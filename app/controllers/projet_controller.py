from flask import request, jsonify
from app.services.projet_service import (
    creer_projet, modifier_projet, supprimer_projet, lister_projets_espace
)

def creer_projet_controller(current_user):
    data = request.get_json()
    if not data or not data.get('titre') or not data.get('espace_id'):
        return jsonify({"message": "Titre et espace_id sont requis"}), 400
    try:
        return creer_projet(data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def modifier_projet_controller(projet_id, current_user):
    data = request.get_json()
    try:
        return modifier_projet(projet_id, data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def supprimer_projet_controller(projet_id, current_user):
    try:
        return supprimer_projet(projet_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def lister_projets_controller(espace_id, current_user):
    try:
        return lister_projets_espace(espace_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
