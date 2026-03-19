from app import db

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    espace_id = db.Column(db.Integer, db.ForeignKey('espace.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)