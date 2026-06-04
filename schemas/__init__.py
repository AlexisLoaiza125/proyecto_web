from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, field_validator

OBJETIVOS = {"perder_peso","ganar_musculo","mantenimiento","resistencia"}
TIPOS_EJ  = {"fuerza","cardio","flexibilidad","hiit","funcional"}
NIVELES   = {"principiante","intermedio","avanzado"}

# ── USUARIO ──────────────────────────────────────────────────────────────────
class UsuarioCreate(BaseModel):
    nombre: str; email: str; username: str
    edad: Optional[int]=None; peso_kg: Optional[float]=None
    altura_cm: Optional[float]=None; objetivo: Optional[str]=None
    foto_perfil: Optional[str]=None

    @field_validator("nombre")
    @classmethod
    def nombre_ok(cls,v):
        if not v.strip(): raise ValueError("Nombre vacío")
        return v.strip()
    @field_validator("edad")
    @classmethod
    def edad_ok(cls,v):
        if v and not(10<=v<=80): raise ValueError("Edad 10-80")
        return v
    @field_validator("objetivo")
    @classmethod
    def obj_ok(cls,v):
        if v and v not in OBJETIVOS: raise ValueError(f"Objetivo: {OBJETIVOS}")
        return v
    @field_validator("peso")
    @classmethod
    def peso_ok(cls,v):
        if v is not None and not(30<=v<=200): raise ValueError("Peso 30-200")
        return v
    @field_validator("altura")
    @classmethod
    def altura_ok(cls,v):
        if v is not None and not(100<=v<=300): raise ValueError("peso 100-300")
        return v


class UsuarioUpdate(BaseModel):
    nombre: Optional[str]=None; edad: Optional[int]=None
    peso_kg: Optional[float]=None; altura_cm: Optional[float]=None
    objetivo: Optional[str]=None; foto_perfil: Optional[str]=None
    @field_validator("objetivo")
    @classmethod
    def obj_ok(cls,v):
        if v and v not in OBJETIVOS: raise ValueError(f"Objetivo: {OBJETIVOS}")
        return v

class UsuarioResponse(UsuarioCreate):
    id: int; is_active: bool; created_at: datetime; updated_at: datetime
    model_config={"from_attributes":True}

# ── EJERCICIO ─────────────────────────────────────────────────────────────────
class EjercicioCreate(BaseModel):
    nombre: str; tipo: str
    grupo_muscular: Optional[str]=None
    nivel_dificultad: Optional[str]="intermedio"
    descripcion: Optional[str]=None; instrucciones: Optional[str]=None
    imagen_url: Optional[str]=None; video_url: Optional[str]=None

    @field_validator("nombre")
    @classmethod
    def nom_ok(cls,v):
        if not v.strip(): raise ValueError("Nombre vacío")
        return v.strip()
    @field_validator("tipo")
    @classmethod
    def tipo_ok(cls,v):
        if v not in TIPOS_EJ: raise ValueError(f"Tipo: {TIPOS_EJ}")
        return v

class EjercicioUpdate(BaseModel):
    nombre: Optional[str]=None; tipo: Optional[str]=None
    grupo_muscular: Optional[str]=None; nivel_dificultad: Optional[str]=None
    descripcion: Optional[str]=None; instrucciones: Optional[str]=None
    imagen_url: Optional[str]=None; video_url: Optional[str]=None

class EjercicioResponse(EjercicioCreate):
    id: int; is_active: bool; created_at: datetime; updated_at: datetime
    model_config={"from_attributes":True}

# ── RUTINA ────────────────────────────────────────────────────────────────────
class RutinaCreate(BaseModel):
    nombre: str; usuario_id: int; ejercicio_id: int
    series: Optional[int]=None; repeticiones: Optional[int]=None
    peso_kg: Optional[float]=None; duracion_min: Optional[int]=None
    fecha_programada: date; notas: Optional[str]=None; completada: Optional[bool]=False

    @field_validator("series","repeticiones")
    @classmethod
    def pos(cls,v):
        if v and v<=0: raise ValueError("Debe ser >0")
        return v

class RutinaUpdate(BaseModel):
    nombre: Optional[str]=None; series: Optional[int]=None
    repeticiones: Optional[int]=None; peso_kg: Optional[float]=None
    duracion_min: Optional[int]=None; fecha_programada: Optional[date]=None
    notas: Optional[str]=None; completada: Optional[bool]=None

class RutinaResponse(RutinaCreate):
    id: int; is_active: bool; created_at: datetime; updated_at: datetime
    model_config={"from_attributes":True}

# ── REGISTRO PROGRESO ─────────────────────────────────────────────────────────
class RegistroProgresoCreate(BaseModel):
    usuario_id: int; fecha: date
    peso_kg: Optional[float]=None; cintura_cm: Optional[float]=None
    cadera_cm: Optional[float]=None; pecho_cm: Optional[float]=None
    brazo_cm: Optional[float]=None; calorias_consumidas: Optional[int]=None
    proteinas_g: Optional[float]=None; carbohidratos_g: Optional[float]=None
    grasas_g: Optional[float]=None; nivel_energia: Optional[int]=None
    notas: Optional[str]=None

    @field_validator("nivel_energia")
    @classmethod
    def niv(cls,v):
        if v and not(1<=v<=10): raise ValueError("Energía 1-10")
        return v
    @field_validator("calorias_consumidas")
    @classmethod
    def cal(cls,v):
        if v and v<0: raise ValueError("Calorías ≥ 0")
        return v

class RegistroProgresoUpdate(BaseModel):
    peso_kg: Optional[float]=None; cintura_cm: Optional[float]=None
    cadera_cm: Optional[float]=None; pecho_cm: Optional[float]=None
    brazo_cm: Optional[float]=None; calorias_consumidas: Optional[int]=None
    proteinas_g: Optional[float]=None; carbohidratos_g: Optional[float]=None
    grasas_g: Optional[float]=None; nivel_energia: Optional[int]=None
    notas: Optional[str]=None

class RegistroProgresoResponse(RegistroProgresoCreate):
    id: int; is_active: bool; created_at: datetime; updated_at: datetime
    model_config={"from_attributes":True}
