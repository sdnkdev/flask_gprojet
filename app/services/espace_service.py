from app import db
from flask import jsonify
from app.models.espace import Espace
from app.models.membre import Membre

def creer_espace(data_user,user_id):
    nouvel_espace = Espace(
        nom=data_user.get('nom'),
        description=data_user.get('description')
    )
    db.session.add(nouvel_espace)
    db.session.flush()

    nouveau_membre = Membre(
        user_id=user_id,
        espace_id=nouvel_espace.id,
        role='admin'
    )
    db.session.add(nouveau_membre)
    db.session.commit()

    
    return jsonify({'message': 'Espace créé avec succès', 'espace_id': nouvel_espace.id}), 201

def modifier_espace(espace_id, data_user,current_user):
    espace = Espace.query.get(espace_id)
    if not espace:
        return jsonify({'message': 'Espace non trouvé'}), 404
    
    
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=espace_id).first()
    if current_user.role != 'admin' and (not membre or membre.role != 'admin'):
        return jsonify({'message': 'Accès refusé: Vous devez être un membre admin de cet espace pour le modifier'}), 403

    espace.nom = data_user.get('nom', espace.nom)
    espace.description = data_user.get('description', espace.description)
    db.session.commit()

    return jsonify({'message': 'Espace modifié avec succès'}), 200

def supprimer_espace(espace_id,current_user):
    espace = Espace.query.get(espace_id)
    if not espace:
        return jsonify({'message': 'Espace non trouvé'}), 404
    
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=espace_id).first()
    if current_user.role != 'admin' and (not membre or membre.role != 'admin'):
        return jsonify({'message': 'Accès refusé: Vous devez être un membre admin de cet espace pour le supprimer'}), 403

   
    if espace.projets:
        return jsonify({'message': 'Impossible de supprimer cet espace car il contient encore des projets. Supprimez les projets d\'abord.'}), 400
    
 
    Membre.query.filter_by(espace_id=espace_id).delete()

    db.session.delete(espace)
    db.session.commit()

    return jsonify({'message': 'Espace supprimé avec succès'}), 200