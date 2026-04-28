from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


OBJETIVOS_VALIDOS = {"perder_peso", "ganar_musculo", "mantenimiento", "resistencia"}


class UsuarioBase(BaseModel):
    nombre: str
    email: str
    username: str
    edad: Optional[int] = None
    peso_kg: Optional[float] = None
    altura_cm: Optional[float] = None
    objetivo: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip()

    @field_validator("edad")
    @classmethod
    def edad_valida(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 10 or v > 120):
            raise ValueError("La edad debe estar entre 10 y 120 años.")
        return v

    @field_validator("peso_kg")
    @classmethod
    def peso_valido(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("El peso debe ser mayor a 0.")
        return v

    @field_validator("objetivo")
    @classmethod
    def objetivo_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in OBJETIVOS_VALIDOS:
            raise ValueError(f"Objetivo debe ser uno de: {OBJETIVOS_VALIDOS}")
        return v


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    peso_kg: Optional[float] = None
    altura_cm: Optional[float] = None
    objetivo: Optional[str] = None

    @field_validator("objetivo")
    @classmethod
    def objetivo_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in OBJETIVOS_VALIDOS:
            raise ValueError(f"Objetivo debe ser uno de: {OBJETIVOS_VALIDOS}")
        return v


class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
