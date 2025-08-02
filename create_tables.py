from models import Base, db

def criar_tabelas():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=db)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas() 