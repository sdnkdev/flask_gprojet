from app import db
from flask import jsonify
from app.models.projet import Projet
from app.models.membre import Membre
from datetime import datetime

def creer_projet(data, current_user):
    espace_id = data.get('espace_id')
    
   
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé : Vous n'êtes pas membre de cet espace"}), 403
    
   
    try:
        date_debut = datetime.strptime(data.get('date_debut'), '%d-%m-%Y').date()
        date_fin = datetime.strptime(data.get('date_fin'), '%d-%m-%Y').date()

        
    except (ValueError, TypeError):
        return jsonify({"message": "Format de date invalide (attendu: DD-MM-YYYY)"}), 400

    if date_fin < date_debut:
        return jsonify({"message": "La date de fin ne peut pas être antérieure à la date de début"}), 400

    nouveau_projet = Projet(
        titre=data.get('titre'),
        description=data.get('description'),
        date_debut=date_debut,
        date_fin=date_fin,
        user_id=current_user.id,
        espace_id=espace_id
    )
    
    db.session.add(nouveau_projet)
    db.session.commit()
    
    return jsonify({
        "message": "Projet créé avec succès",
        "projet": {
            "id": nouveau_projet.id,
            "titre": nouveau_projet.titre
        }
    }), 201

def modifier_projet(projet_id, data, current_user):
    projet = Projet.query.get(projet_id)
    if not projet:
        return jsonify({"message": "Projet non trouvé"}), 404
    
    
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not (projet.user_id == current_user.id or (membre and membre.role == 'admin')):
        return jsonify({"message": "Accès refusé : Vous n'avez pas les droits de modification"}), 403
    
    projet.titre = data.get('titre', projet.titre)
    projet.description = data.get('description', projet.description)
    
    if data.get('date_debut'):
        projet.date_debut = datetime.strptime(data.get('date_debut'), '%Y-%m-%d').date()
    if data.get('date_fin'):
        projet.date_fin = datetime.strptime(data.get('date_fin'), '%Y-%m-%d').date()
        
    db.session.commit()
    
    return jsonify({"message": "Projet modifié avec succès"}), 200

def supprimer_projet(projet_id, current_user):
    projet = Projet.query.get(projet_id)
    if not projet:
        return jsonify({"message": "Projet non trouvé"}), 404
    
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not (projet.user_id == current_user.id or (membre and membre.role == 'admin')):
        return jsonify({"message": "Accès refusé : Vous n'avez pas les droits de suppression"}), 403
    
   
    if projet.taches:
        return jsonify({"message": "Impossible de supprimer ce projet car il contient encore des tâches. Supprimez les tâches d'abord."}), 400

    db.session.delete(projet)
    db.session.commit()
    
    return jsonify({"message": "Projet supprimé avec succès"}), 200

def lister_projets_espace(espace_id, current_user):
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    projets = Projet.query.filter_by(espace_id=espace_id).all()
    return jsonify({
        "projets": [{
            "id": p.id,
            "titre": p.titre,
            "description": p.description,
            "date_debut": str(p.date_debut),
            "date_fin": str(p.date_fin),
            "status": p.status
        } for p in projets]
    }) , 200
