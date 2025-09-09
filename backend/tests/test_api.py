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
    # Cria uma instância do app com a configuração de 'testing'
    app = create_app('testing') 
    
    # Cria um cliente de teste para fazer requisições
    with app.test_client() as testing_client:
        # Cria um contexto de aplicação para interagir com o app e o banco de dados
        with app.app_context():
            db.create_all()  # Cria as tabelas no banco de dados em memória
            yield testing_client  # Disponibiliza o cliente para os testes
            db.session.remove() # Garante que a sessão seja fechada
            db.drop_all()  # Limpa o banco de dados após a execução de cada teste

# --- Testes de Autenticação ---

def test_registro_usuario(test_client):
    """
    Testa o endpoint de registro de um novo usuário.
    Verifica se o usuário é criado com sucesso (status 201).
    """
    response = test_client.post('/api/auth/register',
                                data=json.dumps(dict(
                                    nome='Usuário Teste',
                                    email='teste@exemplo.com',
                                    senha='senha123'
                                )),
                                content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['msg'] == "Usuário registrado com sucesso!"

def test_registro_usuario_email_existente(test_client):
    """
    Testa a tentativa de registro com um e-mail que já existe.
    Verifica se a API retorna um erro de conflito (status 409).
    """
    # Primeiro, registra um usuário para garantir que o e-mail exista no DB limpo deste teste.
    test_client.post('/api/auth/register',
                     data=json.dumps(dict(nome='Outro Teste', email='existente@exemplo.com', senha='123')),
                     content_type='application/json')
    
    # Agora, tenta registrar com o mesmo e-mail.
    response = test_client.post('/api/auth/register',
                                data=json.dumps(dict(
                                    nome='Usuário Teste 2',
                                    email='existente@exemplo.com',
                                    senha='senha456'
                                )),
                                content_type='application/json')
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['msg'] == "Este email já está em uso"

def test_login_usuario(test_client):
    """
    Testa o endpoint de login.
    Verifica se o login é bem-sucedido e retorna um token de acesso.
    """
    # Registra um usuário para poder fazer o login.
    test_client.post('/api/auth/register',
                     data=json.dumps(dict(nome='Login Teste', email='login@exemplo.com', senha='senha123')),
                     content_type='application/json')
    
    response = test_client.post('/api/auth/login',
                                data=json.dumps(dict(
                                    email='login@exemplo.com',
                                    senha='senha123'
                                )),
                                content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_credenciais_invalidas(test_client):
    """
    Testa o login com senha incorreta.
    Verifica se a API retorna um erro de não autorizado (status 401).
    """
    # Registra o usuário para o teste de login falho.
    test_client.post('/api/auth/register',
                     data=json.dumps(dict(nome='Login Teste', email='login@exemplo.com', senha='senha123')),
                     content_type='application/json')

    response = test_client.post('/api/auth/login',
                                data=json.dumps(dict(
                                    email='login@exemplo.com',
                                    senha='senha_errada'
                                )),
                                content_type='application/json')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['msg'] == "Credenciais inválidas"

# --- Testes do CRUD de Tarefas ---

def get_auth_token(test_client, email='tarefa@exemplo.com', senha='123'):
    """Função auxiliar para registrar, logar e obter um token de autenticação."""
    test_client.post('/api/auth/register',
                     data=json.dumps(dict(nome='Tarefa Teste', email=email, senha=senha)),
                     content_type='application/json')
    response = test_client.post('/api/auth/login',
                              data=json.dumps(dict(email=email, senha=senha)),
                              content_type='application/json')
    return json.loads(response.data)['access_token']

def test_criar_tarefa(test_client):
    """
    Testa a criação de uma nova tarefa para um usuário autenticado.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = test_client.post('/api/tarefas',
                                data=json.dumps(dict(
                                    titulo='Minha primeira tarefa',
                                    descricao='Descrição da tarefa de teste.'
                                )),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['titulo'] == 'Minha primeira tarefa'

def test_listar_tarefas(test_client):
    """
    Testa a listagem de tarefas de um usuário autenticado.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # Adiciona uma tarefa para garantir que a lista não esteja vazia
    test_client.post('/api/tarefas', data=json.dumps(dict(titulo='Tarefa para listar')),
                     content_type='application/json', headers=headers)

    response = test_client.get('/api/tarefas', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['titulo'] == 'Tarefa para listar'

def test_atualizar_tarefa(test_client):
    """
    Testa a atualização de uma tarefa existente.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}

    # Cria uma tarefa para depois atualizar
    res_post = test_client.post('/api/tarefas', data=json.dumps(dict(titulo='Tarefa original')),
                                content_type='application/json', headers=headers)
    id_tarefa = json.loads(res_post.data)['id']

    # Atualiza a tarefa
    response = test_client.put(f'/api/tarefas/{id_tarefa}',
                               data=json.dumps(dict(titulo='Tarefa atualizada', concluida=True)),
                               content_type='application/json',
                               headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['titulo'] == 'Tarefa atualizada'
    assert data['concluida'] is True

def test_deletar_tarefa(test_client):
    """
    Testa a exclusão de uma tarefa.
    """
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}

    # Cria uma tarefa para depois deletar
    res_post = test_client.post('/api/tarefas', data=json.dumps(dict(titulo='Tarefa a ser deletada')),
                                content_type='application/json', headers=headers)
    id_tarefa = json.loads(res_post.data)['id']

    # Deleta a tarefa
    response = test_client.delete(f'/api/tarefas/{id_tarefa}', headers=headers)
    assert response.status_code == 200
    assert rb"Tarefa deletada com sucesso" in response.data

    # Verifica se a tarefa realmente foi deletada
    res_get = test_client.get('/api/tarefas', headers=headers)
    data = json.loads(res_get.data)
    # A lista de tarefas agora deve estar vazia.
    assert len(data) == 0