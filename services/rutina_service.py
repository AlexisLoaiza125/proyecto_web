from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.rutina import Rutina
from models.usuario import Usuario
from models.ejercicio import Ejercicio
from schemas.rutina import RutinaCreate, RutinaUpdate


class RutinaService:

    # ------------------------------------------------------------------ #
    #  CREATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def crear_rutina(db: Session, data: RutinaCreate) -> Rutina:
        """
        Reglas de negocio:
        - El usuario debe existir y estar activo.
        - El ejercicio debe existir y estar activo.
        - La fecha programada no puede ser en el pasado.
        """
        usuario = db.query(Usuario).filter(
            Usuario.id == data.usuario_id, Usuario.is_active == True  # noqa: E712
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario id={data.usuario_id} no encontrado o inactivo.",
            )

        ejercicio = db.query(Ejercicio).filter(
            Ejercicio.id == data.ejercicio_id, Ejercicio.is_active == True  # noqa: E712
        ).first()
        if not ejercicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ejercicio id={data.ejercicio_id} no encontrado o inactivo.",
            )

        if data.fecha_programada < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha programada no puede ser anterior a hoy.",
            )

        rutina = Rutina(**data.model_dump())
        db.add(rutina)
        db.commit()
        db.refresh(rutina)
        return rutina

    # ------------------------------------------------------------------ #
    #  READ                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def obtener_todos(
        db: Session,
        solo_activos: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Rutina]:
        query = db.query(Rutina)
        if solo_activos:
            query = query.filter(Rutina.is_active == True)  # noqa: E712
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def obtener_por_id(db: Session, rutina_id: int) -> Rutina:
        rutina = db.query(Rutina).filter(Rutina.id == rutina_id).first()
        if not rutina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rutina con id={rutina_id} no encontrada.",
            )
        return rutina

    @staticmethod
    def filtrar(
        db: Session,
        usuario_id: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        completada: Optional[bool] = None,
        solo_activos: bool = True,
    ) -> list[Rutina]:
        """Filtrado por usuario, rango de fechas y estado de completitud (requisito 4)."""
        query = db.query(Rutina)
        if solo_activos:
            query = query.filter(Rutina.is_active == True)  # noqa: E712
        if usuario_id:
            query = query.filter(Rutina.usuario_id == usuario_id)
        if fecha_inicio:
            query = query.filter(Rutina.fecha_programada >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Rutina.fecha_programada <= fecha_fin)
        if completada is not None:
            query = query.filter(Rutina.completada == completada)
        return query.all()

    # ------------------------------------------------------------------ #
    #  UPDATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def actualizar_rutina(
        db: Session, rutina_id: int, data: RutinaUpdate
    ) -> Rutina:
        rutina = RutinaService.obtener_por_id(db, rutina_id)
        if not rutina.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar una rutina inactiva.",
            )
        cambios = data.model_dump(exclude_unset=True)
        if "fecha_programada" in cambios and cambios["fecha_programada"] < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva fecha programada no puede ser anterior a hoy.",
            )
        for campo, valor in cambios.items():
            setattr(rutina, campo, valor)
        db.commit()
        db.refresh(rutina)
        return rutina

    # ------------------------------------------------------------------ #
    #  DELETE (lógico)                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def eliminar_rutina(db: Session, rutina_id: int) -> dict:
        rutina = RutinaService.obtener_por_id(db, rutina_id)
        if not rutina.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La rutina ya está inactiva.",
            )
        rutina.is_active = False
        db.commit()
        return {"mensaje": f"Rutina id={rutina_id} desactivada correctamente."}
