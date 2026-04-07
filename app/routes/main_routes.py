from flask import Blueprint
from app.controllers.main_controller import (
    home, list_espaces, list_projets_espace, projet_details, 
    tache_details, commentaire_details, file_details
)
from app.utils.auth_middleware import token_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@token_required
def home_route(current_user):
    return home(current_user)

@main_bp.route('/espaces/creer', methods=['POST'])
@token_required
def creer_espace_ui_route(current_user):
    from app.controllers.main_controller import creer_espace_ui
    return creer_espace_ui(current_user)

@main_bp.route('/espaces')
@token_required
def espaces_route(current_user):
    return list_espaces(current_user)

@main_bp.route('/espaces/<int:id>/projets')
@token_required
def espace_projets_route(current_user, id):
    return list_projets_espace(id, current_user)

@main_bp.route('/espaces/<int:id>/modifier', methods=['POST'])
@token_required
def modifier_espace_ui_route(current_user, id):
    from app.controllers.main_controller import modifier_espace_ui
    return modifier_espace_ui(id, current_user)

@main_bp.route('/espaces/<int:id>/supprimer', methods=['POST'])
@token_required
def supprimer_espace_ui_route(current_user, id):
    from app.controllers.main_controller import supprimer_espace_ui
    return supprimer_espace_ui(id, current_user)

@main_bp.route('/espaces/<int:espace_id>/projets/creer', methods=['POST'])
@token_required
def creer_projet_ui_route(current_user, espace_id):
    from app.controllers.main_controller import creer_projet_ui
    return creer_projet_ui(espace_id, current_user)

@main_bp.route('/projets/<int:id>/modifier', methods=['POST'])
@token_required
def modifier_projet_ui_route(current_user, id):
    from app.controllers.main_controller import modifier_projet_ui
    return modifier_projet_ui(id, current_user)

@main_bp.route('/projets/<int:id>/supprimer', methods=['POST'])
@token_required
def supprimer_projet_ui_route(current_user, id):
    from app.controllers.main_controller import supprimer_projet_ui
    return supprimer_projet_ui(id, current_user)

@main_bp.route('/projets/<int:id>/taches/creer', methods=['POST'])
@token_required
def creer_tache_ui_route(current_user, id):
    from app.controllers.main_controller import creer_tache_ui
    return creer_tache_ui(id, current_user)

@main_bp.route('/projets/<int:id>')
@token_required
def projet_details_route(current_user, id):
    return projet_details(id, current_user)

@main_bp.route('/taches/<int:id>')
@token_required
def tache_details_route(current_user, id):
    return tache_details(id, current_user)

@main_bp.route('/commentaires/<int:id>')
@token_required
def commentaire_details_route(current_user, id):
    return commentaire_details(id, current_user)

@main_bp.route('/files/<int:id>')
@token_required
def file_details_route(current_user, id):
    return file_details(id, current_user)

@main_bp.route('/profil')
@token_required
def profil_route(current_user):
    from app.controllers.main_controller import profil_ui
    return profil_ui(current_user)

@main_bp.route('/taches/<int:id>/modifier', methods=['POST'])
@token_required
def modifier_tache_ui_route(current_user, id):
    from app.controllers.main_controller import modifier_tache_ui
    return modifier_tache_ui(id, current_user)

@main_bp.route('/taches/<int:id>/supprimer', methods=['POST'])
@token_required
def supprimer_tache_ui_route(current_user, id):
    from app.controllers.main_controller import supprimer_tache_ui
    return supprimer_tache_ui(id, current_user)

@main_bp.route('/taches/<int:id>/commentaires/ajouter', methods=['POST'])
@token_required
def ajouter_commentaire_ui_route(current_user, id):
    from app.controllers.main_controller import ajouter_commentaire_ui
    return ajouter_commentaire_ui(id, current_user)

@main_bp.route('/taches/<int:id>/files/upload', methods=['POST'])
@token_required
def uploader_fichier_ui_route(current_user, id):
    from app.controllers.main_controller import uploader_fichier_ui
    return uploader_fichier_ui(id, current_user)
@main_bp.route('/espaces/<int:id>/membres/ajouter', methods=['POST'])
@token_required
def ajouter_membre_ui_route(current_user, id):
    from app.controllers.main_controller import ajouter_membre_ui
    return ajouter_membre_ui(id, current_user)

@main_bp.route('/membres/<int:id>/retirer', methods=['POST'])
@token_required
def retirer_membre_ui_route(current_user, id):
    from app.controllers.main_controller import retirer_membre_ui
    return retirer_membre_ui(id, current_user)

@main_bp.route('/membres/<int:id>/role', methods=['POST'])
@token_required
def changer_role_membre_ui_route(current_user, id):
    from app.controllers.main_controller import changer_role_membre_ui
    return changer_role_membre_ui(id, current_user)

@main_bp.route('/admin/creer-user', methods=['POST'])
@token_required
def creer_user_ui_route(current_user):
    from app.controllers.main_controller import creer_user_ui
    return creer_user_ui(current_user)

@main_bp.route('/admin/users')
@token_required
def admin_users_route(current_user):
    from app.controllers.main_controller import liste_utilisateurs_ui
    return liste_utilisateurs_ui(current_user)
