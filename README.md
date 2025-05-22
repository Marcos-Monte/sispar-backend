
# 📌 sispar-backend

API desenvolvida com **Flask** e **MySQL**, responsável pelo gerenciamento de **colaboradores** e **reembolsos** no sistema SISPAR. Esta documentação orienta como clonar, instalar e executar o projeto, além de apresentar as principais rotas disponíveis.

## ✅ Tecnologias Utilizadas

- Flask
- Flask-SQLAlchemy
- MySQL + mysqlclient
- JWT (com Flask-Bcrypt)
- Flasgger (documentação Swagger)
- Flask-CORS
- Python-dotenv
- Gunicorn (para deploy)
- Pytest + pytest-flask (testes)

## 📦 Clonando e Instalando

```bash
# Clone o repositório
git clone https://github.com/Marcos-Monte/sispar-backend.git

# Acesse a pasta do projeto
cd sispar-backend

# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows

# Instale as dependências
pip install -r requirements.txt
```

## ▶️ Como Executar o Projeto

```bash
# Execute o projeto
python run.py
```

O servidor será iniciado em `http://localhost:5000/`.

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (exemplo):

```
FLASK_ENV=development
DATABASE_URL=mysql://usuario:senha@localhost/nome_do_banco
```

## 🔗 Rotas Principais

* Documentação (Flasgger) em: `http://localhost:5000/apidocs/`

### 📂 Colaborador

| Método | Rota                                  | Descrição                               |
|--------|---------------------------------------|-----------------------------------------|
| GET    | `/colaborador/todos-colaboradores`    | Lista todos os colaboradores            |
| GET    | `/colaborador/buscar/<email>`    | Lista o colaborador pelo email            |
| POST   | `/colaborador/cadastrar`              | Cadastra um novo colaborador            |
| POST   | `/colaborador/login`                     | Login de colaborador |
| PUT    | `/colaborador/atualizar/<email>`         | Atualiza os dados de um colaborador     |
| DELETE | `/colaborador/deletar/<id>`                     | Deleta um colaborador |

### 💰 Reembolso

| Método | Rota                                     | Descrição                                  |
|--------|------------------------------------------|--------------------------------------------|
| GET    | `/reembolso/reembolsos`                  | Lista todos os reembolsos                  |
| GET    | `/reembolso/<numero>`                    | Busca reembolso pelo número de prestação   |
| POST   | `/reembolso/solicitacao`                 | Solicita um novo reembolso                 |
| PUT    | `/reembolso/atualizar/<numero>`         | Atualiza os dados de um reembolso     |
| DELETE | `/reembolso/deletar/<numero>`            | Deleta reembolso pelo número de prestação  |


## 🧾 Estrutura de Pastas (resumo)

```
📦 sispar-backend/
 ┣ 📂src/
 ┃ ┣ 📂controllers/
 ┃ ┣ 📂models/
 ┃ ┣ 📂docs/
 ┃ ┣ 📂security/
 ┃ ┗ 📂services/
 ┃ ┗ 📂tests/
 ┣ 📂venv/
 ┣ .gitignore
 ┣ config.py
 ┣ run.py
 ┣ requirements.txt
 ┗ .env
```

## 🛠 Testes

Execute os testes automatizados com:

```bash
pytest src/tests/test_app.py
```

## 👨‍💻 Autor

Desenvolvido por [Marcos Monte](https://github.com/Marcos-Monte)
