from flask import request, jsonify
from app.services.tache_service import (
    creer_tache, modifier_tache, supprimer_tache, lister_taches_projet
)

def creer_tache_controller(current_user):
    data = request.get_json()
    if not data or not data.get('titre') or not data.get('projet_id'):
        return jsonify({"message": "Titre et projet_id sont requis"}), 400
    try:
        return creer_tache(data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def modifier_tache_controller(tache_id, current_user):
    data = request.get_json()
    try:
        return modifier_tache(tache_id, data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def supprimer_tache_controller(tache_id, current_user):
    try:
        return supprimer_tache(tache_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def lister_taches_controller(projet_id, current_user):
    try:
        return lister_taches_projet(projet_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
