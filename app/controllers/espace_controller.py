from flask import request, jsonify
from app.services.espace_service import creer_espace, modifier_espace, supprimer_espace

def creer_espace_controller(current_user):
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({"message": "Le nom de l'espace est requis"}), 400
        
    try:
        nouvel_espace = creer_espace(data, current_user.id)
        return nouvel_espace
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def modifier_espace_controller(espace_id, current_user):
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Aucune donnée fournie pour la modification"}), 400
        
    try:
        response = modifier_espace(espace_id, data, current_user)
        return response
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def supprimer_espace_controller(espace_id, current_user):
    try:
        response = supprimer_espace(espace_id, current_user)
        return response
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

    