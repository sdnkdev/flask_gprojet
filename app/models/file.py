from app import db
from datetime import datetime

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(100), nullable=False)
    url=db.Column(db.String(200), nullable=False)
    type_file=db.Column(db.String(50), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tache_id = db.Column(db.Integer, db.ForeignKey('tache.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship handled by Tache.files backref
