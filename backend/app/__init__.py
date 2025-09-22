# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Habilita CORS
    CORS(app)

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # Registra rotas
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

