import requests

from fastapi import APIRouter, HTTPException, Depends
from models import User
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from config import API_KEY

weather_router = APIRouter(prefix="/weather", tags=["weather"])

@weather_router.get("/{city}")
async def get_weather(city: str,
                      current_user: User = Depends(verificar_token),
                      session: Session = Depends(pegar_sessao)
                      ):
    # Verificar se a API_KEY está configurada
    if not API_KEY or API_KEY == "sua_chave_da_api_aqui_123456789":
        raise HTTPException(status_code=500, detail="API_KEY não configurada")
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={API_KEY}&units=metric&lang=pt_br"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="API_KEY inválida")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Cidade '{city}' não encontrada")
        else:
            # Retornar o erro da API para debug
            error_data = response.json() if response.content else {"message": "Erro desconhecido"}
            raise HTTPException(status_code=response.status_code, detail=error_data)
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")