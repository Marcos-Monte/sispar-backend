from os import environ
from dotenv import load_dotenv

load_dotenv()

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
