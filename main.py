"""
main.py — Punto de entrada de Fitness API
Sirve tanto HTML (Jinja2) como JSON (API REST bajo /api/)
"""
import os
import json
from datetime import date, datetime
from typing import Optional
from collections import Counter

from fastapi import FastAPI, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import init_db
from database.connection import get_db
from models.usuario import Usuario
from models.ejercicio import Ejercicio
from models.rutina import Rutina
from models.registro_progreso import RegistroProgreso
from schemas import (UsuarioCreate, UsuarioUpdate, EjercicioCreate, EjercicioUpdate,
                     RutinaCreate, RutinaUpdate, RegistroProgresoCreate, RegistroProgresoUpdate)
from services import UsuarioService, EjercicioService, RutinaService, RegistroService
from middleware.exception_handlers import validation_handler, sqlalchemy_handler, generic_handler

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="🏋️ Fitness API",
    description="API REST + Frontend web para gestión de entrenamiento fitness",
    version="2.0.0",
)

# Static files
os.makedirs("static/uploads/usuarios", exist_ok=True)
os.makedirs("static/uploads/ejercicios", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
def sqlalchemy_to_json(obj):
    if hasattr(obj, "__dict__"):
        data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        return json.dumps(data, default=str)
    return json.dumps(obj, default=str)

templates.env.filters["tojson"] = sqlalchemy_to_json


# Exception handlers
app.add_exception_handler(RequestValidationError, validation_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_handler)
app.add_exception_handler(Exception, generic_handler)

@app.on_event("startup")
def startup(): init_db()

# ════════════════════════════════════════════════════════════════════════════
#  HTML ROUTES  (devuelven páginas renderizadas)
# ════════════════════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = {
        "usuarios":  db.query(Usuario).filter(Usuario.is_active==True).count(),
        "ejercicios":db.query(Ejercicio).filter(Ejercicio.is_active==True).count(),
        "rutinas":   db.query(Rutina).filter(Rutina.is_active==True).count(),
        "registros": db.query(RegistroProgreso).filter(RegistroProgreso.is_active==True).count(),
    }
    ejercicios = db.query(Ejercicio).filter(Ejercicio.is_active==True).all()
    chart_tipos = dict(Counter(e.tipo for e in ejercicios))
    usuarios = db.query(Usuario).filter(Usuario.is_active==True).all()
    chart_objetivos = dict(Counter(u.objetivo for u in usuarios if u.objetivo))
    ultimos_usuarios = db.query(Usuario).filter(Usuario.is_active==True).order_by(Usuario.created_at.desc()).limit(5).all()
    rutinas_pendientes = db.query(Rutina).filter(Rutina.is_active==True, Rutina.completada==False).order_by(Rutina.fecha_programada).limit(5).all()
    return templates.TemplateResponse("index.html", {
        "request": request, "active": "dashboard",
        "stats": stats, "chart_tipos": chart_tipos, "chart_objetivos": chart_objetivos,
        "ultimos_usuarios": ultimos_usuarios, "rutinas_pendientes": rutinas_pendientes,
    })

@app.get("/usuarios", response_class=HTMLResponse)
def view_usuarios(
    request: Request, db: Session = Depends(get_db),
    q: Optional[str] = None, objetivo: Optional[str] = None,
    solo_activos: int = 1,
):
    activos = solo_activos == 1
    usuarios = UsuarioService.listar(db, solo_activos=activos, q=q)
    if objetivo: usuarios = [u for u in usuarios if u.objetivo == objetivo]
    return templates.TemplateResponse("usuarios.html", {
        "request": request, "active": "usuarios",
        "usuarios": usuarios, "q": q, "objetivo": objetivo, "solo_activos": activos,
    })

@app.get("/usuarios/{usuario_id}", response_class=HTMLResponse)
def view_usuario_detalle(request: Request, usuario_id: int, db: Session = Depends(get_db)):
    u = UsuarioService.por_id(db, usuario_id)
    rutinas = db.query(Rutina).filter(Rutina.usuario_id==usuario_id, Rutina.is_active==True).all()
    registros = db.query(RegistroProgreso).filter(RegistroProgreso.usuario_id==usuario_id, RegistroProgreso.is_active==True).order_by(RegistroProgreso.fecha.desc()).limit(10).all()
    return templates.TemplateResponse("usuario_detalle.html", {
        "request": request, "active": "usuarios", "usuario": u,
        "rutinas": rutinas, "registros": registros,
    })

@app.get("/ejercicios", response_class=HTMLResponse)
def view_ejercicios(
    request: Request, db: Session = Depends(get_db),
    q: Optional[str] = None, tipo: Optional[str] = None,
    nivel: Optional[str] = None, grupo: Optional[str] = None,
):
    ejercicios = EjercicioService.filtrar(db, tipo=tipo, grupo=grupo, nivel=nivel)
    if q: ejercicios = [e for e in ejercicios if q.lower() in e.nombre.lower()]
    return templates.TemplateResponse("ejercicios.html", {
        "request": request, "active": "ejercicios",
        "ejercicios": ejercicios, "q": q, "tipo": tipo, "nivel": nivel, "grupo": grupo,
    })

@app.get("/ejercicios/{ejercicio_id}", response_class=HTMLResponse)
def view_ejercicio_detalle(request: Request, ejercicio_id: int, db: Session = Depends(get_db)):
    e = EjercicioService.por_id(db, ejercicio_id)
    rutinas = db.query(Rutina).filter(Rutina.ejercicio_id==ejercicio_id, Rutina.is_active==True).count()
    return templates.TemplateResponse("ejercicio_detalle.html", {
        "request": request, "active": "ejercicios", "ejercicio": e, "total_rutinas": rutinas,
    })

@app.get("/rutinas", response_class=HTMLResponse)
def view_rutinas(
    request: Request, db: Session = Depends(get_db),
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None, fecha_fin: Optional[date] = None,
    completada: Optional[str] = None,
):
    comp = None
    if completada == "1": comp = True
    elif completada == "0": comp = False
    rutinas = RutinaService.filtrar(db, usuario_id=usuario_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, completada=comp)
    return templates.TemplateResponse("rutinas.html", {
        "request": request, "active": "rutinas",
        "rutinas": rutinas, "usuario_id": usuario_id,
        "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "completada": completada,
    })

@app.get("/progreso", response_class=HTMLResponse)
def view_progreso(
    request: Request, db: Session = Depends(get_db),
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None, fecha_fin: Optional[date] = None,
):
    registros = RegistroService.filtrar(db, usuario_id=usuario_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    chart_data = None
    if usuario_id:
        rps = RegistroService.stats_usuario(db, usuario_id)
        chart_data = [{"fecha": str(r.fecha), "peso_kg": r.peso_kg} for r in rps if r.peso_kg]
    return templates.TemplateResponse("progreso.html", {
        "request": request, "active": "progreso",
        "registros": registros, "usuario_id": usuario_id,
        "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin,
        "chart_data": chart_data,
    })

# ════════════════════════════════════════════════════════════════════════════
#  JSON API ROUTES  (bajo /api/ — usados por el JS del frontend)
# ════════════════════════════════════════════════════════════════════════════

# ── Usuarios ──
@app.get("/api/usuarios/")
def api_listar_usuarios(q: Optional[str]=None, solo_activos: bool=True, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return UsuarioService.listar(db, solo_activos=solo_activos, skip=skip, limit=limit, q=q)

@app.get("/api/usuarios/filtrar/")
def api_filtrar_usuarios(objetivo: Optional[str]=None, solo_activos: bool=True, db: Session=Depends(get_db)):
    return UsuarioService.filtrar(db, objetivo=objetivo, solo_activos=solo_activos)

@app.get("/api/usuarios/username/{username}")
def api_usuario_username(username: str, db: Session=Depends(get_db)):
    return UsuarioService.por_username(db, username)

@app.get("/api/usuarios/{usuario_id}")
def api_usuario(usuario_id: int, db: Session=Depends(get_db)):
    return UsuarioService.por_id(db, usuario_id)

@app.post("/api/usuarios/", status_code=201)
def api_crear_usuario(data: UsuarioCreate, db: Session=Depends(get_db)):
    return UsuarioService.crear(db, data)

@app.put("/api/usuarios/{usuario_id}")
def api_actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session=Depends(get_db)):
    return UsuarioService.actualizar(db, usuario_id, data)

@app.delete("/api/usuarios/{usuario_id}")
def api_eliminar_usuario(usuario_id: int, db: Session=Depends(get_db)):
    return UsuarioService.eliminar(db, usuario_id)

# ── Ejercicios ──
@app.get("/api/ejercicios/")
def api_listar_ejercicios(q: Optional[str]=None, solo_activos: bool=True, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return EjercicioService.listar(db, solo_activos=solo_activos, skip=skip, limit=limit, q=q)

@app.get("/api/ejercicios/filtrar/")
def api_filtrar_ejercicios(tipo: Optional[str]=None, grupo_muscular: Optional[str]=None, nivel_dificultad: Optional[str]=None, solo_activos: bool=True, db: Session=Depends(get_db)):
    return EjercicioService.filtrar(db, tipo=tipo, grupo=grupo_muscular, nivel=nivel_dificultad, solo_activos=solo_activos)

@app.get("/api/ejercicios/buscar/")
def api_buscar_ejercicio(nombre: str = Query(..., min_length=2), db: Session=Depends(get_db)):
    return EjercicioService.buscar_nombre(db, nombre)

@app.get("/api/ejercicios/{ejercicio_id}")
def api_ejercicio(ejercicio_id: int, db: Session=Depends(get_db)):
    return EjercicioService.por_id(db, ejercicio_id)

@app.post("/api/ejercicios/", status_code=201)
def api_crear_ejercicio(data: EjercicioCreate, db: Session=Depends(get_db)):
    return EjercicioService.crear(db, data)

@app.put("/api/ejercicios/{ejercicio_id}")
def api_actualizar_ejercicio(ejercicio_id: int, data: EjercicioUpdate, db: Session=Depends(get_db)):
    return EjercicioService.actualizar(db, ejercicio_id, data)

@app.delete("/api/ejercicios/{ejercicio_id}")
def api_eliminar_ejercicio(ejercicio_id: int, db: Session=Depends(get_db)):
    return EjercicioService.eliminar(db, ejercicio_id)

# ── Rutinas ──
@app.get("/api/rutinas/")
def api_listar_rutinas(solo_activos: bool=True, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return RutinaService.listar(db, solo_activos=solo_activos, skip=skip, limit=limit)

@app.get("/api/rutinas/filtrar/")
def api_filtrar_rutinas(usuario_id: Optional[int]=None, fecha_inicio: Optional[date]=None, fecha_fin: Optional[date]=None, completada: Optional[bool]=None, solo_activos: bool=True, db: Session=Depends(get_db)):
    return RutinaService.filtrar(db, usuario_id=usuario_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, completada=completada, solo_activos=solo_activos)

@app.get("/api/rutinas/{rutina_id}")
def api_rutina(rutina_id: int, db: Session=Depends(get_db)):
    return RutinaService.por_id(db, rutina_id)

@app.post("/api/rutinas/", status_code=201)
def api_crear_rutina(data: RutinaCreate, db: Session=Depends(get_db)):
    return RutinaService.crear(db, data)

@app.put("/api/rutinas/{rutina_id}")
def api_actualizar_rutina(rutina_id: int, data: RutinaUpdate, db: Session=Depends(get_db)):
    return RutinaService.actualizar(db, rutina_id, data)

@app.delete("/api/rutinas/{rutina_id}")
def api_eliminar_rutina(rutina_id: int, db: Session=Depends(get_db)):
    return RutinaService.eliminar(db, rutina_id)

# ── Registros ──
@app.get("/api/registros/")
def api_listar_registros(solo_activos: bool=True, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return RegistroService.listar(db, solo_activos=solo_activos, skip=skip, limit=limit)

@app.get("/api/registros/filtrar/")
def api_filtrar_registros(usuario_id: Optional[int]=None, fecha_inicio: Optional[date]=None, fecha_fin: Optional[date]=None, solo_activos: bool=True, db: Session=Depends(get_db)):
    return RegistroService.filtrar(db, usuario_id=usuario_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, solo_activos=solo_activos)

@app.get("/api/registros/buscar/")
def api_buscar_registro(usuario_id: int, fecha: date, db: Session=Depends(get_db)):
    return RegistroService.buscar_fecha(db, usuario_id, fecha)

@app.get("/api/registros/{registro_id}")
def api_registro(registro_id: int, db: Session=Depends(get_db)):
    return RegistroService.por_id(db, registro_id)

@app.post("/api/registros/", status_code=201)
def api_crear_registro(data: RegistroProgresoCreate, db: Session=Depends(get_db)):
    return RegistroService.crear(db, data)

@app.put("/api/registros/{registro_id}")
def api_actualizar_registro(registro_id: int, data: RegistroProgresoUpdate, db: Session=Depends(get_db)):
    return RegistroService.actualizar(db, registro_id, data)

@app.delete("/api/registros/{registro_id}")
def api_eliminar_registro(registro_id: int, db: Session=Depends(get_db)):
    return RegistroService.eliminar(db, registro_id)

# ── Root / health ──
@app.get("/api/")
def api_root(): return {"mensaje": "🏋️ Fitness API v2.0 OK", "docs": "/docs"}
