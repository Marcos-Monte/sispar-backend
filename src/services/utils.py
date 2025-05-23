import re 
from flask import jsonify
from src.model import db
from src.model.colaborador_model import Colaborador

# --------------- Funções Complementares ------------------------------

def verificar_corpo(dados):
    if not dados:
        return jsonify({'erro': 'Nenhum dado foi enviado.'}), 400
    return None 


def padronizar(dados):
    novos_dados = {} 

    for chave, valor in dados.items():
        chave_minuscula = chave.lower()
        
        if chave == 'foto':
            novos_dados[chave] = valor  # mantém a URL original
            continue
        
        if isinstance(valor, str): # Só converte strings
            valor_minusculo = valor.lower()
        else: 
            valor_minusculo = valor
        novos_dados[chave_minuscula] = valor_minusculo
    return novos_dados


def verificar_campos_obrigatorios(campos_obrigatorios, requisicao):
    for campo in campos_obrigatorios:
        if campo not in requisicao or not requisicao[campo]:
            return jsonify({'erro': f'Campo obrigatório ({campo}) não foi preenchido'}), 400
    return None # Continuar se todos os campos estiverem inseridos


def verificar_email_cadastrado(email_requisicao):
    colaborador = db.session.query(Colaborador).filter_by(email=email_requisicao).first() # Consulta no 'bd' filtrando onde a chave email for igual ao valor passado, retorna o primeiro valor encontrado ou vazio
    if colaborador:
        return jsonify({'erro': f'E-mail ({colaborador.email}) já cadastrado.'}), 409 
    return None # Continuar se o email ainda não tiver sido usado


def formato_email_valido(email):
    resultado = re.match(r"[^@]+@[^@]+\.[^@]+", email)
    if not resultado:
        return jsonify({'erro': f'Formato do e-mail ({email}) é inválido.'}), 400
    return None


# ---------------------Funções Completas -------------------------------

def validacao_cadastro_completa(campos_obrigatorios, dados):

    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    faltando_campo_obrigatorio = verificar_campos_obrigatorios(campos_obrigatorios, dados)
    if faltando_campo_obrigatorio:
        return faltando_campo_obrigatorio
    
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
    
    email_ja_existente = verificar_email_cadastrado(dados['email'])
    if email_ja_existente:
        return email_ja_existente
    
    return None # Tudo válido


def validacao_atualização_colaborador(dados):
    
    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
        
    return None # Tudo Valido


def autenticacao_colaborador(campos_obrigatorios,dados):

    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    faltando_campo_obrigatorio = verificar_campos_obrigatorios(campos_obrigatorios, dados)
    if faltando_campo_obrigatorio:
        return faltando_campo_obrigatorio
    
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
    
    return None # Tudo Válido
