# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    # Carrega as configurações do arquivo config.py (isto já carrega a JWT_SECRET_KEY)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Inicializa as extensões
    db.init_app(app)
    JWTManager(app)

    # Registra o Blueprint de rotas
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Cria as tabelas no banco de dados se elas não existirem
    with app.app_context():
        db.create_all()

    return app