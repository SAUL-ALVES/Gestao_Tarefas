import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuração base. Contém as configurações comuns a todos os ambientes.
    Outras classes de configuração herdarão desta.
    """
  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        Método estático para realizar configurações específicas da aplicação, se necessário.
        Pode ser expandido no futuro.
        """
        pass

class DevelopmentConfig(Config):
    """
    Configurações para o ambiente de desenvolvimento.
    Herda da classe Config base e sobrescreve algumas variáveis.
    """
    
    DEBUG = True


    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    """
    Configurações para o ambiente de testes.
    """
    
    TESTING = True

    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
    SECRET_KEY = 'chave-teste'
    JWT_SECRET_KEY = 'chave-jwt-teste'
class ProductionConfig(Config):
    """
    Configurações para o ambiente de produção.
    """
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

   
    'default': DevelopmentConfig
}