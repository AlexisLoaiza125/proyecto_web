"""
seed.py
Poblar la base de datos con datos simulados realistas.
Ejecutar UNA sola vez: python seed.py
Si ya tienes datos, comenta las secciones que no quieras repetir.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from database.connection import SessionLocal
from database import init_db
from models.usuario import Usuario
from models.ejercicio import Ejercicio
from models.rutina import Rutina
from models.registro_progreso import RegistroProgreso

init_db()
db = SessionLocal()

try:
    # ── USUARIOS ─────────────────────────────────────────────────────────────
    usuarios_data = [
        {
            "nombre": "Carlos Mendez",
            "email": "carlos@fitness.com",
            "username": "cmendez",
            "edad": 28,
            "peso_kg": 82.0,
            "altura_cm": 178.0,
            "objetivo": "ganar_musculo",
            "foto_perfil": "https://i.pravatar.cc/150?img=11",
        },
        {
            "nombre": "Laura Gomez",
            "email": "laura@fitness.com",
            "username": "lgomez",
            "edad": 25,
            "peso_kg": 63.0,
            "altura_cm": 165.0,
            "objetivo": "perder_peso",
            "foto_perfil": "https://i.pravatar.cc/150?img=5",
        },
        {
            "nombre": "Diego Rios",
            "email": "diego@fitness.com",
            "username": "drios",
            "edad": 35,
            "peso_kg": 90.0,
            "altura_cm": 182.0,
            "objetivo": "mantenimiento",
            "foto_perfil": "https://i.pravatar.cc/150?img=15",
        },
        {
            "nombre": "Ana Torres",
            "email": "ana@fitness.com",
            "username": "atorres",
            "edad": 30,
            "peso_kg": 58.0,
            "altura_cm": 162.0,
            "objetivo": "resistencia",
            "foto_perfil": "https://i.pravatar.cc/150?img=9",
        },
        {
            "nombre": "Juan Perez",
            "email": "juan@fitness.com",
            "username": "jperez",
            "edad": 22,
            "peso_kg": 70.0,
            "altura_cm": 175.0,
            "objetivo": "ganar_musculo",
            "foto_perfil": "https://i.pravatar.cc/150?img=3",
        },
    ]

    usuarios = []
    for data in usuarios_data:
        # Evitar duplicados si se corre el seed dos veces
        existente = db.query(Usuario).filter(Usuario.email == data["email"]).first()
        if existente:
            usuarios.append(existente)
            print(f"   ⚠️  Usuario '{data['username']}' ya existe, se omite.")
        else:
            u = Usuario(**data)
            db.add(u)
            db.flush()
            usuarios.append(u)

    db.flush()
    print(f"✅ Usuarios: {len(usuarios)}")

    # ── EJERCICIOS ────────────────────────────────────────────────────────────
    ejercicios_data = [
        {
            "nombre": "Press de Banca",
            "tipo": "fuerza",
            "grupo_muscular": "pecho",
            "nivel_dificultad": "intermedio",
            "descripcion": "Ejercicio básico de empuje para el desarrollo del pecho.",
            "instrucciones": "Acostado en el banco, bajar la barra al pecho de forma controlada y empujar hacia arriba.",
            "imagen_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400",
            "video_url": "https://www.youtube.com/watch?v=rT7DgCr-3pg",
        },
        {
            "nombre": "Sentadilla",
            "tipo": "fuerza",
            "grupo_muscular": "piernas",
            "nivel_dificultad": "intermedio",
            "descripcion": "El rey de los ejercicios para el tren inferior.",
            "instrucciones": "Con la barra en los trapecios, bajar hasta que los muslos queden paralelos al suelo.",
            "imagen_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=400",
            "video_url": "https://www.youtube.com/watch?v=ultWZbUMPL8",
        },
        {
            "nombre": "Peso Muerto",
            "tipo": "fuerza",
            "grupo_muscular": "espalda",
            "nivel_dificultad": "avanzado",
            "descripcion": "Ejercicio compuesto que trabaja toda la cadena posterior.",
            "instrucciones": "Con los pies al ancho de caderas, empujar el suelo con los talones y levantar la barra manteniendo la espalda recta.",
            "imagen_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400",
            "video_url": "https://www.youtube.com/watch?v=op9kVnSso6Q",
        },
        {
            "nombre": "Dominadas",
            "tipo": "fuerza",
            "grupo_muscular": "espalda",
            "nivel_dificultad": "avanzado",
            "descripcion": "Jalón con peso corporal para espalda y bíceps.",
            "instrucciones": "Colgado de la barra, jalar el cuerpo hacia arriba hasta que la barbilla supere la barra.",
            "imagen_url": "https://images.unsplash.com/photo-1598971639058-fab3c3109a00?w=400",
            "video_url": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
        },
        {
            "nombre": "Press Militar",
            "tipo": "fuerza",
            "grupo_muscular": "hombros",
            "nivel_dificultad": "intermedio",
            "descripcion": "Empuje vertical para el desarrollo de hombros.",
            "instrucciones": "De pie o sentado, empujar la barra desde los hombros hacia arriba hasta extender los brazos.",
            "imagen_url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400",
            "video_url": "https://www.youtube.com/watch?v=2yjwXTZQDDI",
        },
        {
            "nombre": "Curl de Bíceps",
            "tipo": "fuerza",
            "grupo_muscular": "biceps",
            "nivel_dificultad": "principiante",
            "descripcion": "Ejercicio de aislamiento para el desarrollo del bíceps.",
            "instrucciones": "Con mancuernas o barra, flexionar el codo llevando el peso hacia el hombro.",
            "imagen_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400",
            "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        },
        {
            "nombre": "Tríceps en Polea",
            "tipo": "fuerza",
            "grupo_muscular": "triceps",
            "nivel_dificultad": "principiante",
            "descripcion": "Extensión de codo para el tríceps usando polea alta.",
            "instrucciones": "Con cuerda o barra en polea alta, extender los codos hacia abajo manteniendo los codos pegados al cuerpo.",
            "imagen_url": "https://images.unsplash.com/photo-1590487988256-9ed24133863e?w=400",
            "video_url": "https://www.youtube.com/watch?v=vB5OHsJ3EME",
        },
        {
            "nombre": "Plancha",
            "tipo": "funcional",
            "grupo_muscular": "core",
            "nivel_dificultad": "principiante",
            "descripcion": "Isométrico para fortalecer el core y mejorar la estabilidad.",
            "instrucciones": "En posición de push-up, mantener el cuerpo recto apoyado en antebrazos y pies.",
            "imagen_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400",
            "video_url": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
        },
        {
            "nombre": "Correr en Cinta",
            "tipo": "cardio",
            "grupo_muscular": "cardio",
            "nivel_dificultad": "principiante",
            "descripcion": "Cardio de baja a media intensidad en cinta ergométrica.",
            "instrucciones": "Mantener ritmo constante entre 8-12 km/h según nivel de condición física.",
            "imagen_url": "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400",
            "video_url": "https://www.youtube.com/watch?v=_kGESn8ArrU",
        },
        {
            "nombre": "Burpees",
            "tipo": "hiit",
            "grupo_muscular": "full_body",
            "nivel_dificultad": "avanzado",
            "descripcion": "Ejercicio de alta intensidad que trabaja todo el cuerpo.",
            "instrucciones": "Desde de pie, bajar al suelo, hacer una lagartija, saltar los pies y terminar con un salto con brazos arriba.",
            "imagen_url": "https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400",
            "video_url": "https://www.youtube.com/watch?v=dZgVxmf6jkA",
        },
        {
            "nombre": "Estiramiento de Isquiotibiales",
            "tipo": "flexibilidad",
            "grupo_muscular": "piernas",
            "nivel_dificultad": "principiante",
            "descripcion": "Estiramiento estático para mejorar la flexibilidad posterior.",
            "instrucciones": "Sentado en el suelo, extender las piernas y alcanzar los pies manteniendo la espalda recta.",
            "imagen_url": "https://images.unsplash.com/photo-1566241440091-ec10de8db2e1?w=400",
            "video_url": "https://www.youtube.com/watch?v=Tb-gLMYfeKU",
        },
        {
            "nombre": "Hip Thrust",
            "tipo": "fuerza",
            "grupo_muscular": "gluteos",
            "nivel_dificultad": "intermedio",
            "descripcion": "Ejercicio principal para el desarrollo de glúteos.",
            "instrucciones": "Con la espalda alta apoyada en un banco y barra en caderas, empujar las caderas hacia arriba.",
            "imagen_url": "https://images.unsplash.com/photo-1607962837359-5e7e89f86776?w=400",
            "video_url": "https://www.youtube.com/watch?v=LM8XHLYJoYs",
        },
    ]

    ejercicios = []
    for data in ejercicios_data:
        existente = db.query(Ejercicio).filter(
            Ejercicio.nombre == data["nombre"],
            Ejercicio.tipo == data["tipo"]
        ).first()
        if existente:
            ejercicios.append(existente)
            print(f"   ⚠️  Ejercicio '{data['nombre']}' ya existe, se omite.")
        else:
            e = Ejercicio(**data)
            db.add(e)
            db.flush()
            ejercicios.append(e)

    db.flush()
    print(f"✅ Ejercicios: {len(ejercicios)}")

    # ── RUTINAS ───────────────────────────────────────────────────────────────
    hoy = date.today()

    rutinas_data = [
        # Carlos — ganar músculo
        {"nombre": "Pecho y Tríceps", "usuario_id": usuarios[0].id, "ejercicio_id": ejercicios[0].id,
         "series": 4, "repeticiones": 10, "peso_kg": 80.0, "fecha_programada": hoy + timedelta(days=1), "completada": False},
        {"nombre": "Espalda y Bíceps", "usuario_id": usuarios[0].id, "ejercicio_id": ejercicios[3].id,
         "series": 4, "repeticiones": 8, "peso_kg": 0.0, "fecha_programada": hoy + timedelta(days=2), "completada": False},
        {"nombre": "Piernas Fuerza", "usuario_id": usuarios[0].id, "ejercicio_id": ejercicios[1].id,
         "series": 5, "repeticiones": 6, "peso_kg": 100.0, "fecha_programada": hoy + timedelta(days=3), "completada": False},
        {"nombre": "Hombros", "usuario_id": usuarios[0].id, "ejercicio_id": ejercicios[4].id,
         "series": 4, "repeticiones": 10, "peso_kg": 50.0, "fecha_programada": hoy + timedelta(days=5), "completada": False},

        # Laura — perder peso
        {"nombre": "Cardio Mañana", "usuario_id": usuarios[1].id, "ejercicio_id": ejercicios[8].id,
         "duracion_min": 35, "fecha_programada": hoy + timedelta(days=1), "completada": False},
        {"nombre": "HIIT Intenso", "usuario_id": usuarios[1].id, "ejercicio_id": ejercicios[9].id,
         "series": 5, "repeticiones": 10, "fecha_programada": hoy + timedelta(days=3), "completada": False},
        {"nombre": "Glúteos y Core", "usuario_id": usuarios[1].id, "ejercicio_id": ejercicios[11].id,
         "series": 3, "repeticiones": 15, "peso_kg": 30.0, "fecha_programada": hoy + timedelta(days=4), "completada": False},

        # Diego — mantenimiento
        {"nombre": "Full Body", "usuario_id": usuarios[2].id, "ejercicio_id": ejercicios[2].id,
         "series": 3, "repeticiones": 8, "peso_kg": 120.0, "fecha_programada": hoy + timedelta(days=1), "completada": False},
        {"nombre": "Core Estabilidad", "usuario_id": usuarios[2].id, "ejercicio_id": ejercicios[7].id,
         "duracion_min": 20, "fecha_programada": hoy + timedelta(days=2), "completada": False},

        # Ana — resistencia
        {"nombre": "Cardio Largo", "usuario_id": usuarios[3].id, "ejercicio_id": ejercicios[8].id,
         "duracion_min": 60, "fecha_programada": hoy + timedelta(days=1), "completada": False},
        {"nombre": "Flexibilidad", "usuario_id": usuarios[3].id, "ejercicio_id": ejercicios[10].id,
         "duracion_min": 30, "fecha_programada": hoy + timedelta(days=2), "completada": False},

        # Juan — ganar músculo
        {"nombre": "Bíceps y Tríceps", "usuario_id": usuarios[4].id, "ejercicio_id": ejercicios[5].id,
         "series": 4, "repeticiones": 12, "peso_kg": 20.0, "fecha_programada": hoy + timedelta(days=1), "completada": False},
        {"nombre": "Pecho Volumen", "usuario_id": usuarios[4].id, "ejercicio_id": ejercicios[0].id,
         "series": 5, "repeticiones": 12, "peso_kg": 60.0, "fecha_programada": hoy + timedelta(days=3), "completada": False},
    ]

    rutinas_creadas = 0
    for data in rutinas_data:
        r = Rutina(**data)
        db.add(r)
        rutinas_creadas += 1

    db.flush()
    print(f"✅ Rutinas: {rutinas_creadas}")

    # ── REGISTROS DE PROGRESO ─────────────────────────────────────────────────
    # Historial de los últimos 14 días para Carlos y Laura
    registros_creados = 0

    # Carlos — subiendo de peso progresivamente
    carlos_pesos = [80.5, 80.8, 81.0, 81.2, 81.0, 81.5, 81.8, 82.0, 81.9, 82.2, 82.0, 82.3, 82.5, 82.0]
    for i, peso in enumerate(carlos_pesos):
        fecha = hoy - timedelta(days=13-i)
        existente = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id == usuarios[0].id,
            RegistroProgreso.fecha == fecha
        ).first()
        if not existente:
            rp = RegistroProgreso(
                usuario_id=usuarios[0].id,
                fecha=fecha,
                peso_kg=peso,
                calorias_consumidas=2800 + (i * 10),
                proteinas_g=180.0 + i,
                carbohidratos_g=320.0,
                grasas_g=70.0,
                nivel_energia=7 + (i % 3),
                notas="Entrenamiento intenso" if i % 3 == 0 else None,
            )
            db.add(rp)
            registros_creados += 1

    # Laura — bajando de peso progresivamente
    laura_pesos = [63.5, 63.3, 63.2, 63.0, 62.8, 63.0, 62.7, 62.5, 62.4, 62.3, 62.5, 62.2, 62.0, 62.1]
    for i, peso in enumerate(laura_pesos):
        fecha = hoy - timedelta(days=13-i)
        existente = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id == usuarios[1].id,
            RegistroProgreso.fecha == fecha
        ).first()
        if not existente:
            rp = RegistroProgreso(
                usuario_id=usuarios[1].id,
                fecha=fecha,
                peso_kg=peso,
                calorias_consumidas=1700 - (i * 5),
                proteinas_g=130.0,
                carbohidratos_g=180.0,
                grasas_g=55.0,
                nivel_energia=6 + (i % 4),
                notas="Día de descanso activo" if i % 4 == 0 else None,
            )
            db.add(rp)
            registros_creados += 1

    # Diego — mantenimiento (peso estable)
    for i in range(7):
        fecha = hoy - timedelta(days=6-i)
        existente = db.query(RegistroProgreso).filter(
            RegistroProgreso.usuario_id == usuarios[2].id,
            RegistroProgreso.fecha == fecha
        ).first()
        if not existente:
            rp = RegistroProgreso(
                usuario_id=usuarios[2].id,
                fecha=fecha,
                peso_kg=90.0 + (0.2 * (i % 3 - 1)),
                calorias_consumidas=2400,
                proteinas_g=160.0,
                carbohidratos_g=280.0,
                grasas_g=80.0,
                nivel_energia=8,
            )
            db.add(rp)
            registros_creados += 1

    db.commit()
    print(f"✅ Registros de progreso: {registros_creados}")

    print("\n" + "="*50)
    print("🎉 Seed completado exitosamente")
    print("="*50)
    print(f"   👤 Usuarios:            {db.query(Usuario).count()}")
    print(f"   🏋️  Ejercicios:          {db.query(Ejercicio).count()}")
    print(f"   📋 Rutinas:             {db.query(Rutina).count()}")
    print(f"   📊 Registros progreso:  {db.query(RegistroProgreso).count()}")
    print("\nUsuarios de prueba:")
    for u in db.query(Usuario).all():
        print(f"   • @{u.username} — {u.objetivo}")

except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    raise
finally:
    db.close()
