"""
Arquivo de testes para a API de Gestão de Tarefas.

Este arquivo contém testes para as funcionalidades de autenticação de usuários
e para o CRUD (Create, Read, Update, Delete) de tarefas.
Os testes utilizam um banco de dados SQLite em memória para garantir
o isolamento completo entre cada execução de teste.
"""

import pytest
import json
from app import create_app, db

# --- Configuração do Ambiente de Teste ---

@pytest.fixture(scope='function')
def test_client():
    """
    Configura o cliente de teste para a aplicação Flask usando o padrão de factory.
    Usa um banco de dados em memória (SQLite) para garantir que cada teste seja isolado.
    """
    app = create_app('testing')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

# --- Funções Auxiliares (Helpers) ---

def get_auth_token(test_client, email='teste@exemplo.com', senha='123', nome='Usuário Teste'):
    """
    Função auxiliar para registrar, logar e obter um token de autenticação.
    Padronizada para usar o parâmetro 'json'.
    """
    # Registra um novo usuário
    test_client.post('/api/auth/register', json={'nome': nome, 'email': email, 'senha': senha})
    
    # Faz o login para obter o token
    response = test_client.post('/api/auth/login', json={'email': email, 'senha': senha})
    
    return response.get_json()['access_token']

def create_task(test_client, headers, payload):
    """
    Função auxiliar para criar uma tarefa.
    Retorna a resposta completa da requisição POST.
    """
    return test_client.post('/api/tarefas', json=payload, headers=headers)

# --- Testes de Autenticação ---

def test_registro_usuario(test_client):
    """
    Testa o endpoint de registro de um novo usuário.
    Verifica se o usuário é criado com sucesso (status 201).
    """
    payload = {
        'nome': 'Usuário Teste',
        'email': 'teste@exemplo.com',
        'senha': 'senha123'
    }
    response = test_client.post('/api/auth/register', json=payload)
    
    assert response.status_code == 201
    assert response.get_json()['msg'] == "Usuário registrado com sucesso!"

def test_registro_usuario_email_existente(test_client):
    """
    Testa a tentativa de registro com um e-mail que já existe.
    Verifica se a API retorna um erro de conflito (status 409).
    """
    user_payload = {'nome': 'Usuário Existente', 'email': 'existente@exemplo.com', 'senha': '123'}
    test_client.post('/api/auth/register', json=user_payload)
    
    # Tenta registrar novamente com o mesmo e-mail
    response = test_client.post('/api/auth/register', json=user_payload)
    
    assert response.status_code == 409
    assert response.get_json()['msg'] == "Este email já está em uso"

def test_login_usuario(test_client):
    """
    Testa o endpoint de login.
    Verifica se o login é bem-sucedido e retorna um token de acesso.
    """
    user_payload = {'nome': 'Login Teste', 'email': 'login@exemplo.com', 'senha': 'senha123'}
    test_client.post('/api/auth/register', json=user_payload)
    
    login_payload = {'email': 'login@exemplo.com', 'senha': 'senha123'}
    response = test_client.post('/api/auth/login', json=login_payload)
    
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_credenciais_invalidas(test_client):
    """
    Testa o login com senha incorreta.
    Verifica se a API retorna um erro de não autorizado (status 401).
    """
    user_payload = {'nome': 'Login Teste', 'email': 'login@exemplo.com', 'senha': 'senha123'}
    test_client.post('/api/auth/register', json=user_payload)

    login_payload = {'email': 'login@exemplo.com', 'senha': 'senha_errada'}
    response = test_client.post('/api/auth/login', json=login_payload)
    
    assert response.status_code == 401
    assert response.get_json()['msg'] == "Credenciais inválidas"

# --- Testes do CRUD de Tarefas ---

def test_criar_tarefa(test_client):
    """
    Testa a criação de uma nova tarefa para um usuário autenticado.
    Verifica o status 201 e se os dados retornados estão corretos.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    
    task_payload = {
        "titulo": "Minha primeira tarefa",
        "descricao": "Descrição da tarefa de teste.",
        "concluida": False 
    }
    
    response = create_task(test_client, headers, task_payload)

    print(f"CORPO DA RESPOSTA DE ERRO: {response.get_json()}")
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == task_payload['titulo']
    assert data['descricao'] == task_payload['descricao']
    assert data['concluida'] is False

def test_listar_tarefas(test_client):
    """
    Testa a listagem de tarefas de um usuário autenticado.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # CORREÇÃO: Adiciona uma tarefa com o payload completo e correto.
    task_payload = {"titulo": "Tarefa para listar", "descricao": "Detalhes", "concluida": False}
    create_task(test_client, headers, task_payload)

    response = test_client.get('/api/tarefas', headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['titulo'] == task_payload['titulo']

def test_atualizar_tarefa(test_client):
    """
    Testa a atualização de uma tarefa existente.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}

    # CORREÇÃO: Cria a tarefa inicial com um payload completo.
    initial_payload = {"titulo": "Tarefa original", "descricao": "Descrição original", "concluida": False}
    res_post = create_task(test_client, headers, initial_payload)
    id_tarefa = res_post.get_json()['id']

    # CORREÇÃO: Atualiza a tarefa usando o parâmetro 'json'.
    update_payload = {"titulo": "Tarefa atualizada", "concluida": True}
    response = test_client.put(f'/api/tarefas/{id_tarefa}', json=update_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == update_payload['titulo']
    assert data['concluida'] is True
    assert data['descricao'] == initial_payload['descricao'] # Descrição não foi alterada

def test_deletar_tarefa(test_client):
    """
    Testa a exclusão de uma tarefa.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}

    # CORREÇÃO: Cria a tarefa para deletar com um payload completo.
    task_payload = {"titulo": "Tarefa a ser deletada", "descricao": "...", "concluida": False}
    res_post = create_task(test_client, headers, task_payload)
    id_tarefa = res_post.get_json()['id']

    # Deleta a tarefa
    response = test_client.delete(f'/api/tarefas/{id_tarefa}', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['msg'] == "Tarefa deletada com sucesso"

    # Verifica se a tarefa realmente foi deletada
    res_get = test_client.get('/api/tarefas', headers=headers)
    data = res_get.get_json()
    assert len(data) == 0