from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.rutina import RutinaCreate, RutinaUpdate, RutinaResponse
from services.rutina_service import RutinaService

router = APIRouter(prefix="/rutinas", tags=["Rutinas"])


@router.get("/", response_model=list[RutinaResponse], summary="Listar rutinas")
def listar_rutinas(
    solo_activos: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return RutinaService.obtener_todos(db, solo_activos=solo_activos, skip=skip, limit=limit)


@router.get(
    "/filtrar/",
    response_model=list[RutinaResponse],
    summary="Filtrar rutinas por usuario, fechas, completada",
)
def filtrar_rutinas(
    usuario_id: Optional[int] = Query(None),
    fecha_inicio: Optional[date] = Query(None, description="YYYY-MM-DD"),
    fecha_fin: Optional[date] = Query(None, description="YYYY-MM-DD"),
    completada: Optional[bool] = Query(None),
    solo_activos: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Filtro combinado por múltiples atributos (requisito 4)."""
    return RutinaService.filtrar(
        db,
        usuario_id=usuario_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        completada=completada,
        solo_activos=solo_activos,
    )


@router.get("/{rutina_id}", response_model=RutinaResponse, summary="Obtener rutina por ID")
def obtener_rutina(rutina_id: int, db: Session = Depends(get_db)):
    return RutinaService.obtener_por_id(db, rutina_id)


@router.post("/", response_model=RutinaResponse, status_code=201, summary="Crear rutina")
def crear_rutina(data: RutinaCreate, db: Session = Depends(get_db)):
    return RutinaService.crear_rutina(db, data)


@router.put("/{rutina_id}", response_model=RutinaResponse, summary="Actualizar rutina")
def actualizar_rutina(
    rutina_id: int, data: RutinaUpdate, db: Session = Depends(get_db)
):
    return RutinaService.actualizar_rutina(db, rutina_id, data)


@router.delete("/{rutina_id}", summary="Eliminar (lógicamente) rutina")
def eliminar_rutina(rutina_id: int, db: Session = Depends(get_db)):
    return RutinaService.eliminar_rutina(db, rutina_id)