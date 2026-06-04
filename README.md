#Fitness API v2.0

Sistema backend completo para gestión de entrenamiento físico, desarrollado con **FastAPI + SQLAlchemy + Jinja2**. Incluye frontend web integrado, multimedia (URLs de imágenes y videos), dashboards con gráficas y despliegue en producción con Render + Supabase.

## 📁 Estructura del proyecto
```
fitness_api/
├── main.py                    # Entrada: rutas HTML (/), API REST (/api/), static files
├── requirements.txt
├── .python-version            # Fija Python 3.11.9 para Render
├── .env                       # DATABASE_URL (no subir a git)
│
├── database/
│   ├── connection.py          # Engine, SessionLocal, Base, get_db()
│   └── __init__.py            # init_db() — create_all()
│
├── models/                    # SQLAlchemy ORM
│   ├── usuario.py             # + foto_perfil (multimedia)
│   ├── ejercicio.py           # + imagen_url, video_url (multimedia)
│   ├── rutina.py
│   └── registro_progreso.py
│
├── schemas/
│   └── __init__.py            # Pydantic: Create / Update / Response por modelo
│
├── services/
│   └── __init__.py            # Lógica de negocio + reglas + CRUD
│
├── middleware/
│   └── exception_handlers.py  # Handlers globales 422 / 500
│
├── templates/                 # Jinja2
│   ├── base.html              # Navbar global + búsqueda + estilos + toast
│   ├── index.html             # Dashboard con Chart.js
│   ├── usuarios.html          # Lista + modal crear + modal editar
│   ├── usuario_detalle.html   # Perfil con foto, rutinas y registros
│   ├── ejercicios.html        # Cards multimedia con imagen + video
│   ├── ejercicio_detalle.html # Detalle con imagen grande y botón video
│   ├── rutinas.html           # Lista con filtros + modal crear
│   └── progreso.html          # Tabla + gráfica de peso Chart.js
│
└── static/
    ├── default-avatar.svg
    └── uploads/
        ├── usuarios/
        └── ejercicios/
```
