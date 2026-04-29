from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Errores de validación Pydantic → 422 con detalle legible."""
    errores = []
    for error in exc.errors():
        campo = " → ".join(str(loc) for loc in error["loc"])
        errores.append({"campo": campo, "mensaje": error["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Error de validación", "detalle": errores},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Errores de base de datos no controlados → 500."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Error interno de base de datos", "detalle": str(exc)},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Captura cualquier excepción inesperada → 500."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Error interno del servidor", "detalle": str(exc)},
    )
