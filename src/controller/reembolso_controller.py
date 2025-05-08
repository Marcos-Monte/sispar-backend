#Tarefa -> Implementação

# 2 Rotas
## 1 - Visualização de TODOS OS REEMBOLSOS -> GET
### ID_COLABORADOR -> Associar todos os reembolsos a um único ID

## 2 - Solicitação de Reembolso -> POST



# -------------------------------------------------------------------------------
# # Tarefa -> Implementação

# Rota de visualização de todos os reembolsos -> GET
# Solicitação de reembolsos -> POST

# Para enviar multiplos dados para o BD, utilize: db.session.bulk_save_objects(lista[instancias])

from flask import Blueprint, request, jsonify

from src.model.reembolso_model import Reembolso
from src.model import db # Retirado do __ini__ da pasta Model

from flasgger import swag_from # Classe que faz a documentação em yml

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')# https://localhost:8000/reembolsos

@bp_reembolso.route('/reembolsos')
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def pegar_todos_reembolsos():
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso)
        ).scalars().all()
        
        if not reembolsos:
            return jsonify({'response': 'Não há reembolsos cadastrados'}), 200
        
        reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]
        
        return jsonify(reembolsos), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500

@bp_reembolso.route('/solicitacao', methods=['POST'])
@swag_from('../docs/reembolso/cadastrar_solicitacoes.yml')
def solicitar_novo_reembolso():
    
    try:
        lista_solicitacao = request.get_json() # Recebe os dados da requisição
    
        # Validações
        if not lista_solicitacao:
            return jsonify({'erro': 'A lista de solicitações está vazia. Envie pelo menos um reembolso.'}), 400
        objetos_solicitacao = []
        # Percorrer a lista recebida e criar um objeto para cada item da lista
        for i, dados_solicitacao in enumerate(lista_solicitacao):
            pep = dados_solicitacao.get('pep')
            divisao = dados_solicitacao.get('divisao')
            ordem_interna = dados_solicitacao.get('ordem_interna')
            
            if pep and not (ordem_interna and divisao):
                if '-' in pep:
                    ordem_interna, divisao = pep.split('-', 1)
                else:
                    return jsonify({'erro': f'{i+1}º Solicitação inválida: o campo pep deve conter "-" para separar ordem_interna e divisão.'}), 400
            elif (ordem_interna and divisao) and not pep:
                pep = f'{ordem_interna}-{divisao}'
            elif pep and (ordem_interna and divisao):
                if '-' in pep:
                    ordem_interna, divisao = pep.split('-', 1)
                else:
                    return jsonify({'erro': f'{i+1}º Solicitação inválida: o campo pep deve conter "-" para separar ordem_interna e divisão.'}), 400
            elif not pep and not (ordem_interna and divisao):
                return jsonify({'erro': f'{i+1}º Solicitação inválida: Informe "pep" ou "ordem_interna e divisao."'}), 400
            
            # Criando o objeto a ser inserido no bd
            nova_solicitacao = Reembolso(
                colaborador = dados_solicitacao['colaborador'],
                empresa = dados_solicitacao['empresa'],
                # num_prestacao = dados_solicitacao['num_prestacao'],
                descricao = dados_solicitacao['descricao'],
                data = dados_solicitacao['data'],
                tipo_reembolso = dados_solicitacao['tipo_reembolso'],
                centro_custo = dados_solicitacao['centro_custo'],
                ordem_interna = ordem_interna,
                divisao = divisao,
                pep = pep,
                moeda = dados_solicitacao['moeda'],
                distancia_km = dados_solicitacao['distancia_km'],
                valor_km = dados_solicitacao['valor_km'],
                valor_faturado = dados_solicitacao['valor_faturado'],
                despesa = dados_solicitacao['despesa'],
                id_colaborador = dados_solicitacao['id_colaborador'],
                status = 'analisando',
            )
            objetos_solicitacao.append(nova_solicitacao)
            
        db.session.add_all(objetos_solicitacao)
        db.session.commit()
        return jsonify({'response': 'Solicitação feita com sucesso'}), 201
    
    except Exception as erro:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(erro)}), 500

@bp_reembolso.route('<int:id>')
def buscar_por_id_colaborador(id):
    
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == id)
        ).scalars().all()
        
        if not reembolsos:
            return jsonify({'error': 'Não solicitação de reembolso com este nº de prestação de contas.'}), 404
        
        reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]
        
        return jsonify(reembolsos), 200
    except Exception as error:
        return jsonify({'error': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_reembolso.route('deletar/<int:id>', methods=['DELETE'])
def deletar_por_id(id):
    try:
        reembolso = db.session.execute(
            db.select(Reembolso).where(Reembolso.id == id)
        ).scalar()
        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso {id} deletado com sucesso'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição', 'detalhes': str(error)}), 500