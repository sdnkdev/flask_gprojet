from flask import render_template
from datetime import datetime
from app.models.espace import Espace
from app.models.projet import Projet
from app.models.tache import Tache
from app.models.commentaire import Commentaire
from app.models.file import File
from app.models.membre import Membre

def home(current_user):
  
    if current_user.role == 'admin':
        espaces_count = Espace.query.count()
        projets_count = Projet.query.count()
        taches_count = Tache.query.filter_by(assigned_user_id=current_user.id).count() 
    else:
        memberships = Membre.query.filter_by(user_id=current_user.id).all()
        espace_ids = [m.espace_id for m in memberships]
        espaces_count = len(memberships)
        projets_count = Projet.query.filter(Projet.espace_id.in_(espace_ids)).count() if espace_ids else 0
        taches_count = Tache.query.filter_by(assigned_user_id=current_user.id).count()
    
   
    recent_tasks = Tache.query.filter_by(assigned_user_id=current_user.id).order_by(Tache.date_creation.desc()).limit(5).all()
    
    return render_template("home.html", 
                           user=current_user, 
                           espaces_count=espaces_count,
                           projets_count=projets_count,
                           taches_count=taches_count,
                           recent_tasks=recent_tasks)

def list_espaces(current_user):
    if current_user.role == 'admin':
        espaces = Espace.query.all()
        # On donne le rôle virtuel admin à l'utilisateur pour tous les espaces
        espaces_with_roles = [(e, 'admin') for e in espaces]
    else:
        memberships = Membre.query.filter_by(user_id=current_user.id).all()
        espaces_with_roles = [(m.espace, m.role) for m in memberships]
        
    return render_template("espaces.html", user=current_user, espaces_with_roles=espaces_with_roles)

def creer_espace_ui(current_user):
    from flask import request, redirect, url_for, flash
    from app.services.espace_service import creer_espace
    
    nom = request.form.get('nom')
    description = request.form.get('description')
    
    if not nom:
        flash("Le nom de l'espace est requis.", "danger")
        return redirect(url_for('main.espaces_route'))
        
    try:
        res, status = creer_espace({"nom": nom, "description": description}, current_user.id)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Espace créé avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.espaces_route'))

def list_projets_espace(espace_id, current_user):
    
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=espace_id).first()
    if not membre and current_user.role != 'admin':
        return "Accès refusé", 403
    
    role = 'admin' if current_user.role == 'admin' else membre.role
    
    espace = Espace.query.get(espace_id)
    projets = Projet.query.filter_by(espace_id=espace_id).all()
    # Récupérer tous les membres de l'espace pour l'affichage
    memberships = Membre.query.filter_by(espace_id=espace_id).all()

    return render_template("projets.html", user=current_user, espace=espace, projets=projets, role=role, memberships=memberships)

def creer_projet_ui(espace_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.projet_service import creer_projet
    
    data = {
        "titre": request.form.get('titre'),
        "description": request.form.get('description'),
        "espace_id": espace_id
    }
    
   
    try:
        d_debut = request.form.get('date_debut')
        d_fin = request.form.get('date_fin')
        if d_debut:
            data['date_debut'] = datetime.strptime(d_debut, '%Y-%m-%d').strftime('%d-%m-%Y')
        if d_fin:
            data['date_fin'] = datetime.strptime(d_fin, '%Y-%m-%d').strftime('%d-%m-%Y')
    except:
        flash("Format de date invalide", "danger")
        return redirect(url_for('main.espace_projets_route', id=espace_id))

 
    d_debut_dt = datetime.strptime(request.form.get('date_debut'), '%Y-%m-%d').date()
    d_fin_dt = datetime.strptime(request.form.get('date_fin'), '%Y-%m-%d').date()
    if d_fin_dt < d_debut_dt:
        flash("La date de fin ne peut pas être antérieure à la date de début", "danger")
        return redirect(url_for('main.espace_projets_route', id=espace_id))

    try:
        res, status = creer_projet(data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Projet créé avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.espace_projets_route', id=espace_id))

def projet_details(projet_id, current_user):
    projet = Projet.query.get(projet_id)
    if not projet:
        return "Projet non trouvé", 404
        
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre and current_user.role != 'admin':
        return "Accès refusé", 403
        
    role = 'admin' if current_user.role == 'admin' else membre.role
    taches = Tache.query.filter_by(projet_id=projet_id).all()
   
    memberships = Membre.query.filter_by(espace_id=projet.espace_id).all()
    membres = [m.user for m in memberships]
    
    return render_template("projet_details.html", user=current_user, projet=projet, taches=taches, role=role, membres=membres)

def tache_details(tache_id, current_user):
    tache = Tache.query.get(tache_id)
    if not tache:
        return "Tâche non trouvée", 404
        
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre and current_user.role != 'admin':
        return "Accès refusé", 403
        
    commentaires = Commentaire.query.filter_by(tache_id=tache_id).all()
    files = File.query.filter_by(tache_id=tache_id).all()
    
    # Get members for task assignment
    memberships = Membre.query.filter_by(espace_id=projet.espace_id).all()
    project_members = [m.user for m in memberships]
    
    return render_template("tache_details.html", user=current_user, tache=tache, projet=projet, commentaires=commentaires, files=files, project_members=project_members)

def commentaire_details(commentaire_id, current_user):
    com = Commentaire.query.get(commentaire_id)
    if not com:
        return "Commentaire non trouvé", 404
        
    tache = Tache.query.get(com.tache_id)
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre and current_user.role != 'admin':
        return "Accès refusé", 403
 
    return render_template("commentaire_details.html", user=current_user, commentaire=com, tache=tache)

def file_details(file_id, current_user):
    f = File.query.get(file_id)
    if not f:
        return "Fichier non trouvé", 404
    
    tache = Tache.query.get(f.tache_id)
    projet = Projet.query.get(tache.projet_id)
    membre = Membre.query.filter_by(user_id=current_user.id, espace_id=projet.espace_id).first()
    if not membre and current_user.role != 'admin':
        return "Accès refusé", 403
        
    return render_template("file_details.html", user=current_user, file=f, tache=tache)

def modifier_espace_ui(espace_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.espace_service import modifier_espace
    data = {"nom": request.form.get('nom'), "description": request.form.get('description')}
    try:
        res, status = modifier_espace(espace_id, data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Espace modifié avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.espaces_route'))

def supprimer_espace_ui(espace_id, current_user):
    from flask import redirect, url_for, flash
    from app.services.espace_service import supprimer_espace
    try:
        res, status = supprimer_espace(espace_id, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Espace supprimé avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.espaces_route'))

def modifier_projet_ui(projet_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.projet_service import modifier_projet
    data = {"titre": request.form.get('titre'), "description": request.form.get('description')}
    if request.form.get('date_debut'): data['date_debut'] = request.form.get('date_debut')
    if request.form.get('date_fin'): data['date_fin'] = request.form.get('date_fin')
    try:
        res, status = modifier_projet(projet_id, data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Projet modifié avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.projet_details_route', id=projet_id))

def supprimer_projet_ui(projet_id, current_user):
    from flask import redirect, url_for, flash
    from app.services.projet_service import supprimer_projet
    projet = Projet.query.get(projet_id)
    espace_id = projet.espace_id if projet else None
    try:
        res, status = supprimer_projet(projet_id, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Projet supprimé avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.espace_projets_route', id=espace_id)) if espace_id else redirect(url_for('main.espaces_route'))

def creer_tache_ui(projet_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.tache_service import creer_tache
    data = {
        "titre": request.form.get('titre'),
        "description": request.form.get('description'),
        "projet_id": projet_id,
        "assigned_user_id": request.form.get('assigned_user_id')
    }
    try:
        d_debut, d_fin = request.form.get('date_debut'), request.form.get('date_fin')
        if d_debut: data['date_debut'] = datetime.strptime(d_debut, '%Y-%m-%d').strftime('%d-%m-%Y')
        if d_fin: data['date_fin'] = datetime.strptime(d_fin, '%Y-%m-%d').strftime('%d-%m-%Y')
        res, status = creer_tache(data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Tâche créée avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.projet_details_route', id=projet_id))

def profil_ui(current_user):
    return render_template("profil.html", user=current_user)

def liste_utilisateurs_ui(current_user):
    from app.services.admin_service import lister_tous_les_utilisateurs
    if current_user.role != 'admin':
        return "Accès refusé", 403
        
    users, status = lister_tous_les_utilisateurs(current_user.id)
    if status >= 400:
        users = []
        
    return render_template("admin_users.html", user=current_user, company_users=users)

def modifier_tache_ui(tache_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.tache_service import modifier_tache
    data = {
        "titre": request.form.get('titre'),
        "description": request.form.get('description'),
        "status": request.form.get('status'),
        "assigned_user_id": request.form.get('assigned_user_id')
    }
    try:
        d_debut, d_fin = request.form.get('date_debut'), request.form.get('date_fin')
        if d_debut: data['date_debut'] = datetime.strptime(d_debut, '%Y-%m-%d').strftime('%d-%m-%Y')
        if d_fin: data['date_fin'] = datetime.strptime(d_fin, '%Y-%m-%d').strftime('%d-%m-%Y')
        res, status = modifier_tache(tache_id, data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Tâche modifiée avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.tache_details_route', id=tache_id))

def supprimer_tache_ui(tache_id, current_user):
    from flask import redirect, url_for, flash
    from app.services.tache_service import supprimer_tache
    tache = Tache.query.get(tache_id)
    projet_id = tache.projet_id if tache else None
    try:
        res, status = supprimer_tache(tache_id, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Tâche supprimée avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.projet_details_route', id=projet_id)) if projet_id else redirect(url_for('main.espaces_route'))

def ajouter_commentaire_ui(tache_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.commentaire_service import ajouter_commentaire
    data = {
        "contenu": request.form.get('contenu'),
        "tache_id": tache_id
    }
    try:
        res, status = ajouter_commentaire(data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Commentaire ajouté !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.tache_details_route', id=tache_id))

def uploader_fichier_ui(tache_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.file_service import ajouter_fichier
    
    data = {
        "nom_file": request.form.get('nom_file'),
        "url": request.form.get('url'),
        "type_file": request.form.get('type_file'),
        "tache_id": tache_id
    }
    try:
        res, status = ajouter_fichier(data, current_user)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Fichier ajouté !", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('main.tache_details_route', id=tache_id))
def ajouter_membre_ui(espace_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.membre_service import ajouter_membre_espace
    
    email = request.form.get('email')
    role = request.form.get('role', 'user')
    
    try:
        res, status = ajouter_membre_espace(espace_id, email, role, current_user.id)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Membre ajouté avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.espace_projets_route', id=espace_id))

def retirer_membre_ui(membre_id, current_user):
    from flask import redirect, url_for, flash
    from app.services.membre_service import retirer_membre_espace
    
    membre = Membre.query.get(membre_id)
    espace_id = membre.espace_id if membre else None
    
    try:
        res, status = retirer_membre_espace(membre_id, current_user.id)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Membre retiré avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.espace_projets_route', id=espace_id)) if espace_id else redirect(url_for('main.espaces_route'))

def changer_role_membre_ui(membre_id, current_user):
    from flask import request, redirect, url_for, flash
    from app.services.membre_service import changer_role_membre
    
    nouveau_role = request.form.get('role')
    membre = Membre.query.get(membre_id)
    espace_id = membre.espace_id if membre else None
    
    try:
        res, status = changer_role_membre(membre_id, nouveau_role, current_user.id)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Rôle mis à jour !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.espace_projets_route', id=espace_id)) if espace_id else redirect(url_for('main.espaces_route'))

def creer_user_ui(current_user):
    from flask import request, redirect, url_for, flash
    from app.services.admin_service import creer_employe
    
    data = {
        "prenom": request.form.get('prenom'),
        "nom": request.form.get('nom'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }
    
    try:
        res, status = creer_employe(data, current_user.id)
        if status >= 400:
            flash(res.get_json().get('message', 'Erreur'), "danger")
        else:
            flash("Compte employé créé avec succès !", "success")
    except Exception as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.profil_route'))
