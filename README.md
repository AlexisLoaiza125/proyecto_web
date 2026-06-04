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

hecho en [https://lucid.com](https://lucid.app/)


## Diagrma de secuencia 
<img width="2212" height="1046" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/7b89d065-3206-4d84-858f-89cadfc4e815" />
hecho en https://mermaid.live/

## Tabla de reglas de negocio
## Reglas de Negocio

El sistema implementa las siguientes reglas de negocio para garantizar la integridad y consistencia de los datos:

| Regla de negocio                                                  | Tipo de validación             | Código HTTP                |
| ----------------------------------------------------------------- | ------------------------------ | -------------------------- |
| Un email no puede repetirse entre usuarios activos.               | Verificación de unicidad       | `400 Bad Request`          |
| Un username no puede repetirse entre usuarios activos.            | Verificación de unicidad       | `400 Bad Request`          |
| No se puede eliminar un usuario con rutinas activas.              | Integridad de negocio          | `409 Conflict`             |
| No se puede duplicar un ejercicio con el mismo nombre y tipo.     | Verificación de unicidad       | `400 Bad Request`          |
| No se puede eliminar un ejercicio asociado a rutinas activas.     | Integridad referencial         | `409 Conflict`             |
| La fecha de una rutina no puede estar en el pasado.               | Validación temporal            | `400 Bad Request`          |
| Solo usuarios y ejercicios activos pueden asociarse a una rutina. | Validación de estado           | `404 Not Found`            |
| Un usuario solo puede tener un registro de progreso por día.      | Restricción de unicidad lógica | `400 Bad Request`          |
| El nivel de energía debe estar entre 1 y 10.                      | Validación de rango            | `422 Unprocessable Entity` |
| Las eliminaciones son lógicas mediante `is_active=False`.         | Soft Delete                    | `200 OK`                   |


