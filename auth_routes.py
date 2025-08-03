#auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from models import User
from dependencies import pegar_sessao, verificar_token, criar_token
from main import bcrypt_context
from schemas import UserSchema, LoginSchema, UsuarioResponseSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

# Tag para identificar as rotas de autenticação no Swagger
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def autenticar_usuario(email, senha, session):
    usuario = session.query(User).filter(User.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação dos pedidos
    """
    return {"message": "Voce esta na rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta", response_model=dict)
async def criar_conta(usuario_schema: UserSchema, session: Session = Depends(pegar_sessao)):
    """
    Cria uma nova conta de usuário
    """
    # Pegando o primeiro usuário caso existir
    usuario = session.query(User).filter(User.email == usuario_schema.email).first()
    if usuario:
        # já existe um usuário
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        # Criptografando a senha
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        
        # Criando novo usuário
        novo_usuario = User(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_criptografada,
            ativo=usuario_schema.ativo,
            admin=usuario_schema.admin
        )
        
        session.add(novo_usuario)
        session.commit()
        
        return {"mensagem": f"usuário cadastrado com sucesso: {usuario_schema.email}"}

@auth_router.post("/login-form")
async def login_form(data_formulario: OAuth2PasswordRequestForm = Depends(), session:Session = Depends(pegar_sessao)):
    """
    Faz login do usuário
    """
    usuario = autenticar_usuario(data_formulario.username, data_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "Bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(usuario: User = Depends(verificar_token)):
    access_token = criar_token(usuario.id)

    return {"access_token": access_token, "token_type": "Bearer"}