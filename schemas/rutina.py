from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, field_validator


class RutinaBase(BaseModel):
    nombre: str
    usuario_id: int
    ejercicio_id: int
    series: Optional[int] = None
    repeticiones: Optional[int] = None
    peso_kg: Optional[float] = None
    duracion_min: Optional[int] = None
    fecha_programada: date
    notas: Optional[str] = None
    completada: Optional[bool] = False

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre de la rutina no puede estar vacío.")
        return v.strip()

    @field_validator("series")
    @classmethod
    def series_positivas(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("Las series deben ser mayor a 0.")
        return v

    @field_validator("repeticiones")
    @classmethod
    def reps_positivas(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("Las repeticiones deben ser mayor a 0.")
        return v


class RutinaCreate(RutinaBase):
    pass


class RutinaUpdate(BaseModel):
    nombre: Optional[str] = None
    series: Optional[int] = None
    repeticiones: Optional[int] = None
    peso_kg: Optional[float] = None
    duracion_min: Optional[int] = None
    fecha_programada: Optional[date] = None
    notas: Optional[str] = None
    completada: Optional[bool] = None


class RutinaResponse(RutinaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
