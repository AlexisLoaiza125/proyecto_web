from database.connection import Base, engine


def init_db():
    """Crea todas las tablas definidas en los modelos."""
    from models import usuario, ejercicio, rutina, registro_progreso  # noqa: F401
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada.")