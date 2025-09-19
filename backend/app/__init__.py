# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
from flask_cors import CORS # NOVO: Importamos a biblioteca

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app) # NOVO: Dizemos ao nosso app para usar o CORS

    db.init_app(app)
    JWTManager(app)

    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app