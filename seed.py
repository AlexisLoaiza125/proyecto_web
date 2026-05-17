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
    # ------- USUARIOS -------
    u1 = Usuario(
        nombre="Carlos Mendez",
        email="carlos@fitness.com",
        username="cmendez",
        edad=28,
        peso_kg=80.5,
        altura_cm=178.0,
        objetivo="ganar_musculo",
    )
    u2 = Usuario(
        nombre="Laura Gomez",
        email="laura@fitness.com",
        username="lgomez",
        edad=25,
        peso_kg=62.0,
        altura_cm=165.0,
        objetivo="perder_peso",
    )
    u3 = Usuario(
        nombre="Diego Rios",
        email="diego@fitness.com",
        username="drios",
        edad=35,
        peso_kg=90.0,
        altura_cm=182.0,
        objetivo="mantenimiento",
    )
    db.add_all([u1, u2, u3])
    db.flush()

    # ------- EJERCICIOS -------
    e1 = Ejercicio(
        nombre="Press de Banca",
        tipo="fuerza",
        grupo_muscular="pecho",
        nivel_dificultad="intermedio",
        descripcion="Ejercicio básico de empuje para pecho.",
        instrucciones="Acostado en banco, bajar la barra al pecho y empujar.",
    )
    e2 = Ejercicio(
        nombre="Sentadilla",
        tipo="fuerza",
        grupo_muscular="piernas",
        nivel_dificultad="intermedio",
        descripcion="El rey de los ejercicios para tren inferior.",
    )
    e3 = Ejercicio(
        nombre="Correr en cinta",
        tipo="cardio",
        grupo_muscular="cardio",
        nivel_dificultad="principiante",
        descripcion="Cardio moderado en cinta.",
    )
    e4 = Ejercicio(
        nombre="Dominadas",
        tipo="fuerza",
        grupo_muscular="espalda",
        nivel_dificultad="avanzado",
        descripcion="Jalón con peso corporal para espalda y bíceps.",
    )
    e5 = Ejercicio(
        nombre="Plancha",
        tipo="funcional",
        grupo_muscular="core",
        nivel_dificultad="principiante",
        descripcion="Isométrico para fortalecer el core.",
    )
    db.add_all([e1, e2, e3, e4, e5])
    db.flush()

    hoy = date.today()

    # ------- RUTINAS -------
    r1 = Rutina(
        nombre="Pecho Lunes",
        usuario_id=u1.id,
        ejercicio_id=e1.id,
        series=4,
        repeticiones=10,
        peso_kg=80.0,
        fecha_programada=hoy + timedelta(days=1),
    )
    r2 = Rutina(
        nombre="Piernas Martes",
        usuario_id=u1.id,
        ejercicio_id=e2.id,
        series=5,
        repeticiones=8,
        peso_kg=100.0,
        fecha_programada=hoy + timedelta(days=2),
    )
    r3 = Rutina(
        nombre="Cardio Ligero",
        usuario_id=u2.id,
        ejercicio_id=e3.id,
        duracion_min=30,
        fecha_programada=hoy + timedelta(days=1),
    )
    db.add_all([r1, r2, r3])
    db.flush()

    # ------- REGISTROS DE PROGRESO -------
    p1 = RegistroProgreso(
        usuario_id=u1.id,
        fecha=hoy - timedelta(days=7),
        peso_kg=81.0,
        calorias_consumidas=2800,
        proteinas_g=180.0,
        nivel_energia=8,
        notas="Buen día de entrenamiento",
    )
    p2 = RegistroProgreso(
        usuario_id=u1.id,
        fecha=hoy - timedelta(days=1),
        peso_kg=80.5,
        calorias_consumidas=2750,
        proteinas_g=185.0,
        nivel_energia=9,
    )
    p3 = RegistroProgreso(
        usuario_id=u2.id,
        fecha=hoy - timedelta(days=3),
        peso_kg=62.0,
        calorias_consumidas=1800,
        proteinas_g=130.0,
        nivel_energia=7,
    )
    db.add_all([p1, p2, p3])
    db.commit()

    print("✅  Datos de prueba insertados correctamente.")
    print(f"   Usuarios: {db.query(Usuario).count()}")
    print(f"   Ejercicios: {db.query(Ejercicio).count()}")
    print(f"   Rutinas: {db.query(Rutina).count()}")
    print(f"   Registros de progreso: {db.query(RegistroProgreso).count()}")

except Exception as e:
    db.rollback()
    print(f"❌  Error: {e}")
    raise
finally:
    db.close()
