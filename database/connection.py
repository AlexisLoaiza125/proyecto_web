import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Log de diagnóstico — quitar después de resolver
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL no está definida.")
else:
    # Solo muestra el inicio para no exponer la contraseña
    print(f"✅ DATABASE_URL encontrada: {DATABASE_URL[:30]}...")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # ← verifica la conexión antes de usarla
    pool_recycle=300,     # ← recicla conexiones cada 5 min (importante en Supabase free)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()