import os
from flask import Flask
from flask_cors import CORS 
from flasgger import Swagger 
from config import Config 
from src.model import db 
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso


swagger_config = {
    "headers": [], # Configurações e Autorizações
    "specs": [ # Especificações da documentação
        {
            "endpoint": "apispec", 
            "route": "/apispec.json/", 
            "rule_filter": lambda rule: True, 
            "model_filter": lambda tag: True, 
        }
    ],
    "static_url_path": "/flasgger_static", 
    "swagger_ui": True, 
    "specs_route": "/apidocs/" 
}

def create_app():

    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')) 
    )
    
    CORS(app, origins=['http://localhost:5173', 'https://sispar-iota.vercel.app'] )
    
    # Registros de Blueprints
    app.register_blueprint(bp_colaborador) 
    app.register_blueprint(bp_reembolso) 
    
    app.config.from_object(Config) # Traz a configuração do ambiente de desenvolvimento
    db.init_app(app) # Inicia a conexão com o Banco de Dados
    
    Swagger(app, config=swagger_config) # Configuração do Swagger
    
    with app.app_context():
        db.create_all() # Cria as tabelas caso elas não existam
    
    return app

