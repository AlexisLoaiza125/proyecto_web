from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


TIPOS_VALIDOS = {"fuerza", "cardio", "flexibilidad", "hiit", "funcional"}
GRUPOS_VALIDOS = {
    "pecho", "espalda", "piernas", "hombros", "biceps",
    "triceps", "core", "gluteos", "full_body", "cardio",
}
NIVELES_VALIDOS = {"principiante", "intermedio", "avanzado"}


class EjercicioBase(BaseModel):
    nombre: str
    tipo: str
    grupo_muscular: Optional[str] = None
    nivel_dificultad: Optional[str] = "intermedio"
    descripcion: Optional[str] = None
    instrucciones: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip()

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo debe ser uno de: {TIPOS_VALIDOS}")
        return v

    @field_validator("nivel_dificultad")
    @classmethod
    def nivel_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in NIVELES_VALIDOS:
            raise ValueError(f"Nivel debe ser uno de: {NIVELES_VALIDOS}")
        return v


class EjercicioCreate(EjercicioBase):
    pass


class EjercicioUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    grupo_muscular: Optional[str] = None
    nivel_dificultad: Optional[str] = None
    descripcion: Optional[str] = None
    instrucciones: Optional[str] = None

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo debe ser uno de: {TIPOS_VALIDOS}")
        return v


class EjercicioResponse(EjercicioBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
