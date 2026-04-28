from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./fitness.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Solo necesario para SQLite
    echo=False,  # Cambiar a True para ver SQL en consola
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""
    pass


def get_db():
    """
    Dependency de FastAPI para inyectar sesión de base de datos.
    Garantiza que la sesión se cierre al terminar el request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
