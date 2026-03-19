from app import db

class Projet(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    titre=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text,nullable=True)
    date_debut=db.Column(db.Date,nullable=False)
    date_fin=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(20),nullable=False,default='en attente')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    espace_id=db.Column(db.Integer,db.ForeignKey('espace.id'),nullable=False)
    espace = db.relationship('Espace', backref='projets', lazy=True)
    taches = db.relationship('Tache', backref='projet', lazy=True, cascade='all, delete-orphan')


