# 📝 TodoClima - API de Lista de Tarefas com Clima

Sistema de gerenciamento de tarefas com autenticação de usuário e integração com uma API de previsão do tempo. As tarefas podem ser classificadas como indoor ou outdoor, e a API pode sugerir ações com base nas condições climáticas.

---

## 🚀 Funcionalidades

- ✅ Criar, atualizar, listar e remover tarefas
- ✅ Marcar tarefa como concluída
- ✅ Filtrar tarefas por status
- ✅ Cadastro e login de usuários (com JWT)
- ✅ Integração com API de clima (OpenWeatherMap)
- ✅ Lógica de sugestão baseada no tipo de atividade e clima
- ✅ Documentação interativa via Swagger

---

## 🧱 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PostgreSQL](https://www.postgresql.org/) (ou SQLite para testes)
- JWT para autenticação
- OpenWeatherMap API

---

## 🛠️ Instalação e Execução

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/todoclima-api.git
cd todoclima-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente (crie .env)
cp .env.example .env

# 5. Rode o projeto
uvicorn app.main:app --reload
