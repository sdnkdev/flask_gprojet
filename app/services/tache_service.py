from app import db
from flask import jsonify
from app.models.tache import Tache
from app.models.projet import Projet
from app.models.membre import Membre
from datetime import datetime

def creer_tache(data, current_user):
    projet_id = data.get('projet_id')
    projet = Projet.query.get(projet_id)
    if not projet:
        return jsonify({"message": "Projet non trouvé"}), 404
    
   
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if current_user.role != 'admin' and (not membre or membre.role != 'admin'):
        return jsonify({"message": "Accès refusé : Seuls les administrateurs peuvent créer des tâches"}), 403
    
    try:
        date_debut = datetime.strptime(data.get('date_debut'), '%d-%m-%Y').date() if data.get('date_debut') else None
        date_fin = datetime.strptime(data.get('date_fin'), '%d-%m-%Y').date() if data.get('date_fin') else None
    except (ValueError, TypeError):
        return jsonify({"message": "Format de date invalide (attendu: DD-MM-YYYY)"}), 400

    nouvelle_tache = Tache(
        titre=data.get('titre'),
        description=data.get('description'),
        status=data.get('status', 'en attente'),
        date_debut=date_debut,
        date_fin=date_fin,
        projet_id=projet_id,
        assigned_user_id=data.get('assigned_user_id')
    )
    
    db.session.add(nouvelle_tache)
    db.session.commit()
    
    return jsonify({
        "message": "Tâche créée avec succès",
        "tache": {
            "id": nouvelle_tache.id,
            "titre": nouvelle_tache.titre
        }
    }), 201

def modifier_tache(tache_id, data, current_user):
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    
   
    if current_user.role != 'admin' and not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    tache.titre = data.get('titre', tache.titre)
    tache.description = data.get('description', tache.description)
    tache.status = data.get('status', tache.status)
    tache.assigned_user_id = data.get('assigned_user_id', tache.assigned_user_id)
    
    try:
        if data.get('date_debut'):
            tache.date_debut = datetime.strptime(data.get('date_debut'), '%d-%m-%Y').date()
        if data.get('date_fin'):
            tache.date_fin = datetime.strptime(data.get('date_fin'), '%d-%m-%Y').date()
    except (ValueError, TypeError):
        return jsonify({"message": "Format de date invalide"}), 400
        
    db.session.commit()
    return jsonify({"message": "Tâche modifiée avec succès"}), 200

def supprimer_tache(tache_id, current_user):
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    
    if current_user.role != 'admin' and (not membre or membre.role != 'admin'):
        return jsonify({"message": "Accès refusé : Seuls les administrateurs peuvent supprimer des tâches"}), 403
    
    
    if tache.commentaires:
        return jsonify({"message": "Impossible de supprimer cette tâche car elle contient encore des commentaires. Supprimez-les d'abord."}), 400
    if tache.files:
        return jsonify({"message": "Impossible de supprimer cette tâche car elle contient encore des fichiers. Supprimez-les d'abord."}), 400

    db.session.delete(tache)
    db.session.commit()
    return jsonify({"message": "Tâche supprimée avec succès"}), 200

def lister_taches_projet(projet_id, current_user):
    projet = Projet.query.get(projet_id)
    if not projet:
        return jsonify({"message": "Projet non trouvé"}), 404
        
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if current_user.role != 'admin' and not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    taches = Tache.query.filter_by(projet_id=projet_id).all()
    return jsonify({
        "taches": [{
            "id": t.id,
            "titre": t.titre,
            "description": t.description,
            "status": t.status,
            "date_debut": str(t.date_debut) if t.date_debut else None,
            "date_fin": str(t.date_fin) if t.date_fin else None,
            "assigned_user_id": t.assigned_user_id
        } for t in taches]
    }), 200
