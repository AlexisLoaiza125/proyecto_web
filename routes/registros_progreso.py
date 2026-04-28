from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.registro_progreso import (
    RegistroProgresoCreate,
    RegistroProgresoUpdate,
    RegistroProgresoResponse,
)
from services.registro_progreso_service import RegistroProgresoService

router = APIRouter(prefix="/registros", tags=["Registros de Progreso"])


@router.get("/", response_model=list[RegistroProgresoResponse], summary="Listar registros")
def listar_registros(
    solo_activos: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return RegistroProgresoService.obtener_todos(
        db, solo_activos=solo_activos, skip=skip, limit=limit
    )


@router.get(
    "/filtrar/",
    response_model=list[RegistroProgresoResponse],
    summary="Filtrar registros por usuario y fechas",
)
def filtrar_registros(
    usuario_id: Optional[int] = Query(None),
    fecha_inicio: Optional[date] = Query(None, description="YYYY-MM-DD"),
    fecha_fin: Optional[date] = Query(None, description="YYYY-MM-DD"),
    solo_activos: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Filtra registros por usuario y rango de fechas (requisito 4)."""
    return RegistroProgresoService.filtrar(
        db,
        usuario_id=usuario_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        solo_activos=solo_activos,
    )


@router.get(
    "/buscar/",
    response_model=RegistroProgresoResponse,
    summary="Buscar registro por usuario y fecha exacta",
)
def buscar_por_fecha(
    usuario_id: int = Query(...),
    fecha: date = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Búsqueda por fecha (requisito 5)."""
    return RegistroProgresoService.buscar_por_fecha(db, usuario_id, fecha)


@router.get(
    "/{registro_id}",
    response_model=RegistroProgresoResponse,
    summary="Obtener registro por ID",
)
def obtener_registro(registro_id: int, db: Session = Depends(get_db)):
    return RegistroProgresoService.obtener_por_id(db, registro_id)


@router.post(
    "/",
    response_model=RegistroProgresoResponse,
    status_code=201,
    summary="Crear registro de progreso",
)
def crear_registro(data: RegistroProgresoCreate, db: Session = Depends(get_db)):
    return RegistroProgresoService.crear_registro(db, data)


@router.put(
    "/{registro_id}",
    response_model=RegistroProgresoResponse,
    summary="Actualizar registro",
)
def actualizar_registro(
    registro_id: int, data: RegistroProgresoUpdate, db: Session = Depends(get_db)
):
    return RegistroProgresoService.actualizar_registro(db, registro_id, data)


@router.delete("/{registro_id}", summary="Eliminar (lógicamente) registro")
def eliminar_registro(registro_id: int, db: Session = Depends(get_db)):
    return RegistroProgresoService.eliminar_registro(db, registro_id)
