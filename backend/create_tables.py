from database.db import engine, Base
from database.models import Ad


print("[*] Criando tabelas...")

Base.metadata.create_all(bind=engine)

print("[🔥 TABELAS CRIADAS COM SUCESSO 🔥]")