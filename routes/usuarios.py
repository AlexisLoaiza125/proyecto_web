from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioResponse], summary="Listar usuarios")
def listar_usuarios(
    solo_activos: bool = Query(True, description="True = solo activos, False = todos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Devuelve la lista de usuarios. Por defecto solo los activos."""
    return UsuarioService.obtener_todos(db, solo_activos=solo_activos, skip=skip, limit=limit)


@router.get(
    "/filtrar/",
    response_model=list[UsuarioResponse],
    summary="Filtrar usuarios por atributos",
)
def filtrar_usuarios(
    objetivo: Optional[str] = Query(None, description="perder_peso | ganar_musculo | mantenimiento | resistencia"),
    solo_activos: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Filtra usuarios por objetivo fitness (requisito 4)."""
    return UsuarioService.filtrar(db, objetivo=objetivo, solo_activos=solo_activos)


@router.get(
    "/username/{username}",
    response_model=UsuarioResponse,
    summary="Buscar usuario por username",
)
def obtener_por_username(username: str, db: Session = Depends(get_db)):
    """Búsqueda por atributo distinto al ID (requisito 5)."""
    return UsuarioService.obtener_por_username(db, username)


@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario por ID")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService.obtener_por_id(db, usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201, summary="Crear usuario")
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario. Email y username deben ser únicos."""
    return UsuarioService.crear_usuario(db, data)


@router.put("/{usuario_id}", response_model=UsuarioResponse, summary="Actualizar usuario")
def actualizar_usuario(
    usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)
):
    return UsuarioService.actualizar_usuario(db, usuario_id, data)


@router.delete("/{usuario_id}", summary="Eliminar (lógicamente) usuario")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminación lógica: cambia is_active a False (requisito 3)."""
    return UsuarioService.eliminar_usuario(db, usuario_id)
