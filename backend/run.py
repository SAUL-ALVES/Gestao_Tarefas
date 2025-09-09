from app import create_app, db
from app.models import Tarefa


app = create_app('default')

@app.shell_context_processor
def make_shell_context():
    """
    Cria um contexto de shell que adiciona a instância do banco de dados e os modelos
    ao escopo do shell, facilitando o teste e a depuração.

    Para usar, execute no terminal: flask shell
    """
    return dict(db=db, Task=Task)

if __name__ == '__main__':
    """
    Ponto de entrada principal para a execução da aplicação.
    Este bloco de código será executado apenas quando o script for chamado diretamente.
    """

    app.run(debug=True)