from flask import Blueprint
from app.controllers.commentaire_controller import (
    ajouter_commentaire_controller, lister_commentaires_controller, supprimer_commentaire_controller
)
from app.utils.auth_middleware import token_required

commentaire_bp = Blueprint('commentaire', __name__, url_prefix='/api/commentaires')

@commentaire_bp.route('', methods=['POST'])
@token_required
def ajouter_commentaire_route(current_user):
    return ajouter_commentaire_controller(current_user)

@commentaire_bp.route('/tache/<int:tache_id>', methods=['GET'])
@token_required
def lister_commentaires_route(current_user, tache_id):
    return lister_commentaires_controller(tache_id, current_user)

@commentaire_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def supprimer_commentaire_route(current_user, id):
    return supprimer_commentaire_controller(id, current_user)
