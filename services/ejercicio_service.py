from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.ejercicio import Ejercicio
from schemas.ejercicio import EjercicioCreate, EjercicioUpdate


class EjercicioService:

    # ------------------------------------------------------------------ #
    #  CREATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def crear_ejercicio(db: Session, data: EjercicioCreate) -> Ejercicio:
        """
        Regla de negocio: No se permiten ejercicios duplicados
        (mismo nombre + tipo en estado activo).
        """
        existente = db.query(Ejercicio).filter(
            Ejercicio.nombre == data.nombre,
            Ejercicio.tipo == data.tipo,
            Ejercicio.is_active == True,  # noqa: E712
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe el ejercicio '{data.nombre}' de tipo '{data.tipo}'.",
            )
        ejercicio = Ejercicio(**data.model_dump())
        db.add(ejercicio)
        db.commit()
        db.refresh(ejercicio)
        return ejercicio

    # ------------------------------------------------------------------ #
    #  READ                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def obtener_todos(
        db: Session,
        solo_activos: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Ejercicio]:
        query = db.query(Ejercicio)
        if solo_activos:
            query = query.filter(Ejercicio.is_active == True)  # noqa: E712
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def obtener_por_id(db: Session, ejercicio_id: int) -> Ejercicio:
        ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
        if not ejercicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ejercicio con id={ejercicio_id} no encontrado.",
            )
        return ejercicio

    @staticmethod
    def buscar_por_nombre(db: Session, nombre: str) -> list[Ejercicio]:
        """Búsqueda por nombre (requisito 5) — búsqueda parcial case-insensitive."""
        return (
            db.query(Ejercicio)
            .filter(
                Ejercicio.nombre.ilike(f"%{nombre}%"),
                Ejercicio.is_active == True,  # noqa: E712
            )
            .all()
        )

    @staticmethod
    def filtrar(
        db: Session,
        tipo: Optional[str] = None,
        grupo_muscular: Optional[str] = None,
        nivel_dificultad: Optional[str] = None,
        solo_activos: bool = True,
    ) -> list[Ejercicio]:
        """
        Filtrado por múltiples atributos (requisito 4).
        Todos los parámetros son opcionales y se combinan (AND).
        """
        query = db.query(Ejercicio)
        if solo_activos:
            query = query.filter(Ejercicio.is_active == True)  # noqa: E712
        if tipo:
            query = query.filter(Ejercicio.tipo == tipo)
        if grupo_muscular:
            query = query.filter(Ejercicio.grupo_muscular == grupo_muscular)
        if nivel_dificultad:
            query = query.filter(Ejercicio.nivel_dificultad == nivel_dificultad)
        return query.all()

    # ------------------------------------------------------------------ #
    #  UPDATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def actualizar_ejercicio(
        db: Session, ejercicio_id: int, data: EjercicioUpdate
    ) -> Ejercicio:
        ejercicio = EjercicioService.obtener_por_id(db, ejercicio_id)
        if not ejercicio.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un ejercicio inactivo.",
            )
        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(ejercicio, campo, valor)
        db.commit()
        db.refresh(ejercicio)
        return ejercicio

    # ------------------------------------------------------------------ #
    #  DELETE (lógico)                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def eliminar_ejercicio(db: Session, ejercicio_id: int) -> dict:
        """
        Regla de negocio: no eliminar si hay rutinas activas que lo usan.
        """
        from models.rutina import Rutina

        ejercicio = EjercicioService.obtener_por_id(db, ejercicio_id)
        if not ejercicio.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ejercicio ya está inactivo.",
            )
        rutinas_activas = db.query(Rutina).filter(
            Rutina.ejercicio_id == ejercicio_id, Rutina.is_active == True  # noqa: E712
        ).count()
        if rutinas_activas > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"No se puede desactivar: el ejercicio está en uso en "
                    f"{rutinas_activas} rutina(s) activa(s)."
                ),
            )
        ejercicio.is_active = False
        db.commit()
        return {"mensaje": f"Ejercicio id={ejercicio_id} desactivado correctamente."}
