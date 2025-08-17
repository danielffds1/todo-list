# migrate_database.py
from models import Base, db, TodoHistory
from sqlalchemy import text

def migrar_banco():
    """Executa a migração do banco de dados"""
    try:
        # Criar a nova tabela de histórico
        Base.metadata.create_all(bind=db)
        print("✅ Migração concluída com sucesso!")
        print("📋 Nova tabela 'todo_history' criada")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")

if __name__ == "__main__":
    migrar_banco()
