from app import db
from datetime import datetime

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='en attente')
    date_debut=db.Column(db.Date,nullable=True)
    date_fin=db.Column(db.Date,nullable=True)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships are handled on the parent side (Projet) via backref
    files = db.relationship('File', backref='tache', lazy=True, cascade='all, delete-orphan')
    commentaires = db.relationship('Commentaire', backref='tache', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Tache {self.titre}>'
