from flask import Blueprint
from app.controllers.tache_controller import (
    creer_tache_controller, modifier_tache_controller,
    supprimer_tache_controller, lister_taches_controller
)
from app.utils.auth_middleware import token_required

tache_bp = Blueprint('tache', __name__, url_prefix='/api/taches')

@tache_bp.route('', methods=['POST'])
@token_required
def creer_tache_route(current_user):
    return creer_tache_controller(current_user)

@tache_bp.route('/<int:id>', methods=['PUT'])
@token_required
def modifier_tache_route(current_user, id):
    return modifier_tache_controller(id, current_user)

@tache_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def supprimer_tache_route(current_user, id):
    return supprimer_tache_controller(id, current_user)

@tache_bp.route('/projet/<int:projet_id>', methods=['GET'])
@token_required
def lister_taches_route(current_user, projet_id):
    return lister_taches_controller(projet_id, current_user)
