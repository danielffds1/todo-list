# main.py
import os
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

# Instancia a classe FastAPI
app = FastAPI()

# Encriptando a senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Importa as rotas
from auth_routes import auth_router
from todo_routes import todo_router

# inclusão das rotas pelo FastAPI
app.include_router(auth_router)
app.include_router(todo_router)
