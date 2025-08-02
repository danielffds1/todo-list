#schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para criação de usuário
class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

# Schema para login
class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class UsuarioResponseSchema(BaseModel):
    id: str
    nome: str
    email: str
    ativo: bool
    admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TodoSchema(BaseModel):
    title: str
    description: str
    status: str
    activity_type: str
    city: str
    suggestion: Optional[str] = None

    class Config:
        from_attributes = True

class TodoUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    activity_type: Optional[str] = None
    city: Optional[str] = None
    suggestion: Optional[str] = None

    class Config:
        from_attributes = True

class TodoResponseSchema(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    status: str
    activity_type: str
    city: str
    suggestion: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True