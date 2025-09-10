from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_senha = db.Column(db.String(256), nullable=False)
    tarefas = db.relationship('Tarefa', backref='autor', lazy=True, cascade="all, delete-orphan")

    def set_senha(self, senha):
        self.hash_senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.hash_senha, senha)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email
        }

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(500), default='')
    concluida = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def to_dict(self):
        """
        Serializa o objeto Tarefa para um dicionário, facilitando a conversão para JSON.
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'concluida': self.concluida,
            'data_criacao': self.data_criacao.isoformat(),
            'id_usuario': self.id_usuario
        }