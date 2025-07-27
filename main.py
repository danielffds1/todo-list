# main.py
from fastapi import FastAPI

#Instancia a classe FastAPI
app = FastAPI()

# Importa as rotas
from auth_routes import auth_router
from todo_routes import todo_router

#inclusão das rotas pelo FastAPI
app.include_router(auth_router)
app.include_router(todo_router)
