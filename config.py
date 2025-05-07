# Importa o objeto 'environ' para acessar variáveis de ambiente do sistema
from os import environ

# Importa a função 'load_dotenv' para carregar variáveis de ambiente definidas em um arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para serem acessíveis via 'environ'
load_dotenv()

# Classe de configuração principal da aplicação
class Config:
    ENV = environ.get("FLASK_ENV", "development")
    
    if ENV == 'production':
        # Em produção, usa a variável que está configurada diretamente no Render
        SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')
    else: 
        # Em desenvolvimento, usa a variável do .env local
        SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV")
        
    # Desativa a funcionalidade de rastreamento de modificações de objetos para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
