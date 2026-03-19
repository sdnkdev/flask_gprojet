from flask import Blueprint
from app.controllers.projet_controller import (
    creer_projet_controller, modifier_projet_controller,
    supprimer_projet_controller, lister_projets_controller
)
from app.utils.auth_middleware import token_required

projet_bp = Blueprint('projet', __name__, url_prefix='/api/projets')

@projet_bp.route('', methods=['POST'])
@token_required
def creer_projet_route(current_user):
    return creer_projet_controller(current_user)

@projet_bp.route('/<int:id>', methods=['PUT'])
@token_required
def modifier_projet_route(current_user, id):
    return modifier_projet_controller(id, current_user)

@projet_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def supprimer_projet_route(current_user, id):
    return supprimer_projet_controller(id, current_user)

@projet_bp.route('/espace/<int:espace_id>', methods=['GET'])
@token_required
def lister_projets_route(current_user, espace_id):
    return lister_projets_controller(espace_id, current_user)
