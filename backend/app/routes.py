# app/routes.py
from flask import request, jsonify, Blueprint
from .models import db, Usuario, Tarefa
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint('api', __name__)


@api.route('/tarefas', methods=['POST'])
@jwt_required()
def criar_tarefa():
    # ... (lógica de criar_tarefa atualizada para receber status e prioridade) ...
    id_usuario_atual = get_jwt_identity()
    dados = request.get_json()
    nova_tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        status=dados.get('status', 'pendente'),
        prioridade=dados.get('prioridade', 'media'),
        id_usuario=id_usuario_atual
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    return jsonify(nova_tarefa.to_dict()), 201

@api.route('/tarefas', methods=['GET'])
@jwt_required()
def listar_tarefas():
    # ATUALIZADO: Lógica de filtros, busca e paginação
    id_usuario_atual = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search_term = request.args.get('q', '', type=str)
    status_filter = request.args.get('status', 'todos', type=str)
    priority_filter = request.args.get('prioridade', 'todas', type=str)

    query = Tarefa.query.filter_by(id_usuario=id_usuario_atual)

    if search_term:
        query = query.filter(db.or_(Tarefa.titulo.ilike(f'%{search_term}%'), Tarefa.descricao.ilike(f'%{search_term}%')))
    
    if status_filter != 'todos':
        query = query.filter_by(status=status_filter)
        
    if priority_filter != 'todas':
        query = query.filter_by(prioridade=priority_filter)

    paginated_tasks = query.order_by(Tarefa.data_criacao.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'data': [t.to_dict() for t in paginated_tasks.items],
        'total': paginated_tasks.total,
        'page': paginated_tasks.page,
        'totalPages': paginated_tasks.pages
    })

@api.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
@jwt_required()
def atualizar_tarefa(id_tarefa):
    # ... (lógica de atualizar_tarefa atualizada para incluir status e prioridade) ...
    id_usuario_atual = get_jwt_identity()
    tarefa = Tarefa.query.filter_by(id=id_tarefa, id_usuario=id_usuario_atual).first_or_404()
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.status = dados.get('status', tarefa.status)
    tarefa.prioridade = dados.get('prioridade', tarefa.prioridade)
    db.session.commit()
    return jsonify(tarefa.to_dict()), 200

# ... (código de deletar_tarefa sem alterações) ...