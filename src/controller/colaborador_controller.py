# Recebe as Requisições e Devolvemos as Respostas da Entidade 'Colaborador'
from flask import Blueprint, request, jsonify
# Request -> Recurso do flask que facilita a captura dos dados na requisição. Toda Req tem o JSON, através do 'request' pegamos e armazenamos em uma variavel
    # Trabalhar com as requisições
# Jsonify -> Recurso do flask que envia os dados no formato Json
    # Oposto do Request, trabalha com a Resposta -> Envio dos Dados no Formato JSON, Envio dos Status (200, 404, 500...)

from src.model.colaborador_model import Colaborador # Importa a classe molde de Colaborador
from src.model import db # Importa a instância do banco de dados

from src.security.security import checar_senha, hash_senha # Funções de segurança para cryptografar as senhas

from src.services.utils import padronizar, validacao_cadastro_completa, validacao_atualização_colaborador, autenticacao_colaborador

from flasgger import swag_from # Classe que faz a documentação em yml

from sqlalchemy.exc import IntegrityError

# Anteriormente usava se uma lista de dicionario com dados como banco de dados Mockado

# Blueprint -> Conceito de dividir as rotas 
# Usar o nome do arquivo, recebe a Classe 'Blueprint'
bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador') # https://localhost:8000/colaborador

@bp_colaborador.route('/todos-colaboradores')
@swag_from('../docs/colaborador/listar_colaboradores.yml') # Integra a função com a documentação desse 'caminho'
def pegar_dados_todos_colaboradores():
    try:
        # Criando uma lista de objetos de Colaboradores
        # return dados # Uma rota sempre retorna algo
        # Instancia do Banco de Dados = db
        colaboradores = db.session.execute(
            db.select(Colaborador) # Classe Colaborador é o molde para criar a tabela
        ).scalars().all() # AO inves de trazer 1 dado trás todos 
        
        if not colaboradores:
            return jsonify({'response': 'Não há dados para retornar'}), 204
        
        colaboradores = [ colaborador.all_data() for colaborador in colaboradores ]  # Está adicionando cada colaborador dentro do Dicionário Colaboradores
        # Execute essa expressão, para cada          item do         iteravel
        return jsonify(colaboradores), 200
    except Exception as error:
        # Aqui indica um erro na requisição
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhe': str(error)}), 500

# Rota cadastrar só vai receber requisições com o método POST
@bp_colaborador.route('/cadastrar', methods=['POST']) # Colchetes indica que o retorno pode ser uma lista
@swag_from('../docs/colaborador/cadastrar_colaborador.yml') # Integra a função com a documentação desse 'caminho'
def cadastrar_novo_coladorador():
    try:
        campos_obrigatorios = ['nome', 'email', 'senha', 'cargo', 'salario', 'status']
        dados_requisicao = request.get_json() # Pegando o corpo da requisição enviada pelo Front
        dados_requisicao = padronizar(dados_requisicao) # Padronizando chaves e valores do dicionario
        
        # Validações: função utilitária
        erro = validacao_cadastro_completa(campos_obrigatorios, dados_requisicao)
        if erro:
            return erro
        
        # Criando novo dicionário nos moldes da classe 'Colaborador'
        novo_colaborador = Colaborador(
            nome=dados_requisicao['nome'],
            email=dados_requisicao['email'],
            senha=hash_senha(dados_requisicao['senha']), # Criptografando a senha
            cargo=dados_requisicao['cargo'],
            salario=dados_requisicao['salario'],
            status=dados_requisicao['status']
        )
        
        # INSERT INTO tb_colaborador (nome, email, senha cargo, salario) 
        # VALUES (
            # dados_requisicao['nome'], dados_requisicao['email'], dados_requisicao['senha'], dados_requisicao['cargo'], dados_requisicao['salario']
        #)
        db.session.add(novo_colaborador)
        db.session.commit() # Faz o commit no banco de dados, persistindo os dados
        
        return jsonify({'response': 'Colaborador cadastrado com sucesso'}), 201 # Retorna mensagem de sucesso e o Status Code de 'created'
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhe': str(error)}), 500

# SInaliza que os dados enviados após o 'atualizar', serão dinamicos e enviados pela URL
# https://localhost:8000/colaborador/atualizar/500 --> O ID deve estar passando assim
@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
@swag_from('../docs/colaborador/atualizar_colaborador.yml') # Integra a função com a documentação desse 'caminho'
def atualizar_dados_colaborador(id_colaborador):

    try:
        dados_requisicao = request.get_json() # Pegando o corpo da requisição enviada pelo Front
        dados_requisicao = padronizar(dados_requisicao) # Padronizando chaves e valores do dicionario
        
        # Validações: função utilitária
        erro = validacao_atualização_colaborador(dados_requisicao)
        if erro:
            return erro
        
        colaborador = db.session.get(Colaborador, id_colaborador) # Buscando o colaborador pelo id 

        # Vaalidação se o ID existe na aplicação
        if not colaborador:
            return jsonify({'response': 'Id de usuário não identificado'}), 404

        if 'nome' in dados_requisicao:
            colaborador.nome = dados_requisicao['nome']
        if 'cargo' in dados_requisicao:
            colaborador.cargo = dados_requisicao['cargo']
        if 'salario' in dados_requisicao:
            colaborador.salario = dados_requisicao['salario']
        if 'status' in dados_requisicao:
            colaborador.status = dados_requisicao['status']
        if 'email' in dados_requisicao:
            colaborador.email = dados_requisicao['email']
        if 'senha' in dados_requisicao:
            colaborador.senha = hash_senha(dados_requisicao['senha']).decode('utf-8')

        db.session.commit()

        return jsonify({'response': 'Dados do colaborador atualizados com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_colaborador.route('login', methods=['POST'])
@swag_from('../docs/colaborador/fazer_login_colaborador.yml') # Integra a função com a documentação desse 'caminho'
def login():
    try:
        campos_obrigatorios = ['email', 'senha']
        dados_requisicao = request.get_json() # Pegando o corpo da requisição enviada pelo Front
        dados_requisicao = padronizar(dados_requisicao) # Padronizando chaves e valores do dicionario

        erro = autenticacao_colaborador(campos_obrigatorios, dados_requisicao)
        if erro:
            return erro
        
        email = dados_requisicao['email']
        senha = dados_requisicao['senha']
        
        colaborador = db.session.execute(
            # Query fica dentro dos parametros do 'execute'
                # (Classe Colaborador está dentro de 'model')
            db.select(Colaborador).where(Colaborador.email == email) # Select * from colaborador Where email == 'algum_email
            
        ).scalar() # Traz um registro ou Atribui 'none' na variável
        
        # Usuário não encontrado (busca feito pelo email)
        if not colaborador:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
        
        # Se o usuário existir -> transforme ele em um dicionario
        colaborador = colaborador.to_dict()
        
        # Verificar se a senha é a mesma indicada na requisição e BD
        if checar_senha(senha, colaborador.get('senha')):
            return jsonify({'mensagem': f"Login de ({colaborador['email']}) realizado com sucesso", "items": colaborador}), 200 # Resposta de sucesso
        else:
            return jsonify({'mensagem': 'Senha incorreta'}), 401 # Resposta da senha incorreta
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500
    
@bp_colaborador.route('deletar/<int:id_colaborador>', methods=['DELETE'])
@swag_from('../docs/colaborador/deletar_colaborador.yml') # Integra a função com a documentação desse 'caminho'
def deletar_por_id(id_colaborador):
    colaborador = db.session.get(Colaborador, id_colaborador) # Buscando o colaborador pelo id 
    
    # Erro para caso o id_colaborador não exista no banco de dados
    if not colaborador:
        return jsonify({'erro': 'Colaborador não encontrado'}), 404

    try:
        db.session.delete(colaborador) # Deletando o colaborador encontrado
        db.session.commit() # executando a ação
        return jsonify({'mensagem': f'Colaborador {colaborador.email} deletado com sucesso'}), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': f'Não é possível excluir o colaborador ({colaborador.email}), pois há registros relacionados'}), 400