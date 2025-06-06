from flask import Blueprint, request, jsonify
from flasgger import swag_from # Classe que faz a documentação em yml
from src.model import db # Retirado do __ini__ da pasta Model
from src.model.reembolso_model import Reembolso
from src.services.utils import padronizar

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

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
    def normalizar_numero(valor):
        return float(valor) if valor not in ["", None, "null"] else None
    
    try:
        lista_solicitacao = request.get_json() 
    

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
            
            nova_solicitacao = Reembolso(
                colaborador=dados_solicitacao['colaborador'],
                empresa=dados_solicitacao['empresa'],
                descricao=dados_solicitacao['descricao'],
                data=dados_solicitacao['data'],
                tipo_reembolso=dados_solicitacao['tipo_reembolso'],
                centro_custo=dados_solicitacao['centro_custo'],
                ordem_interna=ordem_interna,
                divisao=divisao,
                pep=pep,
                moeda=dados_solicitacao['moeda'],
                distancia_km=str(dados_solicitacao.get('distancia_km') or ""),
                valor_km=str(dados_solicitacao.get('valor_km') or ""),
                valor_faturado=normalizar_numero(dados_solicitacao.get('valor_faturado')),
                despesa=normalizar_numero(dados_solicitacao.get('despesa')),
                id_colaborador=int(dados_solicitacao['id_colaborador']),
                status='analisando',
            )
            objetos_solicitacao.append(nova_solicitacao)
            
        db.session.add_all(objetos_solicitacao)
        db.session.commit()
        return jsonify({'response': 'Solicitação feita com sucesso'}), 201
    
    except Exception as erro:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(erro)}), 500

@bp_reembolso.route('<int:num_prestacao>')
@swag_from('../docs/reembolso/buscar_solicitacao.yml')
def buscar__reembolso_por_num_prestacao(num_prestacao):
    
    try:
        reembolsos = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
        ).scalars().all()
        
        if not reembolsos:
            return jsonify({'error': 'Não solicitação de reembolso com este nº de prestação de contas.'}), 404
        
        reembolsos = [ reembolso.all_data() for reembolso in reembolsos ]
        
        return jsonify(reembolsos), 200
    except Exception as error:
        return jsonify({'error': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500

@bp_reembolso.route('deletar/<int:num_prestacao>', methods=['DELETE'])
@swag_from('../docs/reembolso/deletar_solicitacao.yml')
def deletar_por_num_prestacao(num_prestacao):
    try:
        reembolso = db.session.execute(
            db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
        ).scalar()
        if not reembolso:
            return jsonify({'erro': 'Solicitação de reembolso não encontrada.'}), 404

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso {num_prestacao} deletado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição.', 'detalhes': str(error)}), 500
    
@bp_reembolso.route('/atualizar/<int:num_prestacao>', methods=['PUT'])
@swag_from('../docs/reembolso/atualizar_solicitacao.yml')
def atualizar_reembolso(num_prestacao):
    def normalizar_numero(valor):
        return float(valor) if valor not in ["", None, "null"] else None

    try:
        dados_reembolso = request.get_json()
        dados_reembolso = padronizar(dados_reembolso)

        reembolso = db.session.get(Reembolso, num_prestacao)

        if not reembolso:
            return jsonify({'response': 'Nº de prestação de conta não identificado.'}), 404

        if 'colaborador' in dados_reembolso:
            reembolso.colaborador = dados_reembolso['colaborador']
        if 'empresa' in dados_reembolso:
            reembolso.empresa = dados_reembolso['empresa']
        if 'descricao' in dados_reembolso:
            reembolso.descricao = dados_reembolso['descricao']
        if 'data' in dados_reembolso:
            reembolso.data = dados_reembolso['data']
        if 'tipo_reembolso' in dados_reembolso:
            reembolso.tipo_reembolso = dados_reembolso['tipo_reembolso']
        if 'centro_custo' in dados_reembolso:
            reembolso.centro_custo = dados_reembolso['centro_custo']
        if 'ordem_interna' in dados_reembolso:
            reembolso.ordem_interna = dados_reembolso['ordem_interna']
        if 'divisao' in dados_reembolso:
            reembolso.divisao = dados_reembolso['divisao']
        if 'pep' in dados_reembolso:
            reembolso.pep = dados_reembolso['pep']
        if 'moeda' in dados_reembolso:
            reembolso.moeda = dados_reembolso['moeda']
        if 'distancia_km' in dados_reembolso:
            reembolso.distancia_km = str(dados_reembolso['distancia_km'] or "")
        if 'valor_km' in dados_reembolso:
            reembolso.valor_km = str(dados_reembolso['valor_km'] or "")
        if 'valor_faturado' in dados_reembolso:
            reembolso.valor_faturado = normalizar_numero(dados_reembolso['valor_faturado'])
        if 'despesa' in dados_reembolso:
            reembolso.despesa = normalizar_numero(dados_reembolso['despesa'])
        if 'status' in dados_reembolso:
            reembolso.status = dados_reembolso['status']
            
        db.session.commit()
        
        return jsonify({'response': 'Solicitação de reembolso atualizado com sucesso.'}), 200
        
    except Exception as error:
        return jsonify({'erro': 'Erro inesperado ao processar a requisição ', 'detalhes': str(error)}), 500