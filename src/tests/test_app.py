# # Para que a biblioteca encontre o arquivo de test ele tem que encontrar com 'test'

# ##### Para Rodar devemos usar no terminal --> pytest src/tests/test_app.py

# # pip install pytest-flask -> iNSTALANDO O PYTEST
# import pytest # Traz a biblioteca de testes
# import time # Manipular o tempo
# from src.model.colaborador_model import Colaborador
# from src.model.reembolso_model import Reembolso
# from src.app import create_app

# # ------------------------------------
# # Configurações para Testes


# # Yield será o primeiro a ser destruído para liberar espaço de memotira
# @pytest.fixture # Identifica funções de configurações para o teste
# def app():
#     app = create_app() # Instancia do Flask
#     yield app # YIELD vai guardar os valores em memoria (para usar em outros lugares)
    
    
# @pytest.fixture
# def client(app): # Simula o Usuário
#     return app.test_client()
    
# # --------------------------------------

# # Arquivos e Funções precisam começar com a palavra test
# def test_desempenho_requisicao_get(client):
    
#     comeco = time.time() # Pega a hora atual e transforma em segundos
    
#     for _ in range(1900): # fazer 100 requisições em 1 segundo (_ fala que a variavel auxiliar não serve para nada)
#         resposta = client.get('/reembolso/reembolsos') # Usuario vai fazer um get no servidor e armazenar em 'resposta'
        
#     fim = time.time() - comeco # A hora que acabar menos a hora que começou (dando o o tempo que levou para fazer a requisição)
#     assert  fim < 1.0 # Assert -> Palavra reservada Verifica condições (Verifica se elas são iguais)

import pytest
import time
from src.model.colaborador_model import Colaborador
from src.model.reembolso_model import Reembolso
from src.app import create_app
from src.model import db
from src.security.security import hash_senha

# -----------------------
# FIXTURES DE TESTE
# -----------------------

@pytest.fixture
def app():
    """Cria uma instância da aplicação Flask para testes."""
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """Simula um cliente HTTP que faz requisições à aplicação."""
    return app.test_client()

# -----------------------
# TESTES - COLABORADOR
# -----------------------

def test_login_colaborador(client):
    """Verifica se a rota de login responde corretamente com dados simulados."""
    response = client.post('/colaborador/login', json={
        'email': 'teste@email.com',
        'senha': '123456'
    })
    assert response.status_code in (200, 401, 404)

def test_cadastro_colaborador(client):
    """Testa o cadastro de um novo colaborador."""
    response = client.post('/colaborador/cadastrar', json={
        "nome": "Marcos Monte",
        "email": f"marcos{int(time.time())}@email.com",
        "senha": "senha123",
        "cargo": "Desenvolvedor",
        "foto": None,
        "salario": 5000,
        "status": "ativo"
    })
    assert response.status_code in (201, 400)

def test_listar_colaboradores(client):
    """Verifica se a listagem de colaboradores funciona corretamente."""
    response = client.get('/colaborador/todos-colaboradores')
    assert response.status_code in (200, 204)

# -----------------------
# TESTES - REEMBOLSO
# -----------------------

def test_cadastro_reembolso(client, app):
    """Testa o cadastro de reembolso vinculado a um colaborador."""
    with app.app_context():
        novo = Colaborador(
            nome="Marcos Monte",
            email=f"marcos{int(time.time())}@teste.com",
            senha=hash_senha("senha123").decode("utf-8"),
            cargo="Desenvolvedor",
            salario=5000.0,
            status="ativo",
            foto=None
        )
        db.session.add(novo)
        db.session.commit()
        id_colaborador = novo.id

    payload = [{
        "colaborador": "Marcos Monte",
        "empresa": "Empresa Teste",
        "descricao": "Viagem a serviço",
        "data": "2025-05-12",
        "tipo_reembolso": "Transporte",
        "centro_custo": "Financeiro",
        "ordem_interna": "1234",
        "divisao": "A",
        "pep": "1234-A",
        "moeda": "BRL",
        "distancia_km": 10,
        "valor_km": 2.5,
        "valor_faturado": 25.0,
        "despesa": 25.0,
        "id_colaborador": id_colaborador
    }]

    response = client.post('/reembolso/solicitacao', json=payload)
    assert response.status_code == 201

def test_listar_reembolsos(client):
    """Verifica se a listagem de reembolsos está acessível."""
    response = client.get('/reembolso/reembolsos')
    assert response.status_code in (200, 204)

def test_desempenho_lista_reembolsos(client):
    """
    Verifica se a rota de listagem de reembolsos aguenta 500 requisições em menos de 1 segundo.
    Esse é um indicativo de desempenho importante para apresentações.
    """
    inicio = time.time()
    for _ in range(500):
        client.get('/reembolso/reembolsos')
    tempo_total = time.time() - inicio
    print(f"\nTempo para 500 requisições: {tempo_total:.4f} segundos")
    assert tempo_total < 1.0  # Indicativo de desempenho robusto

    