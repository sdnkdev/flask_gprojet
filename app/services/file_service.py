from app import db
from flask import jsonify
from app.models.file import File
from app.models.tache import Tache
from app.models.projet import Projet
from app.models.membre import Membre

def ajouter_fichier(data, current_user):
    tache_id = data.get('tache_id')
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    nouveau_file = File(
        nom=data.get('nom_file'),
        url=data.get('url', ''),
        type_file=data.get('type_file'),
        tache_id=tache_id,
        user_id=current_user.id
    )
    
    db.session.add(nouveau_file)
    db.session.commit()
    
    return jsonify({"message": "Fichier ajouté avec succès"}), 201

def lister_fichiers_tache(tache_id, current_user):
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    files = File.query.filter_by(tache_id=tache_id).all()
    return jsonify({
        "fichiers": [{
            "id": f.id,
            "nom": f.nom,
            "url": f.url,
            "type": f.type_file,
            "date_creation": str(f.date_creation),
            "uploader_id": f.user_id
        } for f in files]
    })

def supprimer_fichier(id, current_user):
    f = File.query.get(id)
    if not f:
        return jsonify({"message": "Fichier non trouvé"}), 404
        
    tache = Tache.query.get(f.tache_id)
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    
    if not (f.user_id == current_user.id or (membre and membre.role == 'admin')):
        return jsonify({"message": "Accès refusé"}), 403
        
    db.session.delete(f)
    db.session.commit()
    return jsonify({"message": "Fichier supprimé"}), 200


