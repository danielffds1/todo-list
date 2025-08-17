# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

# Carrega as variáveis de ambiente
load_dotenv()

# Instancia a classe FastAPI
app = FastAPI()

# Adicionar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Encriptando a senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Criando esquema de autenticação para o Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Importa as rotas
from auth_routes import auth_router
from todo_routes import todo_router
from weather_routes import weather_router

# inclusão das rotas pelo FastAPI
app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(weather_router)
