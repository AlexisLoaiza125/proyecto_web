from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.ejercicio import EjercicioCreate, EjercicioUpdate, EjercicioResponse
from services.ejercicio_service import EjercicioService

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])


@router.get("/", response_model=list[EjercicioResponse], summary="Listar ejercicios")
def listar_ejercicios(
    solo_activos: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return EjercicioService.obtener_todos(db, solo_activos=solo_activos, skip=skip, limit=limit)


@router.get(
    "/filtrar/",
    response_model=list[EjercicioResponse],
    summary="Filtrar ejercicios por tipo / grupo / nivel",
)
def filtrar_ejercicios(
    tipo: Optional[str] = Query(None, description="fuerza | cardio | flexibilidad | hiit | funcional"),
    grupo_muscular: Optional[str] = Query(None),
    nivel_dificultad: Optional[str] = Query(None, description="principiante | intermedio | avanzado"),
    solo_activos: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Filtra ejercicios por tipo, grupo muscular y nivel (requisito 4)."""
    return EjercicioService.filtrar(
        db,
        tipo=tipo,
        grupo_muscular=grupo_muscular,
        nivel_dificultad=nivel_dificultad,
        solo_activos=solo_activos,
    )


@router.get(
    "/buscar/",
    response_model=list[EjercicioResponse],
    summary="Buscar ejercicios por nombre",
)
def buscar_ejercicio(
    nombre: str = Query(..., min_length=2, description="Búsqueda parcial por nombre"),
    db: Session = Depends(get_db),
):
    """Búsqueda por nombre (requisito 5) — case-insensitive."""
    return EjercicioService.buscar_por_nombre(db, nombre)


@router.get("/{ejercicio_id}", response_model=EjercicioResponse, summary="Obtener ejercicio por ID")
def obtener_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
    return EjercicioService.obtener_por_id(db, ejercicio_id)


@router.post("/", response_model=EjercicioResponse, status_code=201, summary="Crear ejercicio")
def crear_ejercicio(data: EjercicioCreate, db: Session = Depends(get_db)):
    return EjercicioService.crear_ejercicio(db, data)


@router.put("/{ejercicio_id}", response_model=EjercicioResponse, summary="Actualizar ejercicio")
def actualizar_ejercicio(
    ejercicio_id: int, data: EjercicioUpdate, db: Session = Depends(get_db)
):
    return EjercicioService.actualizar_ejercicio(db, ejercicio_id, data)


@router.delete("/{ejercicio_id}", summary="Eliminar (lógicamente) ejercicio")
def eliminar_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
    return EjercicioService.eliminar_ejercicio(db, ejercicio_id)
