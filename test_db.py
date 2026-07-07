import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# No seu .env, a URL completa está em DATABASE_URL
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("Erro: Variável DATABASE_URL não encontrada no .env")
else:
    print(f"Testando conexão com: {db_url}")
    engine = create_engine(db_url)

    try:
        connection = engine.connect()
        print("Conectou com sucesso!")
        connection.close()
    except Exception as e:
        print("Erro ao conectar:", e)