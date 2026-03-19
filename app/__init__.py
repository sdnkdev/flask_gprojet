from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.user import User
    from app.models.projet import Projet
    from app.models.tache import Tache
    from app.models.file import File
    from app.models.commentaire import Commentaire
    from app.models.espace import Espace
    from app.models.membre import Membre

    from app.routes.espace_routes import espace_bp
    from app.routes.projet_routes import projet_bp
    from app.routes.tache_routes import tache_bp
    from app.routes.commentaire_routes import commentaire_bp
    from app.routes.file_routes import file_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    
    app.register_blueprint(espace_bp)
    app.register_blueprint(projet_bp)
    app.register_blueprint(tache_bp)
    app.register_blueprint(commentaire_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app


