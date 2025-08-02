#auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from models import User
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UserSchema, LoginSchema, UsuarioResponseSchema
from sqlalchemy.orm import Session

# Tag para identificar as rotas de autenticação no Swagger
auth_router = APIRouter(prefix="/auth", tags=["auth"])

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

@auth_router.post("/login", response_model=dict)
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
    Faz login do usuário
    """
    # Buscando usuário pelo email
    usuario = session.query(User).filter(User.email == login_schema.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Verificando se a senha está correta
    if not bcrypt_context.verify(login_schema.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Verificando se o usuário está ativo
    if not usuario.ativo:
        raise HTTPException(status_code=401, detail="Usuário inativo")
    
    return {
        "mensagem": "Login realizado com sucesso",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "admin": usuario.admin
        }
    }