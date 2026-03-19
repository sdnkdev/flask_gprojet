from flask import request, jsonify
from app.services.file_service import (
    ajouter_fichier, lister_fichiers_tache, supprimer_fichier
)

def ajouter_fichier_controller(current_user):
    data = request.get_json()
    if not data or not data.get('nom_file') or not data.get('tache_id'):
        return jsonify({"message": "nom_file et tache_id sont requis"}), 400
    try:
        return ajouter_fichier(data, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def lister_fichiers_controller(tache_id, current_user):
    try:
        return lister_fichiers_tache(tache_id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def supprimer_fichier_controller(id, current_user):
    try:
        return supprimer_fichier(id, current_user)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
