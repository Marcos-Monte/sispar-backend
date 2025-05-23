from src.model import db 
from sqlalchemy.schema import Column 
from sqlalchemy.types import String, DECIMAL, Integer 

class Colaborador(db.Model):
    __tablename__ = 'tb_colaborador' # Cria a tabela com o nome tb_colaborador
    
    id = Column(Integer, primary_key= True, autoincrement=True) # Coluna id, tipo inteiro, chave primaria com autoincremento
    nome = Column(String(255))
    email = Column(String(155))
    senha = Column(String(150))
    cargo = Column(String(150))
    salario = Column(DECIMAL(10,2))
    status = Column(String(100))
    foto = db.Column(db.String(255), nullable=True)
    
    # Método construtor
    def __init__ (self, nome, email, senha, cargo, salario, status, foto):
        self.nome = nome 
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario
        self.status = status
        self.foto = foto
        
    # Retornos
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'cargo': self.cargo,
            'foto': self.foto,
        }
        
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