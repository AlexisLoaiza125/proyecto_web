from routes.usuarios import router as usuarios_router
from routes.ejercicios import router as ejercicios_router
from routes.rutinas import router as rutinas_router
from routes.registros_progreso import router as registros_router

__all__ = ["usuarios_router", "ejercicios_router", "rutinas_router", "registros_router"]
