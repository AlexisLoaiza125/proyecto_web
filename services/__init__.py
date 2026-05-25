from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.usuario import Usuario
from models.ejercicio import Ejercicio
from models.rutina import Rutina
from models.registro_progreso import RegistroProgreso
from schemas import (UsuarioCreate, UsuarioUpdate, EjercicioCreate, EjercicioUpdate,
                     RutinaCreate, RutinaUpdate, RegistroProgresoCreate, RegistroProgresoUpdate)

# ── helpers ──────────────────────────────────────────────────────────────────
def _get_or_404(db, Model, id_):
    obj = db.query(Model).filter(Model.id == id_).first()
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{Model.__tablename__} id={id_} no encontrado.")
    return obj

# ── USUARIO ──────────────────────────────────────────────────────────────────
class UsuarioService:
    @staticmethod
    def crear(db:Session, data:UsuarioCreate):
        if db.query(Usuario).filter(Usuario.email==data.email, Usuario.is_active==True).first():
            raise HTTPException(400, f"Email '{data.email}' ya registrado.")
        if db.query(Usuario).filter(Usuario.username==data.username, Usuario.is_active==True).first():
            raise HTTPException(400, f"Username '{data.username}' ya existe.")
        u = Usuario(**data.model_dump()); db.add(u); db.commit(); db.refresh(u); return u

    @staticmethod
    def listar(db:Session, solo_activos=True, skip=0, limit=100, q:Optional[str]=None):
        qry = db.query(Usuario)
        if solo_activos: qry = qry.filter(Usuario.is_active==True)
        if q: qry = qry.filter(Usuario.nombre.ilike(f"%{q}%") | Usuario.username.ilike(f"%{q}%"))
        return qry.offset(skip).limit(limit).all()

    @staticmethod
    def por_id(db:Session, id_): return _get_or_404(db, Usuario, id_)

    @staticmethod
    def por_username(db:Session, username):
        u = db.query(Usuario).filter(Usuario.username==username, Usuario.is_active==True).first()
        if not u: raise HTTPException(404, f"Usuario '{username}' no encontrado.")
        return u

    @staticmethod
    def filtrar(db:Session, objetivo=None, solo_activos=True):
        qry = db.query(Usuario)
        if solo_activos: qry = qry.filter(Usuario.is_active==True)
        if objetivo: qry = qry.filter(Usuario.objetivo==objetivo)
        return qry.all()

    @staticmethod
    def actualizar(db:Session, id_, data:UsuarioUpdate):
        u = _get_or_404(db, Usuario, id_)
        if not u.is_active: raise HTTPException(400, "Usuario inactivo.")
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(u,k,v)
        db.commit(); db.refresh(u); return u

    @staticmethod
    def eliminar(db:Session, id_):
        u = _get_or_404(db, Usuario, id_)
        if not u.is_active: raise HTTPException(400, "Ya inactivo.")
        n = db.query(Rutina).filter(Rutina.usuario_id==id_, Rutina.is_active==True).count()
        if n: raise HTTPException(409, f"Tiene {n} rutina(s) activa(s). Elimínalas primero.")
        u.is_active = False; db.commit()
        return {"mensaje": f"Usuario id={id_} desactivado."}

# ── EJERCICIO ─────────────────────────────────────────────────────────────────
class EjercicioService:
    @staticmethod
    def crear(db:Session, data:EjercicioCreate):
        if db.query(Ejercicio).filter(Ejercicio.nombre==data.nombre, Ejercicio.tipo==data.tipo, Ejercicio.is_active==True).first():
            raise HTTPException(400, f"Ejercicio '{data.nombre}' tipo '{data.tipo}' ya existe.")
        e = Ejercicio(**data.model_dump()); db.add(e); db.commit(); db.refresh(e); return e

    @staticmethod
    def listar(db:Session, solo_activos=True, skip=0, limit=100, q:Optional[str]=None):
        qry = db.query(Ejercicio)
        if solo_activos: qry = qry.filter(Ejercicio.is_active==True)
        if q: qry = qry.filter(Ejercicio.nombre.ilike(f"%{q}%"))
        return qry.offset(skip).limit(limit).all()

    @staticmethod
    def por_id(db:Session, id_): return _get_or_404(db, Ejercicio, id_)

    @staticmethod
    def buscar_nombre(db:Session, nombre):
        return db.query(Ejercicio).filter(Ejercicio.nombre.ilike(f"%{nombre}%"), Ejercicio.is_active==True).all()

    @staticmethod
    def filtrar(db:Session, tipo=None, grupo=None, nivel=None, solo_activos=True):
        qry = db.query(Ejercicio)
        if solo_activos: qry = qry.filter(Ejercicio.is_active==True)
        if tipo:  qry = qry.filter(Ejercicio.tipo==tipo)
        if grupo: qry = qry.filter(Ejercicio.grupo_muscular==grupo)
        if nivel: qry = qry.filter(Ejercicio.nivel_dificultad==nivel)
        return qry.all()

    @staticmethod
    def actualizar(db:Session, id_, data:EjercicioUpdate):
        e = _get_or_404(db, Ejercicio, id_)
        if not e.is_active: raise HTTPException(400, "Ejercicio inactivo.")
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(e,k,v)
        db.commit(); db.refresh(e); return e

    @staticmethod
    def eliminar(db:Session, id_):
        e = _get_or_404(db, Ejercicio, id_)
        if not e.is_active: raise HTTPException(400, "Ya inactivo.")
        n = db.query(Rutina).filter(Rutina.ejercicio_id==id_, Rutina.is_active==True).count()
        if n: raise HTTPException(409, f"En uso en {n} rutina(s) activa(s).")
        e.is_active = False; db.commit()
        return {"mensaje": f"Ejercicio id={id_} desactivado."}

# ── RUTINA ────────────────────────────────────────────────────────────────────
class RutinaService:
    @staticmethod
    def crear(db:Session, data:RutinaCreate):
        if not db.query(Usuario).filter(Usuario.id==data.usuario_id, Usuario.is_active==True).first():
            raise HTTPException(404, f"Usuario id={data.usuario_id} no encontrado o inactivo.")
        if not db.query(Ejercicio).filter(Ejercicio.id==data.ejercicio_id, Ejercicio.is_active==True).first():
            raise HTTPException(404, f"Ejercicio id={data.ejercicio_id} no encontrado o inactivo.")
        if data.fecha_programada < date.today():
            raise HTTPException(400, "Fecha no puede ser en el pasado.")
        r = Rutina(**data.model_dump()); db.add(r); db.commit(); db.refresh(r); return r

    @staticmethod
    def listar(db:Session, solo_activos=True, skip=0, limit=100):
        qry = db.query(Rutina)
        if solo_activos: qry = qry.filter(Rutina.is_active==True)
        return qry.offset(skip).limit(limit).all()

    @staticmethod
    def por_id(db:Session, id_): return _get_or_404(db, Rutina, id_)

    @staticmethod
    def filtrar(db:Session, usuario_id=None, fecha_inicio=None, fecha_fin=None, completada=None, solo_activos=True):
        qry = db.query(Rutina)
        if solo_activos: qry = qry.filter(Rutina.is_active==True)
        if usuario_id:   qry = qry.filter(Rutina.usuario_id==usuario_id)
        if fecha_inicio: qry = qry.filter(Rutina.fecha_programada>=fecha_inicio)
        if fecha_fin:    qry = qry.filter(Rutina.fecha_programada<=fecha_fin)
        if completada is not None: qry = qry.filter(Rutina.completada==completada)
        return qry.all()

    @staticmethod
    def actualizar(db:Session, id_, data:RutinaUpdate):
        r = _get_or_404(db, Rutina, id_)
        if not r.is_active: raise HTTPException(400, "Rutina inactiva.")
        cambios = data.model_dump(exclude_unset=True)
        if "fecha_programada" in cambios and cambios["fecha_programada"] < date.today():
            raise HTTPException(400, "Fecha no puede ser en el pasado.")
        for k,v in cambios.items(): setattr(r,k,v)
        db.commit(); db.refresh(r); return r

    @staticmethod
    def eliminar(db:Session, id_):
        r = _get_or_404(db, Rutina, id_)
        if not r.is_active: raise HTTPException(400, "Ya inactiva.")
        r.is_active = False; db.commit()
        return {"mensaje": f"Rutina id={id_} desactivada."}

# ── REGISTRO PROGRESO ─────────────────────────────────────────────────────────
class RegistroService:
    @staticmethod
    def crear(db:Session, data:RegistroProgresoCreate):
        if not db.query(Usuario).filter(Usuario.id==data.usuario_id, Usuario.is_active==True).first():
            raise HTTPException(404, f"Usuario id={data.usuario_id} no encontrado.")
        if db.query(RegistroProgreso).filter(RegistroProgreso.usuario_id==data.usuario_id, RegistroProgreso.fecha==data.fecha, RegistroProgreso.is_active==True).first():
            raise HTTPException(400, f"Ya existe registro para usuario {data.usuario_id} en {data.fecha}.")
        rp = RegistroProgreso(**data.model_dump()); db.add(rp); db.commit(); db.refresh(rp); return rp

    @staticmethod
    def listar(db:Session, solo_activos=True, skip=0, limit=100):
        qry = db.query(RegistroProgreso)
        if solo_activos: qry = qry.filter(RegistroProgreso.is_active==True)
        return qry.order_by(RegistroProgreso.fecha.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def por_id(db:Session, id_): return _get_or_404(db, RegistroProgreso, id_)

    @staticmethod
    def filtrar(db:Session, usuario_id=None, fecha_inicio=None, fecha_fin=None, solo_activos=True):
        qry = db.query(RegistroProgreso)
        if solo_activos: qry = qry.filter(RegistroProgreso.is_active==True)
        if usuario_id:   qry = qry.filter(RegistroProgreso.usuario_id==usuario_id)
        if fecha_inicio: qry = qry.filter(RegistroProgreso.fecha>=fecha_inicio)
        if fecha_fin:    qry = qry.filter(RegistroProgreso.fecha<=fecha_fin)
        return qry.order_by(RegistroProgreso.fecha.desc()).all()

    @staticmethod
    def buscar_fecha(db:Session, usuario_id, fecha):
        rp = db.query(RegistroProgreso).filter(RegistroProgreso.usuario_id==usuario_id, RegistroProgreso.fecha==fecha, RegistroProgreso.is_active==True).first()
        if not rp: raise HTTPException(404, f"Sin registro para usuario {usuario_id} en {fecha}.")
        return rp

    @staticmethod
    def actualizar(db:Session, id_, data:RegistroProgresoUpdate):
        rp = _get_or_404(db, RegistroProgreso, id_)
        if not rp.is_active: raise HTTPException(400, "Registro inactivo.")
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(rp,k,v)
        db.commit(); db.refresh(rp); return rp

    @staticmethod
    def eliminar(db:Session, id_):
        rp = _get_or_404(db, RegistroProgreso, id_)
        if not rp.is_active: raise HTTPException(400, "Ya inactivo.")
        rp.is_active = False; db.commit()
        return {"mensaje": f"Registro id={id_} desactivado."}

    @staticmethod
    def stats_usuario(db:Session, usuario_id):
        registros = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id==usuario_id, RegistroProgreso.is_active==True
        ).order_by(RegistroProgreso.fecha).all()
        return registros
