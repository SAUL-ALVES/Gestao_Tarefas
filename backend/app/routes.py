from flask import request, jsonify, Blueprint
from .models import db, Usuario, Tarefa
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


api = Blueprint('api', __name__)


@api.route('/auth/register', methods=['POST'])
def registrar_usuario():
    dados = request.get_json()
    if not dados or not 'email' in dados or not 'senha' in dados or not 'nome' in dados:
        return jsonify({"msg": "Campos 'nome', 'email' e 'senha' são obrigatórios"}), 400

    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({"msg": "Este email já está em uso"}), 409

    novo_usuario = Usuario(nome=dados['nome'], email=dados['email'])
    novo_usuario.set_senha(dados['senha'])
    
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"msg": "Usuário registrado com sucesso!"}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    dados = request.get_json()
    if not dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({"msg": "Campos 'email' e 'senha' são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=dados['email']).first()

    if usuario and usuario.check_senha(dados['senha']):
        access_token = create_access_token(identity=usuario.id)
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Credenciais inválidas"}), 401

# --- ROTAS DO CRUD DE TAREFAS (PROTEGIDAS) ---

@api.route('/tarefas', methods=['POST'])
@jwt_required()
def criar_tarefa():
    id_usuario_atual = get_jwt_identity()
    dados = request.get_json()
    if not dados or 'titulo' not in dados:
        return jsonify({"msg": "O campo 'titulo' é obrigatório"}), 400

    nova_tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        id_usuario=id_usuario_atual
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    return jsonify(nova_tarefa.to_dict()), 201

@api.route('/tarefas', methods=['GET'])
@jwt_required()
def listar_tarefas():
    id_usuario_atual = get_jwt_identity()
    tarefas = Tarefa.query.filter_by(id_usuario=id_usuario_atual).order_by(Tarefa.data_criacao.desc()).all()
    return jsonify([t.to_dict() for t in tarefas]), 200

@api.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
@jwt_required()
def atualizar_tarefa(id_tarefa):
    id_usuario_atual = get_jwt_identity()
    tarefa = Tarefa.query.filter_by(id=id_tarefa, id_usuario=id_usuario_atual).first_or_404()
    
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    
    db.session.commit()
    return jsonify(tarefa.to_dict()), 200

@api.route('/tarefas/<int:id_tarefa>', methods=['DELETE'])
@jwt_required()
def deletar_tarefa(id_tarefa):
    id_usuario_atual = get_jwt_identity()
    tarefa = Tarefa.query.filter_by(id=id_tarefa, id_usuario=id_usuario_atual).first_or_404()
    
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"msg": "Tarefa deletada com sucesso"}), 200