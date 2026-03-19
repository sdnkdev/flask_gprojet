from app import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nom = db.Column(db.String(100),nullable=False)
    prenom = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    mot_de_passe = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(100),nullable=False, default='user')
    projets = db.relationship('Projet', backref='author', lazy=True)
    assigned_tasks = db.relationship('Tache', backref='assigned_user', lazy=True)
    commentaires = db.relationship('Commentaire', backref='author', lazy=True)
    files = db.relationship('File', backref='uploader', lazy=True)
    memberships = db.relationship('Membre', backref='user', lazy=True)

    