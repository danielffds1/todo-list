# todo_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import TodoSchema, TodoUpdateSchema, TodoResponseSchema
from models import Todo, User
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

#Instancia a classe APIRouter para criar as rotas do todo
todo_router = APIRouter(prefix="/todo", tags=["todo"])

# Função temporária para obter usuário atual (depois será substituída por JWT)
def get_current_user(session: Session, user_id: str = "temp_user_id"):
    return session.query(User).filter(User.id == user_id).first() #retorna o usuário atual

# CRIAR TODO
@todo_router.post("/", response_model=TodoResponseSchema)
async def criar_todo(
    todo_schema: TodoSchema,
    session: Session = Depends(pegar_sessao)
):
    user_id = "temp_user_id"

    novo_todo = Todo(
        user_id=user_id,
        title=todo_schema.title,
        description=todo_schema.description,
        status=todo_schema.status,
        activity_type=todo_schema.activity_type,
        city=todo_schema.city,
        suggestion=todo_schema.suggestion
    )

    session.add(novo_todo)
    session.commit()
    session.refresh(novo_todo)

    return novo_todo

# LISTAR TODOS
@todo_router.get("/", response_model=List[TodoResponseSchema])
async def listar_todos(session: Session = Depends(pegar_sessao)):
    user_id = "temp_user_id"
    todos = session.query(Todo).filter(Todo.user_id == user_id).all()
    return todos

# OBTER TODO ESPECÍFICO
@todo_router.get("/{todo_id}", response_model=TodoResponseSchema)
async def obter_todo(todo_id: str, session: Session = Depends(pegar_sessao)):
    user_id = "temp_user_id"
    
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == user_id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return todo

# ATUALIZAR TODO
@todo_router.put("/{todo_id}", response_model=TodoResponseSchema)
async def atualizar_todo(
    todo_id: str,
    todo_data: TodoUpdateSchema,  # Esta é a variável correta
    session: Session = Depends(pegar_sessao)
):
    user_id = "temp_user_id"
    
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == user_id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # CORREÇÃO: usar todo_data em vez de todo_update
    for field, value in todo_data.model_dump().items():
        if value is not None:
            setattr(todo, field, value)

    todo.updated_at = datetime.now()
    session.commit()
    session.refresh(todo)
    
    return todo

# DELETAR TODO
@todo_router.delete("/{todo_id}", response_model=dict)
async def deletar_todo(todo_id: str, session: Session = Depends(pegar_sessao)):
    user_id = "temp_user_id"
    
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == user_id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    session.delete(todo)
    session.commit()
    
    return {"message": "Tarefa deletada com sucesso"}
