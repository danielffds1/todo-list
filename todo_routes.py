# todo_routes.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import TodoSchema, TodoUpdateSchema, TodoResponseSchema
from models import Todo, User
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel

#Instancia a classe APIRouter para criar as rotas do todo
todo_router = APIRouter(prefix="/todo", tags=["todo"])

# CRIAR TODO
@todo_router.post("/", response_model=TodoResponseSchema)
async def criar_todo(
    todo_schema: TodoSchema,
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    novo_todo = Todo(
        user_id=current_user.id,
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
async def listar_todos(
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token),
    status: Optional[str] = Query(None, description="Filtro por status"),
    activity_type: Optional[str] = Query(None, description="Filtro por tipo de atividade"),
    limit: int = Query(10, description="Limite de resultados")
):
    query = session.query(Todo).filter(Todo.user_id == current_user.id)
    
    # Aplicar filtros se fornecidos
    if status:
        query = query.filter(Todo.status == status)
    
    if activity_type:
        query = query.filter(Todo.activity_type == activity_type)
    
    # Ordenar por data de criação (mais recentes primeiro)
    query = query.order_by(Todo.created_at.desc())
    
    # Aplicar limite se fornecido
    if limit:
        query = query.limit(limit)
    
    todos = query.all()
    
    return todos

# LISTAR TODOS DO DIA
@todo_router.get("/hoje", response_model=List[TodoResponseSchema])
async def listar_todos_hoje(
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    """
    Lista apenas as tarefas criadas hoje
    """
    hoje = date.today()
    todos = session.query(Todo).filter(
        Todo.user_id == current_user.id,
        Todo.created_at >= hoje
    ).order_by(Todo.created_at.desc()).all()
    
    return todos

# OBTER TODO ESPECÍFICO
@todo_router.get("/{todo_id}", response_model=TodoResponseSchema)
async def obter_todo(
    todo_id: str, 
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return todo

# ATUALIZAR TODO
@todo_router.put("/{todo_id}", response_model=TodoResponseSchema)
async def atualizar_todo(
    todo_id: str,
    todo_data: TodoUpdateSchema,
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    for field, value in todo_data.model_dump().items():
        if value is not None:
            setattr(todo, field, value)

    todo.updated_at = datetime.now()
    session.commit()
    session.refresh(todo)
    
    return todo

# DELETAR TODO
@todo_router.delete("/{todo_id}", response_model=dict)
async def deletar_todo(
    todo_id: str, 
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    session.delete(todo)
    session.commit()
    
    return {"message": "Tarefa deletada com sucesso"}

# ROTA ADMIN - LISTAR TODOS OS TODOS (apenas para admins)
@todo_router.get("/admin/todos", response_model=List[TodoResponseSchema])
async def listar_todos_admin(
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    """
    Lista todos os todos de todos os usuários (apenas para administradores)
    """
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores.")
    
    todos = session.query(Todo).order_by(Todo.created_at.desc()).all()
    return todos
