#models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from enum import Enum
from datetime import datetime
import uuid

#cria a conexão com o banco de dados
db = create_engine('sqlite:///database.db')

#cria a base do banco de dados
Base = declarative_base()

class User(Base):
    __tablename__ = 'usuarios'

    id = Column('id', String, primary_key=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String, nullable=False)
    admin = Column('admin', Boolean, default=False)
    ativo = Column('ativo', Boolean, default=True)
    created_at = Column('created_at', DateTime, default=datetime.now)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.created_at = datetime.now()
        self.admin = admin

class Todo(Base):
    __tablename__ = 'todos'

    id = Column('id', String, primary_key=True)
    user_id = Column('user_id', String, ForeignKey('usuarios.id'))
    title = Column('title', String, nullable=False)
    description = Column('description', String, nullable=False)
    status = Column('status', String, nullable=False)
    activity_type = Column('activity_type', String, nullable=False)
    city = Column('city', String, nullable=False)
    suggestion = Column('suggestion', String, nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.now)

    def __init__(self, user_id, title, description, status, activity_type, city, suggestion):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.activity_type = activity_type
        self.city = city
        self.suggestion = suggestion
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class TodoHistory(Base):
    __tablename__ = 'todo_history'

    id = Column('id', String, primary_key=True)
    todo_id = Column('todo_id', String, ForeignKey('todos.id'))
    user_id = Column('user_id', String, ForeignKey('usuarios.id'))
    action = Column('action', String, nullable=False)  # 'created', 'updated', 'deleted', 'status_changed'
    field_name = Column('field_name', String)  # 'title', 'description', 'status', etc.
    old_value = Column('old_value', Text)
    new_value = Column('new_value', Text)
    created_at = Column('created_at', DateTime, default=datetime.now)

    def __init__(self, todo_id, user_id, action, field_name=None, old_value=None, new_value=None):
        self.id = str(uuid.uuid4())
        self.todo_id = todo_id
        self.user_id = user_id
        self.action = action
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.created_at = datetime.now()
