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
    except Exception as e:
        return jsonify({'erro': 'Erro interno no servidor', 'detalhes': str(e)}), 500

@bp_reembolso.route('/solicitacao', methods=['POST'])
def solicitar_novo_reembolso():
    dados_solicitacao = request.get_json() # Recebe os dados da requisição
    
    # Validações
    if not dados_solicitacao:
        return jsonify({'error': 'Necessário enviar dados na solicitação!'}), 400
    
    # Criando o objeto a ser inserido no bd
    nova_solicitacao = Reembolso(
        colaborador = dados_solicitacao['colaborador'],
        empresa = dados_solicitacao['empresa'],
        num_prestacao = dados_solicitacao['num_prestacao'],
        descricao = dados_solicitacao['descricao'],
        data = dados_solicitacao['data'],
        tipo_reembolso = dados_solicitacao['tipo_reembolso'],
        centro_custo = dados_solicitacao['centro_custo'],
        ordem_interna = dados_solicitacao['ordem_interna'],
        divisao = dados_solicitacao['divisao'],
        pep = dados_solicitacao['pep'],
        moeda = dados_solicitacao['moeda'],
        distancia_km = dados_solicitacao['distancia_km'],
        valor_km = dados_solicitacao['valor_km'],
        valor_faturado = dados_solicitacao['valor_faturado'],
        despesa = dados_solicitacao['despesa'],
        id_colaborador = dados_solicitacao['id_colaborador'],
        status = dados_solicitacao['status'],
    )
    
    db.session.add(nova_solicitacao)
    db.session.commit()
    
    return jsonify({'response': 'Solicitação feita com sucesso'}), 201

@bp_reembolso.route('<int:id>')
def buscar_por_id(id):
    # reembolsos = Reembolso.query.get(id)
    reembolsos = db.session.execute(
        db.select(Reembolso).where(Reembolso.id_colaborador == id)
    ).scalars().all()
    
    if not reembolsos:
        return jsonify({'error': 'Não há reembolsos desse ID de Colaborador'}), 404
    
    reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]
    
    return jsonify(reembolsos), 200

@bp_reembolso.route('deletar/<int:id>', methods=['DELETE'])
def deletar_por_id(id):
    reembolso = Reembolso.query.get(id)
    if not reembolso:
        return jsonify({'erro': 'reembolso não encontrado'}), 404

    db.session.delete(reembolso)
    db.session.commit()

    return jsonify({'mensagem': f'Reembolso {id} deletado com sucesso'})