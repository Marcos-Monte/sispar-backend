from src.model import db # Instancia do Banco de Dados
# Importações para criar as tabelas no Banco de Dados
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DECIMAL, DATE
from sqlalchemy import func # Função geradora (Usado para pegar a data atual do sistema)
from sqlalchemy  import ForeignKey # Para lidar com chaves estrangeiras

# Classe de Molde
class Reembolso(db.Model): 
    __tablename__ = 'tb_reembolso' # Cria a tabela com o nome tb_colaborador
#-------------------------- Atributos ------------------------------------
    # Tipo de dados + Constraints (Regras)
    
    id = Column(Integer, primary_key=True, autoincrement=True) # Coluna id, tipo inteiro, chave primaria com autoincremento
    colaborador = Column(String(150), nullable=False) # Coluna colaborador, tipo string, não pode ter valores nulos
    empresa = Column(String(50), nullable=False) # Coluna empresa, tipo string (trabalham com abreviações)
    num_prestacao = Column(Integer, nullable=False) # Coluna número de prestação, tipo inteiro
    # Ícone
    descricao = Column(String(255)) # Seria a imagem dos tickets de comprovação (poderiamos armazenar imagens e chamar URL ou usar alguma técnica)
    # No caso de tratar no front, pode gerar erro!
    data = Column(DATE, default=func.current_date(), nullable=False) # Coluna data, tipo data, (Se não tiver data, pegar a data do dia)
    # Enumarate (tecnica para lidar com outros Selects)
    tipo_reembolso = Column(String(35), nullable=False) # Coluna tipo, tipo string (virá de um select no front)
    centro_custo = Column(String(50), nullable=False) # Coluna centro de custo, tipo string (virá de um select no front)
    
    # pep = ordem + divisão -> Fazer regra de negocio para que isso fique disponível no Front
    ordem_interna = Column(String(50)) 
    divisao = Column(String(50)) 
    pep = Column(String(50)) 
    
    moeda = Column(String(20), nullable=False) # Coluna moeda, tipo string (virá de um select no front)
    
    # Função que recebe distancia e indica o valor por km percorrido no valor_faturado (10 x 1 = 10)
    distancia_km = Column(String((50)))
    valor_km = Column(String((50)))
    valor_faturado = Column(DECIMAL(10, 2), nullable=False) # Colocando 10 casas antes da virgula e 2 depois
    
    despesa = Column(DECIMAL(10, 2)) # Colocando 10 casas antes da virgula e 2 depois (Adiantamento pode existir ou não)
    
    # Chave estrangeira para fixar relacionamento entre essa tabela e a de colaboradores
    id_colaborador = Column(Integer, ForeignKey(column='tb_colaborador.id'))
    status = Column(String(25)) # Colocaremos os 3 status possíveis (todas começam: 'Em análise')
    
# ----------------------------------------------------------------------------
    # Método contrutor -> Necessário o atributo 'self'
    def __init__ (self, colaborador, empresa, num_prestacao, descricao, data, tipo_reembolso, centro_custo, ordem_interna, divisao, pep, moeda, distancia_km, valor_km, valor_faturado, despesa, id_colaborador, status='analisando'):
        # self.id = id # Quando o ID é autoincrementado, não precisa estar no Método Construtor
        self.colaborador = colaborador
        self.empresa = empresa
        self.num_prestacao = num_prestacao
        self.descricao = descricao
        self.data = data
        self.tipo_reembolso = tipo_reembolso
        self.centro_custo = centro_custo
        self.ordem_interna = ordem_interna
        self.divisao = divisao
        self.pep = pep
        self.moeda = moeda
        self.distancia_km = distancia_km
        self.valor_km = valor_km
        self.valor_faturado = valor_faturado
        self.despesa = despesa
        self.id_colaborador = id_colaborador
        self.status = status

# --------------------Métodos ---------------------------------------------------
    def all_data(self) -> dict:
        return {
            'id': self.id,
            'colaborador': self.colaborador,
            'empresa': self.empresa,
            'num_prestacao': self.num_prestacao,
            'descricao': self.descricao,
            'data': self.data,
            'tipo_reembolso': self.tipo_reembolso,
            'centro_custo': self.centro_custo,
            'ordem_interna': self.ordem_interna,
            'divisao': self.divisao,
            'pep': self.pep,
            'moeda': self.moeda,
            'distancia_km': self.distancia_km,
            'valor_km': self.valor_km,
            'valor_faturado': self.valor_faturado,
            'despesa': self.despesa,
            'id_colaborador': self.id_colaborador,
            'status': self.status,
        }