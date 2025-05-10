# Biliotecas
import re 
from flask import jsonify # Retorno das requisições em formado json

# Componentes, Classes e Instâncias
from src.model import db # Instancia do Banco de Dados
from src.model.colaborador_model import Colaborador

# --------------- Funções Simples------------------------------

def verificar_corpo(dados):
    if not dados:
        return jsonify({'erro': 'Nenhum dado foi enviado.'}), 400
    return None # Se existir dados, retorna vazio

# Padronizar como 'minusculas' todas as chaves e valores strings de uma requisição
def padronizar(dados):
    novos_dados = {} 
    # Percorrendo os items do Objeto
    for chave, valor in dados.items():
        # Transformando a 'chave' em minúscula
        chave_minuscula = chave.lower()
        
        if isinstance(valor, str): # Só converte strings
            # Transformando o 'valor / string' em minusculo
            valor_minusculo = valor.lower()
        else: 
            # Se não for string, apenas atribuir
            valor_minusculo = valor
        # Atribuindo chave e valor ao objeto
        novos_dados[chave_minuscula] = valor_minusculo
    # Retorna o novo objeto padronizado
    return novos_dados

# Verificação dos campos obrigatórios para uma equisição
def verificar_campos_obrigatorios(campos_obrigatorios, requisicao):
    for campo in campos_obrigatorios:
        if campo not in requisicao or not requisicao[campo]:
            return jsonify({'erro': f'Campo obrigatório ({campo}) não foi preenchido'}), 400
    return None # Continuar se todos os campos estiverem inseridos

# Verificar se o EMAIL já está cadastrado no banco de dados (valor único)
def verificar_email_cadastrado(email_requisicao):
    colaborador = db.session.query(Colaborador).filter_by(email=email_requisicao).first() # Consulta no 'bd' filtrando onde a chave email for igual ao valor passado, retorna o primeiro valor encontrado ou vazio
    if colaborador: # Se retornar algum valor
        return jsonify({'erro': f'E-mail ({colaborador.email}) já cadastrado.'}), 409 # Responder com jsonify que já existe
    return None # Continuar se o email ainda não tiver sido usado

# Verificar se o formato do email indicado é válido
def formato_email_valido(email):
    resultado = re.match(r"[^@]+@[^@]+\.[^@]+", email)
    if not resultado:
        return jsonify({'erro': f'Formato do e-mail ({email}) é inválido.'}), 400
    return None


# ---------------------Funções Completas -------------------------------

# Verificação completa para caso de cadastro para novo colaborador
def validacao_cadastro_completa(campos_obrigatorios, dados):

    # Validação de envio de dados
    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    # Validação referente aos campos obrigatórios para criação de novo colaborador
    faltando_campo_obrigatorio = verificar_campos_obrigatorios(campos_obrigatorios, dados)
    if faltando_campo_obrigatorio:
        return faltando_campo_obrigatorio
    
    # Verificação se o email está em formato válido
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
    
    # Verificação se o email passado já existe no cadastro
    email_ja_existente = verificar_email_cadastrado(dados['email'])
    if email_ja_existente:
        return email_ja_existente
    
    return None # Tudo válido

# Verificação completa para caso de atualização
def validacao_atualização_colaborador(dados):
    
    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
        
    return None # Tudo Valido

# Verificação para fazer o login de colaborador
def autenticacao_colaborador(campos_obrigatorios,dados):
    # Validação de envio de dados
    se_dados = verificar_corpo(dados)
    if se_dados:
        return se_dados
    
    # Validação referente aos campos obrigatórios para criação de novo colaborador
    faltando_campo_obrigatorio = verificar_campos_obrigatorios(campos_obrigatorios, dados)
    if faltando_campo_obrigatorio:
        return faltando_campo_obrigatorio
    
    # Verificação se o email está em formato válido
    email_invalido = formato_email_valido(dados['email'])
    if email_invalido:
        return email_invalido
    
    return None # Tudo Válido
