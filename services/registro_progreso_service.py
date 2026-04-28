from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.registro_progreso import RegistroProgreso
from models.usuario import Usuario
from schemas.registro_progreso import RegistroProgresoCreate, RegistroProgresoUpdate


class RegistroProgresoService:

    # ------------------------------------------------------------------ #
    #  CREATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def crear_registro(db: Session, data: RegistroProgresoCreate) -> RegistroProgreso:
        """
        Reglas de negocio:
        - El usuario debe existir y estar activo.
        - No se permite más de un registro por usuario por día (activo).
        """
        usuario = db.query(Usuario).filter(
            Usuario.id == data.usuario_id, Usuario.is_active == True  # noqa: E712
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario id={data.usuario_id} no encontrado o inactivo.",
            )

        duplicado = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id == data.usuario_id,
            RegistroProgreso.fecha == data.fecha,
            RegistroProgreso.is_active == True,  # noqa: E712
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Ya existe un registro activo para el usuario "
                    f"id={data.usuario_id} en la fecha {data.fecha}."
                ),
            )

        registro = RegistroProgreso(**data.model_dump())
        db.add(registro)
        db.commit()
        db.refresh(registro)
        return registro

    # ------------------------------------------------------------------ #
    #  READ                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def obtener_todos(
        db: Session,
        solo_activos: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RegistroProgreso]:
        query = db.query(RegistroProgreso)
        if solo_activos:
            query = query.filter(RegistroProgreso.is_active == True)  # noqa: E712
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def obtener_por_id(db: Session, registro_id: int) -> RegistroProgreso:
        registro = db.query(RegistroProgreso).filter(
            RegistroProgreso.id == registro_id
        ).first()
        if not registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con id={registro_id} no encontrado.",
            )
        return registro

    @staticmethod
    def filtrar(
        db: Session,
        usuario_id: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        solo_activos: bool = True,
    ) -> list[RegistroProgreso]:
        """Filtrado por usuario y rango de fechas (requisito 4)."""
        query = db.query(RegistroProgreso)
        if solo_activos:
            query = query.filter(RegistroProgreso.is_active == True)  # noqa: E712
        if usuario_id:
            query = query.filter(RegistroProgreso.usuario_id == usuario_id)
        if fecha_inicio:
            query = query.filter(RegistroProgreso.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(RegistroProgreso.fecha <= fecha_fin)
        return query.order_by(RegistroProgreso.fecha.desc()).all()

    @staticmethod
    def buscar_por_fecha(
        db: Session, usuario_id: int, fecha: date
    ) -> RegistroProgreso:
        """Búsqueda por fecha (requisito 5)."""
        registro = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id == usuario_id,
            RegistroProgreso.fecha == fecha,
            RegistroProgreso.is_active == True,  # noqa: E712
        ).first()
        if not registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró registro para usuario_id={usuario_id} en fecha={fecha}.",
            )
        return registro

    # ------------------------------------------------------------------ #
    #  UPDATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def actualizar_registro(
        db: Session, registro_id: int, data: RegistroProgresoUpdate
    ) -> RegistroProgreso:
        registro = RegistroProgresoService.obtener_por_id(db, registro_id)
        if not registro.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un registro inactivo.",
            )
        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(registro, campo, valor)
        db.commit()
        db.refresh(registro)
        return registro

    # ------------------------------------------------------------------ #
    #  DELETE (lógico)                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def eliminar_registro(db: Session, registro_id: int) -> dict:
        registro = RegistroProgresoService.obtener_por_id(db, registro_id)
        if not registro.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El registro ya está inactivo.",
            )
        registro.is_active = False
        db.commit()
        return {"mensaje": f"Registro id={registro_id} desactivado correctamente."}
