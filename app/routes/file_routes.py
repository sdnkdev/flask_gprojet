from flask import Blueprint
from app.controllers.file_controller import (
    ajouter_fichier_controller, lister_fichiers_controller, supprimer_fichier_controller
)
from app.utils.auth_middleware import token_required

file_bp = Blueprint('file', __name__, url_prefix='/api/files')

@file_bp.route('', methods=['POST'])
@token_required
def ajouter_fichier_route(current_user):
    return ajouter_fichier_controller(current_user)

@file_bp.route('/tache/<int:tache_id>', methods=['GET'])
@token_required
def lister_fichiers_route(current_user, tache_id):
    return lister_fichiers_controller(tache_id, current_user)

@file_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def supprimer_fichier_route(current_user, id):
    return supprimer_fichier_controller(id, current_user)
