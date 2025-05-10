# Responsavel pela criação da aplicação
# Create_app() -> Vai configurar a instancia do Flask
from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db # Importa a instância do banco de dados
from config import Config # Importa a classe de configuração

from flask_cors import CORS # Importa a classe do CORS -> Configuração sempre após a instancia do flask

from flasgger import Swagger # Importando a classe Swagger

import os # Interação com o sistema operacional. Manipulação de diretórios, arquivos, processos e outros

swagger_config = {
    "headers": [], # Questões de autorizações serão indicadas aqui ->  Não temos configurações de autorização por isso a lista vazia
    "specs": [ # Especificações da documentação
        {
            "endpoint": "apispec", # <-- Da um nome de referencia para a documentacao
            "route": "/apispec.json/", # <- Rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True, # <-- Todas as rotas/endpoints serão documentados
            "model_filter": lambda tag: True, # <-- Especificar quuais modelos da entidade serão documentados
        }
    ],
    "static_url_path": "/flasgger_static", # Podemos estilizar o documento do Swagger através desta rota
    "swagger_ui": True, # UI = User Interface ->  Indica se a interface será ou não visível
    "specs_route": "/apidocs/" # URL onde estará disponível a documentação
}

def create_app():
    # app = Flask(__name__)  # <-- carrega a instancia do Flask
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')) # Indica o caminho da pasta 'static' para o Flask
    )
    
    CORS(app, origins=['http://localhost:5173', 'https://sispar-iota.vercel.app'] ) # A politica de CORS seja implementada em TODA a aplicação (todas as rotas vão aceitar requisições dos endereços indicados) # Lista de origens (asterico libera qualquer requisição)
    
    app.register_blueprint(bp_colaborador) # Registra o blueprint -> colaborador
    app.register_blueprint(bp_reembolso) # Registra o blueprint -> reembolso
    
    app.config.from_object(Config) # Traz a configuração do ambiente de desenvolvimento
    db.init_app(app) # Inicia a conexão com o Banco de Dados
    
    Swagger(app, config=swagger_config) # Configuração do Swagger
    
    with app.app_context():
        db.create_all() # Cria as tabelas caso elas não existam
    
    return app

