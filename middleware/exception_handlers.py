from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

async def validation_handler(request: Request, exc: RequestValidationError):
    errors = [{"campo": "→".join(str(l) for l in e["loc"]), "mensaje": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "Validación fallida", "detalle": errors})

async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"error": "Error de base de datos", "detalle": str(exc)})

async def generic_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Error interno", "detalle": str(exc)})
