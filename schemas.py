#schemas.py
from pydantic import BaseModel
from typing import Optional

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
    created_at: str

    class Config:
        from_attributes = True