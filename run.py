# Importa a função create_app do módulo app.py dentro da pasta src
from src.app import create_app

# Cria uma instância da aplicação Flask chamando a função create_app
app = create_app()

# Verifica se o script está sendo executado diretamente (não importado como módulo)
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask
    # O modo debug=True ativa o hot reload e exibe mensagens de erro detalhadas
    app.run(debug=True)