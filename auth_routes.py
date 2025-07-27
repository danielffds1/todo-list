#auth_routes.py
from fastapi import APIRouter, HTTPException, Depends

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Rota para autenticação
    """
    return {"message":"Hello World"}