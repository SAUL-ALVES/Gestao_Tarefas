import os
from dotenv import load_dotenv

# Carregar variáveis do .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

# Configurações do banco PostgreSQL
DB_USER = os.getenv("DB_USER", "gestor_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "senha_forte123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "gestao_tarefas")

POSTGRES_URL = (
    os.getenv("DATABASE_URL") or
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

class Config:
    """
    Configuração base. Contém as configurações comuns a todos os ambientes.
    Outras classes de configuração herdarão desta.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma-chave-secreta-muito-dificil-de-adivinhar')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua_chave_super_secreta')
    SQLALCHEMY_DATABASE_URI = POSTGRES_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Configurações extras podem ser aplicadas aqui futuramente."""
        pass


class DevelopmentConfig(Config):
    """Configurações para o ambiente de desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', POSTGRES_URL)


class TestingConfig(Config):
    """Configurações para o ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', POSTGRES_URL)
    SECRET_KEY = 'chave-teste'
    JWT_SECRET_KEY = 'chave-jwt-teste'


class ProductionConfig(Config):
    """Configurações para o ambiente de produção."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', POSTGRES_URL)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
