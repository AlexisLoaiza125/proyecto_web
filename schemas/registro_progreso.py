from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, field_validator


class RegistroProgresoBase(BaseModel):
    usuario_id: int
    fecha: date
    peso_kg: Optional[float] = None
    cintura_cm: Optional[float] = None
    cadera_cm: Optional[float] = None
    pecho_cm: Optional[float] = None
    brazo_cm: Optional[float] = None
    calorias_consumidas: Optional[int] = None
    proteinas_g: Optional[float] = None
    carbohidratos_g: Optional[float] = None
    grasas_g: Optional[float] = None
    nivel_energia: Optional[int] = None
    notas: Optional[str] = None

    @field_validator("nivel_energia")
    @classmethod
    def energia_valida(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("El nivel de energía debe estar entre 1 y 10.")
        return v

    @field_validator("calorias_consumidas")
    @classmethod
    def calorias_validas(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Las calorías no pueden ser negativas.")
        return v


class RegistroProgresoCreate(RegistroProgresoBase):
    pass


class RegistroProgresoUpdate(BaseModel):
    peso_kg: Optional[float] = None
    cintura_cm: Optional[float] = None
    cadera_cm: Optional[float] = None
    pecho_cm: Optional[float] = None
    brazo_cm: Optional[float] = None
    calorias_consumidas: Optional[int] = None
    proteinas_g: Optional[float] = None
    carbohidratos_g: Optional[float] = None
    grasas_g: Optional[float] = None
    nivel_energia: Optional[int] = None
    notas: Optional[str] = None


class RegistroProgresoResponse(RegistroProgresoBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
