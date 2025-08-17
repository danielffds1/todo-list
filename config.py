# config.py
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_muito_segura_aqui_123456789")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) 
API_KEY = os.getenv("API_KEY", "b719f873d4492df30fd3463ddc13710e")  # Sua API key aqui