# Sistema de Gestão de Tarefas

## Descrição

Este projeto é uma aplicação web completa de "Gestão de Tarefas" (To-Do List). O sistema permite que usuários se cadastrem, façam login e gerenciem suas tarefas pessoais através de uma interface limpa e reativa.

A arquitetura segue uma separação clara entre o back-end (uma API RESTful em Flask) e o front-end (uma Single Page Application em HTML, CSS e JavaScript puro), comunicando-se através de JSON e utilizando autenticação baseada em tokens JWT.

## Funcionalidades

-   **Autenticação de Usuários:** Sistema completo de registro e login com senhas criptografadas e tokens de acesso JWT.
-   **CRUD de Tarefas:** Usuários autenticados podem Criar, Ler, Atualizar e Deletar (CRUD) suas próprias tarefas.
-   **Interface Reativa:** O front-end consome a API de forma assíncrona, proporcionando uma experiência de usuário fluida, sem recarregamento de página.
-   **Segurança:** As rotas da API de tarefas são protegidas, garantindo que um usuário só possa acessar e manipular suas próprias tarefas.
-   **Paginação:** A lista de tarefas no front-end é paginada para lidar com um grande número de itens de forma eficiente.

## Tecnologias Utilizadas

### **Back-end**
-   **Python 3.11**
-   **Flask:** Micro-framework web para a construção da API.
-   **Flask-SQLAlchemy:** ORM para interação com o banco de dados.
-   **Flask-JWT-Extended:** Para implementação da autenticação com JSON Web Tokens.
-   **Werkzeug:** Para hashing de senhas.

### **Front-end**
-   **HTML5**
-   **CSS3:** Estilização moderna com Flexbox.
-   **JavaScript (ES6+):** Manipulação da DOM e consumo da API com a `Fetch API` (`async/await`).

### **Banco de Dados**
-   **PostgreSQL** 

## Como Executar o Projeto

Siga os passos abaixo para rodar o projeto em sua máquina local.

### **Pré-requisitos**

-   [Python 3.9+](https://www.python.org/downloads/)
-   `pip` (gerenciador de pacotes do Python)
-   Um banco de dados relacional (PostgreSQL ou MySQL) instalado e em execução.

### **1. Clonando o Repositório**
```bash
git clone https://github.com/SAUL-ALVES/Gestao_Tarefas.git
cd Gestao_Tarefas
```

### **2. Configuração do Back-end**

```bash
# Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente
# Use o arquivo .env.example como modelo
```
**Conteúdo do arquivo `.env`:**
```
# Chave secreta para o JWT. Use um gerador de chaves aleatórias.
JWT_SECRET_KEY='sua-chave-super-secreta-aqui'

# URI de conexão com o seu banco de dados
# Exemplo para PostgreSQL:
# DATABASE_URI='postgresql://usuario:senha@localhost/nome_do_banco'
# Exemplo para MySQL:
# DATABASE_URI='mysql+pymysql://usuario:senha@localhost/nome_do_banco'
DATABASE_URI='sua-uri-de-conexao-aqui'
```

### **3. Executando o Back-end**
Com o ambiente virtual ativado, inicie o servidor Flask:
```bash
python run.py
```
A API estará disponível em `http://127.0.0.1:5000`.

### **4. Executando o Front-end**
A forma mais simples é usar a extensão **Live Server** no Visual Studio Code.
1. Abra a pasta `frontend` no VS Code.
2. Clique com o botão direito no arquivo `index.html`.
3. Selecione "Open with Live Server".

O front-end abrirá no seu navegador, pronto para se comunicar com a API.

## Documentação da API

A API base está localizada em `/api`.

### Autenticação

| Método | Endpoint             | Descrição                                | Corpo da Requisição (JSON)                                    | Resposta de Sucesso (201 ou 200)                         |
| :----- | :------------------- | :--------------------------------------- | :------------------------------------------------------------ | :------------------------------------------------------ |
| `POST` | `/auth/register`     | Registra um novo usuário.                | `{ "nome": "Seu Nome", "email": "teste@email.com", "senha": "123" }` | `{"msg": "Usuário registrado com sucesso!"}`             |
| `POST` | `/auth/login`        | Autentica um usuário e retorna um token. | `{ "email": "teste@email.com", "senha": "123" }`                | `{"access_token": "seu.jwt.token"}`                      |

---
### Tarefas (Rotas Protegidas)
**Observação:** Todas as requisições para estes endpoints devem incluir o cabeçalho: `Authorization: Bearer <seu.jwt.token>`

| Método   | Endpoint             | Descrição                                 | Corpo da Requisição (JSON)                                                                  | Resposta de Sucesso (200 ou 201)                                |
| :------- | :------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------ | :-------------------------------------------------------------- |
| `GET`    | `/tarefas`           | Lista todas as tarefas do usuário logado. | N/A                                                                                         | `[ { "id": 1, "titulo": "Minha Tarefa", ... }, ... ]`             |
| `POST`   | `/tarefas`           | Cria uma nova tarefa.                     | `{ "titulo": "Nova Tarefa", "descricao": "Detalhes" }`                                        | `{ "id": 2, "titulo": "Nova Tarefa", ... }`                     |
| `PUT`    | `/tarefas/<id_tarefa>` | Atualiza uma tarefa existente.            | `{ "titulo": "Título Atualizado", "concluida": true }`                                        | `{ "id": 2, "titulo": "Título Atualizado", ... }`               |
| `DELETE` | `/tarefas/<id_tarefa>` | Deleta uma tarefa específica.             | N/A                                                                                         | `{"msg": "Tarefa deletada com sucesso"}`                         |
