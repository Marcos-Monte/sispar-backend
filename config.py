# Importa o objeto 'environ' para acessar variáveis de ambiente do sistema
from os import environ

# Importa a função 'load_dotenv' para carregar variáveis de ambiente definidas em um arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para serem acessíveis via 'environ'
load_dotenv()

# Exibe no terminal a URI do banco de dados que foi carregada das variáveis de ambiente
print("URI do banco:", environ.get('URL_DATABASE_DEV'))

# Classe de configuração principal da aplicação
class Config:
    # Define a URI do banco de dados que será usada pela extensão SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV')
    
    # Desativa a funcionalidade de rastreamento de modificações de objetos para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
