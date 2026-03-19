from flask import Blueprint
from app.controllers.espace_controller import (
    creer_espace_controller, modifier_espace_controller, supprimer_espace_controller
)
from app.utils.auth_middleware import token_required

espace_bp = Blueprint('espace', __name__, url_prefix='/api/espaces')

@espace_bp.route('/creer', methods=['POST'])
@token_required
def creer_espace_route(current_user):
    return creer_espace_controller(current_user)

@espace_bp.route('/<int:id>', methods=['PUT'])
@token_required
def modifier_espace_route(current_user, id):
    return modifier_espace_controller(id, current_user)

@espace_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def supprimer_espace_route(current_user, id):
    return supprimer_espace_controller(id, current_user)
