
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate


class UsuarioService:

    # ------------------------------------------------------------------ #
    #  CREATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def crear_usuario(db: Session, data: UsuarioCreate) -> Usuario:
        """
        Regla de negocio:
        - El email y el username deben ser únicos en usuarios ACTIVOS.
        """
        if db.query(Usuario).filter(
            Usuario.email == data.email, Usuario.is_active == True  # noqa: E712
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario activo con el email '{data.email}'.",
            )
        if db.query(Usuario).filter(
            Usuario.username == data.username, Usuario.is_active == True  # noqa: E712
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario activo con el username '{data.username}'.",
            )

        usuario = Usuario(**data.model_dump())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    # ------------------------------------------------------------------ #
    #  READ                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def obtener_todos(
        db: Session,
        solo_activos: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Usuario]:
        query = db.query(Usuario)
        if solo_activos:
            query = query.filter(Usuario.is_active == True)  # noqa: E712
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int) -> Usuario:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id={usuario_id} no encontrado.",
            )
        return usuario

    @staticmethod
    def obtener_por_username(db: Session, username: str) -> Usuario:
        """Búsqueda por atributo distinto al ID (requisito 5)."""
        usuario = db.query(Usuario).filter(
            Usuario.username == username, Usuario.is_active == True  # noqa: E712
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con username='{username}' no encontrado.",
            )
        return usuario

    @staticmethod
    def filtrar(
        db: Session,
        objetivo: Optional[str] = None,
        solo_activos: bool = True,
    ) -> list[Usuario]:
        """Filtrado por atributos (requisito 4)."""
        query = db.query(Usuario)
        if solo_activos:
            query = query.filter(Usuario.is_active == True)  # noqa: E712
        if objetivo:
            query = query.filter(Usuario.objetivo == objetivo)
        return query.all()

    # ------------------------------------------------------------------ #
    #  UPDATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def actualizar_usuario(
        db: Session, usuario_id: int, data: UsuarioUpdate
    ) -> Usuario:
        usuario = UsuarioService.obtener_por_id(db, usuario_id)
        if not usuario.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un usuario inactivo.",
            )
        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario

    # ------------------------------------------------------------------ #
    #  DELETE (lógico)                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int) -> dict:
        """
        Eliminación lógica (requisito 3).
        Regla de negocio: no se puede eliminar si tiene rutinas ACTIVAS.
        """
        from models.rutina import Rutina

        usuario = UsuarioService.obtener_por_id(db, usuario_id)
        if not usuario.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está inactivo.",
            )
        rutinas_activas = db.query(Rutina).filter(
            Rutina.usuario_id == usuario_id, Rutina.is_active == True  # noqa: E712
        ).count()
        if rutinas_activas > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"No se puede desactivar el usuario: tiene {rutinas_activas} "
                    "rutina(s) activa(s). Elimínalas primero."
                ),
            )
        usuario.is_active = False
        db.commit()
        return {"mensaje": f"Usuario id={usuario_id} desactivado correctamente."}
