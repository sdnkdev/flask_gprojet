from app import db
from datetime import datetime

class Commentaire(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    contenu = db.Column(db.Text,nullable=False)
    tache_id = db.Column(db.Integer, db.ForeignKey('tache.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship handled by Tache.commentaires backref
