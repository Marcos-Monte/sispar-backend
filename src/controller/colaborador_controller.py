from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy.exc import IntegrityError
from src.model import db
from src.model.colaborador_model import Colaborador 
from src.security.security import checar_senha, hash_senha
from src.services.utils import padronizar, validacao_cadastro_completa, validacao_atualização_colaborador, autenticacao_colaborador

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')


@bp_colaborador.route('/todos-colaboradores')
@swag_from('../docs/colaborador/listar_colaboradores.yml') 
def pegar_dados_todos_colaboradores():
    try:
        colaboradores = db.session.execute(
            db.select(Colaborador) 
        ).scalars().all() # AO inves de trazer 1 dado trás todos 
        
        if not colaboradores:
            return jsonify({'response': 'Não há dados para retornar'}), 204
        
        colaboradores = [ colaborador.all_data() for colaborador in colaboradores ]  # Está adicionando cada colaborador dentro do Dicionário Colaboradores

        return jsonify(colaboradores), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhe': str(error)}), 500


@bp_colaborador.route('/cadastrar', methods=['POST']) # Colchetes indica que o retorno pode ser uma lista
@swag_from('../docs/colaborador/cadastrar_colaborador.yml') 
def cadastrar_novo_coladorador():
    try:
        campos_obrigatorios = ['nome', 'email', 'senha', 'cargo', 'salario', 'status']
        dados_requisicao = request.get_json()
        dados_requisicao = padronizar(dados_requisicao) 
        
        erro = validacao_cadastro_completa(campos_obrigatorios, dados_requisicao)
        if erro:
            return erro
        
        senha_pura = dados_requisicao['senha']
        if isinstance(senha_pura, bytes):
            senha_pura = senha_pura.decode('utf-8')
        senha_hash = hash_senha(senha_pura).decode('utf-8')
        
        novo_colaborador = Colaborador(
            nome=dados_requisicao['nome'],
            email=dados_requisicao['email'],
            senha=senha_hash, # Criptografando a senha
            cargo=dados_requisicao['cargo'],
            salario=dados_requisicao['salario'],
            status=dados_requisicao['status'],
            foto=dados_requisicao.get('foto')  # opcional 
        )
        
        db.session.add(novo_colaborador)
        db.session.commit() # Faz o commit no banco de dados, persistindo os dados
        
        return jsonify({'response': 'Colaborador cadastrado com sucesso'}), 201
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhe': str(error)}), 500

@bp_colaborador.route('/atualizar/<string:email>', methods=['PUT'])
@swag_from('../docs/colaborador/atualizar_colaborador.yml') 
def atualizar_dados_colaborador(email):

    try:
        dados_requisicao = request.get_json() 
        dados_requisicao = padronizar(dados_requisicao) 
        
        erro = validacao_atualização_colaborador(dados_requisicao)
        if erro:
            return erro
        
        colaborador = db.session.execute(
            db.select(Colaborador).where(Colaborador.email == email)
        ).scalar_one_or_none()

        if not colaborador:
            return jsonify({'response': 'E-mail de usuário não identificado'}), 404

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
            senha = dados_requisicao['senha']
            if isinstance(senha, bytes):
                senha = senha.decode('utf-8')
            colaborador.senha = hash_senha(senha).decode('utf-8')
        if 'foto' in dados_requisicao:
            colaborador.foto = dados_requisicao['foto']

        db.session.commit()

        return jsonify({'response': 'Dados do colaborador atualizados com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_colaborador.route('login', methods=['POST'])
@swag_from('../docs/colaborador/fazer_login_colaborador.yml') 
def login():
    try:
        campos_obrigatorios = ['email', 'senha']
        dados_requisicao = request.get_json() 
        dados_requisicao = padronizar(dados_requisicao) 

        erro = autenticacao_colaborador(campos_obrigatorios, dados_requisicao)
        if erro:
            return erro
        
        email = dados_requisicao['email']
        senha = dados_requisicao['senha']
        
        colaborador = db.session.execute(
            # Query fica dentro dos parametros do 'execute'
            db.select(Colaborador).where(Colaborador.email == email) # Select * from colaborador Where email == 'algum_email'
            
        ).scalar() # Traz um registro ou Atribui 'none' na variável
        
        if not colaborador:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
        
        colaborador = colaborador.to_dict()
        
        if checar_senha(senha, colaborador.get('senha')):
            return jsonify({'mensagem': f"Login de ({colaborador['email']}) realizado com sucesso", "items": colaborador}), 200 
        else:
            return jsonify({'mensagem': 'Senha incorreta'}), 401 
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500
    
@bp_colaborador.route('deletar/<int:id_colaborador>', methods=['DELETE'])
@swag_from('../docs/colaborador/deletar_colaborador.yml') 
def deletar_por_id(id_colaborador):
    colaborador = db.session.get(Colaborador, id_colaborador) 
    
    if not colaborador:
        return jsonify({'erro': 'Colaborador não encontrado'}), 404

    try:
        db.session.delete(colaborador)
        db.session.commit() 
        return jsonify({'mensagem': f'Colaborador {colaborador.email} deletado com sucesso'}), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': f'Não é possível excluir o colaborador ({colaborador.email}), pois há registros relacionados'}), 400
    
@bp_colaborador.route('/buscar/<string:email>', methods=['GET'])
@swag_from('../docs/colaborador/buscar_por_email.yml') 
def buscar_colaborador_por_email(email):
    try:
        colaborador = db.session.execute(
            db.select(Colaborador).where(Colaborador.email == email)
        ).scalar_one_or_none()

        if not colaborador:
            return jsonify({'mensagem': 'Colaborador não encontrado'}), 404
        
        # Não enviamos a senha nesse retorno!
        dados_colaborador = colaborador.to_dict()
        dados_colaborador.pop('senha', None)

        return jsonify({'mensagem': 'Colaborador encontrado', 'colaborador': dados_colaborador}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro ao buscar colaborador', 'detalhes': str(error)}), 500
