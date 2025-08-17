# todo_routes.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import TodoSchema, TodoUpdateSchema, TodoResponseSchema, TodoHistorySchema
from models import Todo, User, TodoHistory
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
import requests
from config import API_KEY

#Instancia a classe APIRouter para criar as rotas do todo
todo_router = APIRouter(prefix="/todo", tags=["todo"])

def gerar_sugestao_clima(activity_type: str, city: str) -> str:
    """
    Gera sugestões inteligentes baseadas no tipo de atividade e clima da cidade
    """
    try:
        # Verificar se a API_KEY está configurada
        if not API_KEY or API_KEY == "sua_chave_da_api_aqui_123456789":
            return "Não foi possível verificar o clima. Configure a API_KEY."
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={API_KEY}&units=metric&lang=pt_br"
        response = requests.get(url)
        
        if response.status_code != 200:
            return "Não foi possível obter informações do clima."
        
        weather_data = response.json()
        weather_description = weather_data.get('weather', [{}])[0].get('description', '').lower()
        temp = weather_data.get('main', {}).get('temp', 0)
        humidity = weather_data.get('main', {}).get('humidity', 0)
        wind_speed = weather_data.get('wind', {}).get('speed', 0)
        
        # Lógica de sugestões baseada no tipo de atividade e clima
        if activity_type.lower() in ['externo', 'outdoor', 'ar livre', 'rua', 'exercício', 'esporte']:
            if any(word in weather_description for word in ['chuva', 'rain', 'storm', 'tempestade', 'thunderstorm']):
                return f"🌧️ Está chovendo em {city} ({temp}°C)! ⚠️ Considere uma atividade interna: organização, leitura, exercícios em casa, projetos caseiros ou estudo."
            elif any(word in weather_description for word in ['céu limpo', 'clear sky', 'ensolarado']):
                return f"☀️ Tempo limpo e ensolarado em {city} ({temp}°C)! ✅ Perfeito para atividades externas. Aproveite o bom tempo e não esqueça do protetor solar!"
            elif temp < 10:
                return f"❄️ Temperatura muito baixa em {city} ({temp}°C). Vista-se adequadamente com roupas quentes para atividades externas!"
            elif temp < 15:
                return f"🥶 Temperatura baixa em {city} ({temp}°C). Use um casaco leve para atividades externas!"
            elif temp > 35:
                return f"🔥 Temperatura muito alta em {city} ({temp}°C). ⚠️ Evite atividades externas nos horários mais quentes (10h-16h). Considere atividades internas ou exercícios em casa."
            elif temp > 30:
                return f"🌡️ Temperatura alta em {city} ({temp}°C). Mantenha-se hidratado e evite atividades externas nos horários mais quentes!"
            elif wind_speed > 20:
                return f"💨 Vento forte em {city} ({wind_speed} km/h). ⚠️ Considere o impacto do vento em sua atividade externa ou opte por atividades internas."
            else:
                return f"🌤️ Clima agradável em {city} ({temp}°C)! ✅ Bom momento para atividades externas. Umidade: {humidity}%"
        
        elif activity_type.lower() in ['interno', 'casa', 'home', 'indoor', 'escritório', 'trabalho']:
            if any(word in weather_description for word in ['chuva', 'rain', 'storm', 'tempestade']):
                return f"🌧️ Perfeito! Está chovendo em {city} ({temp}°C), então sua tarefa interna é uma excelente escolha. ✅ Aproveite para ficar confortável em casa e ouvir o som da chuva!"
            elif any(word in weather_description for word in ['céu limpo', 'clear sky', 'ensolarado']):
                return f"☀️ Tempo limpo e ensolarado em {city} ({temp}°C)!  Que tal aproveitar o bom tempo? Considere: caminhada, exercícios ao ar livre, passeio no parque ou atividades externas."
            elif any(word in weather_description for word in ['nublado', 'clouds', 'overcast']):
                return f"☁️ Tempo nublado em {city} ({temp}°C). ✅ Bom momento para tarefas internas que precisam de concentração. A luz suave é ideal para trabalhar!"
            elif temp > 30:
                return f"🌡️ Temperatura alta em {city} ({temp}°C). Mantenha-se hidratado e use ventilador/ar condicionado para sua tarefa interna!"
            elif temp < 15:
                return f"🥶 Temperatura baixa em {city} ({temp}°C). ✅ Aproveite para ficar aconchegante em casa com sua tarefa interna!"
            else:
                return f"🏠 Clima agradável em {city} ({temp}°C). ✅ Sua tarefa interna será confortável! Umidade: {humidity}%"
        
        elif activity_type.lower() in ['estudo', 'leitura', 'concentração']:
            if any(word in weather_description for word in ['chuva', 'rain', 'storm', 'tempestade']):
                return f"🌧️ Clima perfeito para estudo em {city} ({temp}°C)! ✅ O som da chuva pode ajudar na concentração. Aproveite para ler ou estudar!"
            elif any(word in weather_description for word in ['nublado', 'clouds', 'overcast']):
                return f"☁️ Tempo nublado em {city} ({temp}°C). ✅ Luz suave ideal para leitura e estudo. Aproveite a tranquilidade!"
            elif any(word in weather_description for word in ['céu limpo', 'clear sky', 'ensolarado']):
                return f"☀️ Tempo limpo em {city} ({temp}°C). Boa luz natural para estudo, mas evite o sol direto nos olhos!"
            else:
                return f"📚 Clima em {city}: {weather_description.capitalize()} ({temp}°C). ✅ Bom para atividades que precisam de concentração!"
        
        else:
            # Para outros tipos de atividade
            if any(word in weather_description for word in ['chuva', 'rain', 'storm', 'tempestade']):
                return f"🌧️ Clima em {city}: {weather_description.capitalize()} ({temp}°C). Considere o impacto do clima em sua atividade!"
            elif any(word in weather_description for word in ['céu limpo', 'clear sky', 'ensolarado']):
                return f"☀️ Clima em {city}: {weather_description.capitalize()} ({temp}°C). Tempo agradável para suas atividades!"
            else:
                return f"🌤️ Clima em {city}: {weather_description.capitalize()} ({temp}°C). Umidade: {humidity}%"
                
    except Exception as e:
        return f"Erro ao verificar o clima: {str(e)}"

# Função para registrar histórico
def registrar_historico(session: Session, todo_id: str, user_id: str, action: str, field_name: str = None, old_value: str = None, new_value: str = None):
    """
    Registra uma entrada no histórico de uma tarefa
    """
    historico = TodoHistory(
        todo_id=todo_id,
        user_id=user_id,
        action=action,
        field_name=field_name,
        old_value=old_value,
        new_value=new_value
    )
    session.add(historico)
    session.commit()

# CRIAR TODO
@todo_router.post("/", response_model=TodoResponseSchema)
async def criar_todo(
    todo_schema: TodoSchema,
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    # Gerar sugestão baseada no clima se não foi fornecida
    if not todo_schema.suggestion:
        todo_schema.suggestion = gerar_sugestao_clima(todo_schema.activity_type, todo_schema.city)
    
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

    # Registrar criação no histórico
    registrar_historico(
        session=session,
        todo_id=novo_todo.id,
        user_id=current_user.id,
        action="created",
        field_name="tarefa_completa",
        old_value=None,
        new_value=f"Tarefa criada: {novo_todo.title}"
    )

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
    
    # Registrar mudanças no histórico
    for field, value in todo_data.model_dump().items():
        if value is not None:
            old_value = getattr(todo, field)
            if old_value != value:
                registrar_historico(
                    session=session,
                    todo_id=todo_id,
                    user_id=current_user.id,
                    action="updated",
                    field_name=field,
                    old_value=str(old_value),
                    new_value=str(value)
                )
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
    
    # Registrar exclusão no histórico
    registrar_historico(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id,
        action="deleted",
        field_name="tarefa_completa",
        old_value=f"Tarefa: {todo.title}",
        new_value=None
    )
    
    session.delete(todo)
    session.commit()
    
    return {"message": "Tarefa deletada com sucesso"}

# OBTER SUGESTÃO DE CLIMA
@todo_router.get("/sugestao-clima/{activity_type}/{city}")
async def obter_sugestao_clima(
    activity_type: str,
    city: str,
    current_user: User = Depends(verificar_token)
):
    """
    Obtém uma sugestão baseada no clima para um tipo de atividade e cidade específicos
    """
    sugestao = gerar_sugestao_clima(activity_type, city)
    
    return {
        "activity_type": activity_type,
        "city": city,
        "suggestion": sugestao,
        "timestamp": datetime.now().isoformat()
    }

# OBTER SUGESTÕES DE ATIVIDADES BASEADAS NO CLIMA
@todo_router.get("/sugestoes-clima/{city}")
async def obter_sugestoes_clima(
    city: str,
    current_user: User = Depends(verificar_token)
):
    """
    Obtém sugestões de atividades baseadas no clima da cidade
    """
    try:
        # Verificar se a API_KEY está configurada
        if not API_KEY or API_KEY == "sua_chave_da_api_aqui_123456789":
            return {"error": "API_KEY não configurada"}
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={API_KEY}&units=metric&lang=pt_br"
        response = requests.get(url)
        
        if response.status_code != 200:
            return {"error": "Não foi possível obter informações do clima."}
        
        weather_data = response.json()
        weather_description = weather_data.get('weather', [{}])[0].get('description', '').lower()
        temp = weather_data.get('main', {}).get('temp', 0)
        humidity = weather_data.get('main', {}).get('humidity', 0)
        wind_speed = weather_data.get('wind', {}).get('speed', 0)
        
        # Sugerir atividades baseadas no clima
        if any(word in weather_description for word in ['chuva', 'rain', 'storm', 'tempestade', 'thunderstorm']):
            sugestoes_internas = [
                "Organização da casa",
                "Leitura de um livro",
                "Exercícios em casa",
                "Projetos caseiros",
                "Estudo ou trabalho remoto",
                "Cozinhar algo especial",
                "Meditação ou yoga",
                "Jogos de tabuleiro",
                "Assistir filmes/séries",
                "Arte e artesanato"
            ]
            clima_info = f"🌧️ Está chovendo em {city} ({temp}°C)"
            recomendacao = "Perfeito para atividades internas!"
            
        elif any(word in weather_description for word in ['céu limpo', 'clear sky', 'ensolarado']):
            sugestoes_externas = [
                "Caminhada no parque",
                "Exercícios ao ar livre",
                "Passeio de bicicleta",
                "Piquenique",
                "Esportes externos",
                "Fotografia",
                "Jardinagem",
                "Corrida",
                "Yoga ao ar livre",
                "Visita a museus"
            ]
            clima_info = f"☀️ Tempo limpo e ensolarado em {city} ({temp}°C)"
            recomendacao = "Ideal para atividades externas!"
            
        elif temp < 15:
            sugestoes_internas = [
                "Ficar aconchegante em casa",
                "Leitura com chá quente",
                "Exercícios em casa",
                "Cozinhar sopas",
                "Meditação",
                "Jogos de tabuleiro",
                "Assistir filmes"
            ]
            sugestoes_externas = [
                "Caminhada com casaco",
                "Visita a museus",
                "Shopping center",
                "Café quente"
            ]
            clima_info = f"🥶 Temperatura baixa em {city} ({temp}°C)"
            recomendacao = "Vista-se adequadamente para atividades externas!"
            
        elif temp > 30:
            sugestoes_internas = [
                "Atividades em ambiente climatizado",
                "Exercícios em casa",
                "Leitura",
                "Trabalho remoto",
                "Meditação",
                "Jogos de tabuleiro"
            ]
            sugestoes_externas = [
                "Natação",
                "Atividades na sombra",
                "Visita a museus",
                "Shopping center"
            ]
            clima_info = f"🔥 Temperatura alta em {city} ({temp}°C)"
            recomendacao = "Mantenha-se hidratado e evite atividades externas nos horários mais quentes!"
            
        else:
            sugestoes_mistas = [
                "Atividades mistas (internas e externas)",
                "Visita a museus",
                "Shopping center",
                "Café ao ar livre",
                "Atividades culturais",
                "Exercícios moderados",
                "Passeios leves"
            ]
            clima_info = f"🌤️ Clima agradável em {city}: {weather_description.capitalize()} ({temp}°C)"
            recomendacao = "Bom para diversos tipos de atividades!"
        
        return {
            "city": city,
            "clima_info": clima_info,
            "recomendacao": recomendacao,
            "temperatura": temp,
            "umidade": humidity,
            "vento": wind_speed,
            "sugestoes_internas": sugestoes_internas if 'sugestoes_internas' in locals() else [],
            "sugestoes_externas": sugestoes_externas if 'sugestoes_externas' in locals() else [],
            "sugestoes_mistas": sugestoes_mistas if 'sugestoes_mistas' in locals() else [],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Erro ao verificar o clima: {str(e)}"}

# ATUALIZAR SUGESTÕES BASEADAS NO CLIMA
@todo_router.put("/{todo_id}/sugestao-clima", response_model=TodoResponseSchema)
async def atualizar_sugestao_clima(
    todo_id: str,
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    """
    Atualiza a sugestão de uma tarefa baseada no clima atual da cidade
    """
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Gerar nova sugestão baseada no clima atual
    nova_sugestao = gerar_sugestao_clima(todo.activity_type, todo.city)
    todo.suggestion = nova_sugestao
    todo.updated_at = datetime.now()
    
    session.commit()
    session.refresh(todo)
    
    return todo

# ATUALIZAR SUGESTÕES DE TODAS AS TAREFAS DO USUÁRIO
@todo_router.put("/atualizar-sugestoes-clima", response_model=dict)
async def atualizar_sugestoes_clima_todas(
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    """
    Atualiza as sugestões de todas as tarefas do usuário baseadas no clima atual
    """
    todos = session.query(Todo).filter(Todo.user_id == current_user.id).all()
    
    atualizadas = 0
    for todo in todos:
        nova_sugestao = gerar_sugestao_clima(todo.activity_type, todo.city)
        todo.suggestion = nova_sugestao
        todo.updated_at = datetime.now()
        atualizadas += 1
    
    session.commit()
    
    return {
        "message": f"Sugestões atualizadas para {atualizadas} tarefas baseadas no clima atual",
        "tarefas_atualizadas": atualizadas
    }

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

# Endpoints para estatísticas
@todo_router.get("/estatisticas")
async def obter_estatisticas(current_user: User = Depends(verificar_token)):
    # Total de tarefas, concluídas, pendentes, etc.
    pass # Placeholder for actual implementation

# NOVO ENDPOINT: Obter histórico de uma tarefa
@todo_router.get("/{todo_id}/historico", response_model=List[TodoHistorySchema])
async def obter_historico_tarefa(
    todo_id: str,
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token)
):
    """
    Obtém o histórico completo de uma tarefa
    """
    # Verificar se a tarefa existe e pertence ao usuário
    todo = session.query(Todo).filter(
        Todo.id == todo_id, 
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Buscar histórico da tarefa
    historico = session.query(TodoHistory).filter(
        TodoHistory.todo_id == todo_id
    ).order_by(TodoHistory.created_at.desc()).all()
    
    return historico

# NOVO ENDPOINT: Obter histórico de todas as tarefas do usuário
@todo_router.get("/historico/geral", response_model=List[TodoHistorySchema])
async def obter_historico_geral(
    session: Session = Depends(pegar_sessao),
    current_user: User = Depends(verificar_token),
    limit: int = Query(50, description="Limite de registros")
):
    """
    Obtém o histórico de todas as tarefas do usuário
    """
    historico = session.query(TodoHistory).filter(
        TodoHistory.user_id == current_user.id
    ).order_by(TodoHistory.created_at.desc()).limit(limit).all()
    
    return historico
