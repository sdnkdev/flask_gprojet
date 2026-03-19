from app import db

class Espace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    membre = db.relationship('Membre', backref='espace', lazy=True)