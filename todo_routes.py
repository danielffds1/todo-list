# todo_routes.py
from fastapi import APIRouter, HTTPException, Depends
#Instancia a classe APIRouter para criar as rotas do todo
todo_router = APIRouter(prefix="/todo", tags=["todo"])

#Rota para criar um novo todo
@todo_router.get("/")
async def get_todos():
    """
    Rota para obter as listas de tarefas
    """
    return {"message": "Hello World"}