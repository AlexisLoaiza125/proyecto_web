#Fitness API v2.0

Sistema backend completo para gestión de entrenamiento físico, desarrollado con **FastAPI + SQLAlchemy + Jinja2**. Incluye frontend web integrado, multimedia (URLs de imágenes y videos), dashboards con gráficas y despliegue en producción con Render + Supabase.

## 📁 Estructura del proyecto
```
fitness_api/
├── main.py                    # Entrada de las rutas HTML (/), API REST (/api/)
├── requirements.txt
├── .python-version            # Fija Python 3.11.9 para Render
├── .env                       # DATABASE_URL, SUPABASE_KEY, SUPABASE_URL para storage en supabase (.gitignore)
│
├── database/
│   ├──connection.py          # Engine, SessionLocal, Base, get_db()
│   ├──__init__.py            # init_db() — create_all()
│   └── storage.py            # Para subida de imagenes de manera local
|
├── models/                    # SQLAlchemy ORM
│   ├── usuario.py             # con foto_perfil (multimedia)
│   ├── ejercicio.py           # con imagen_url, video_url (multimedia)
│   ├── rutina.py
│   └── registro_progreso.py
│
├── schemas/
│   └── __init__.py            # Pydantic: Create / Update / Response por modelo con sus respectivas validaciones pydantic
│
├── services/
│   └── __init__.py            # Lógica de negocio + reglas + CRUD
│
├── middleware/
│   └── exception_handlers.py  # Handlers globales 422 / 500
│
├── templates/                 # Jinja2
│   ├── base.html              # Navbar global, búsqueda, estilos, toast
│   ├── index.html             # Dashboard con Chart.js
│   ├── usuarios.html          # Lista, modal crear, modal editar
│   ├── usuario_detalle.html   # Perfil con foto, rutinas y registros
│   ├── ejercicios.html        # Cards multimedia con imagen + video
│   ├── ejercicio_detalle.html # Detalle con imagen grande y botón video
│   ├── rutinas.html           # Lista con filtros mas modal crear
│   └── progreso.html          # Tabla mas gráfica de peso Chart.js
│
└── static/
|    ├── default-avatar.svg
|    └── uploads/
|        ├── usuarios/
|       └── ejercicios/
└── seed.py                    #(minidataset) Datos de prueba
```
## Diagrama de clases 
<img width="676" height="791" alt="image" src="https://github.com/user-attachments/assets/d9b68aea-16af-4121-aa3e-a905339d65e2" />
## Diagrma de secuencia 
Navegador → main.py → Service → Model → Supabase BD
    │           │         │        │         │
    │  GET /usuarios       │        │         │
    │──────────►│          │        │         │
    │           │ listar() │        │         │
    │           │─────────►│        │         │
    │           │          │ query()│         │
    │           │          │───────►│         │
    │           │          │        │ SELECT  │
    │           │          │        │────────►│
    │           │          │        │◄────────│
    │           │          │◄───────│         │
    │           │◄─────────│        │         │
    │◄──────────│          │        │         │
  HTML renderizado
