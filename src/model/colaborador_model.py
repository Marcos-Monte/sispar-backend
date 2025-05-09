from src.model import db # Traz a instancia SQLAlchemy para este arquivo
from sqlalchemy.schema import Column # Traz recurso que transforma atributos em colunas
from sqlalchemy.types import String, DECIMAL, Integer # Traz o recurso que identifica os tipos de dados para as colunas

# Ess classe é uma abstração de todos os colaboradores
class Colaborador(db.Model): # db.Model -> Mapear e criar a tabela  
    __tablename__ = 'tb_colaborador' # Cria a tabela com o nome tb_colaborador
    
#---------------------------- Atributos da classe --------------------------
    # id INT AUTO_INCREMENT PRIMARY KEY
    id = Column(Integer, primary_key= True, autoincrement=True) # Coluna id, tipo inteiro, chave primaria com autoincremento
    
    nome = Column(String(255))
    email = Column(String(155))
    senha = Column(String(150))
    cargo = Column(String(150))
    salario = Column(DECIMAL(10,2))
    status = Column(String(100))
    foto = db.Column(db.String(255), nullable=True)
    
    # Método __init__ é um método construtor
    def __init__ (self, nome, email, senha, cargo, salario, status, foto):
        self.nome = nome 
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario
        self.status = status
        self.foto = foto
        
# -------------------------------------------------------------------------------------------------
    # Formata o tipo de dados que serão enviados ao FrontEnd
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'cargo': self.cargo,
            'foto': self.foto,
        }
        
#-------------------------------------------------------------------------------------------------
    # Pega um Objeto e transforma em um Dicionário
    def all_data(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'cargo': self.cargo,
            'salario': self.salario,
            'status': self.status,
            'foto': self.foto,
        }