from app import db
from flask import jsonify
from app.models.commentaire import Commentaire
from app.models.tache import Tache
from app.models.projet import Projet
from app.models.membre import Membre

def ajouter_commentaire(data, current_user):
    tache_id = data.get('tache_id')
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    nouveau_commentaire = Commentaire(
        contenu=data.get('contenu'),
        tache_id=tache_id,
        user_id=current_user.id
    )
    
    db.session.add(nouveau_commentaire)
    db.session.commit()
    
    return jsonify({"message": "Commentaire ajouté avec succès"}), 201

def lister_commentaires_tache(tache_id, current_user):
    tache = Tache.query.get(tache_id)
    if not tache:
        return jsonify({"message": "Tâche non trouvée"}), 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre:
        return jsonify({"message": "Accès refusé"}), 403
        
    commentaires = Commentaire.query.filter_by(tache_id=tache_id).all()
    return jsonify({
        "commentaires": [{
            "id": c.id,
            "contenu": c.contenu,
            "date_creation": str(c.date_creation),
            "author_id": c.user_id
        } for c in commentaires]
    })

def supprimer_commentaire(id, current_user):
    com = Commentaire.query.get(id)
    if not com:
        return jsonify({"message": "Commentaire non trouvé"}), 404
        
   
    tache = Tache.query.get(com.tache_id)
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    
    if not (com.user_id == current_user.id or (membre and membre.role == 'admin')):
        return jsonify({"message": "Accès refusé"}), 403
        
    db.session.delete(com)
    db.session.commit()
    return jsonify({"message": "Commentaire supprimé"}), 200
