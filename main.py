
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from database import init_db

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
    license_info={"name": "MIT"},
)
