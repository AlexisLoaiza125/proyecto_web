
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from database import init_db
from routes import usuarios_router, ejercicios_router, rutinas_router, registros_router
from middleware.exception_handlers import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)


# ---------------------------------------------------------------------------
# Instancia principal de la aplicación
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Fitness API",
    description="""
## API REST para gestión de entrenamiento y nutrición

### Recursos disponibles
- **Usuarios** – Registro y seguimiento de atletas
- **Ejercicios** – Catálogo de ejercicios clasificados por tipo y grupo muscular
- **Rutinas** – Planificación de sesiones de entrenamiento por usuario
- **Registros de Progreso** – Historial de medidas corporales y nutrición diaria

### Características
- CRUD completo con reglas de negocio
- Eliminación lógica (is_active) – los datos nunca se borran físicamente
- Filtros y búsquedas avanzadas
- Manejo robusto de errores con códigos HTTP estándar
- Documentación automática con Swagger / ReDoc
    """,
    version="1.0.0",
    contact={"name": "Fitness API Team"},
    license_info={"name": "Alexis Loaiza 67001155"},
)

# ---------------------------------------------------------------------------
# Manejadores globales de excepciones (requisito 7)
# ---------------------------------------------------------------------------
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ---------------------------------------------------------------------------
# Registro de routers
# ---------------------------------------------------------------------------
app.include_router(usuarios_router)
app.include_router(ejercicios_router)
app.include_router(rutinas_router)
app.include_router(registros_router)


# ---------------------------------------------------------------------------
# Eventos de ciclo de vida
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    """Crea las tablas en la BD si no existen al arrancar."""
    init_db()
    print("  Base de datos inicializada.")


# ---------------------------------------------------------------------------
# Endpoint raíz
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"], summary="Estado de la API")
def root():
    return {
        "mensaje": " Fitness API funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
