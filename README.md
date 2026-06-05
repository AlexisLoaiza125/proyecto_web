## Proyecto integrador - Entrega final

Sistema backend completo para gestión de entrenamiento físico, desarrollado con **FastAPI + SQLAlchemy + Jinja2**. Incluye frontend web integrado, multimedia (URLs de imágenes y videos), dashboards con gráficas y despliegue en producción con Render + Supabase.

URL Publica: https://proyecto-web-v2py.onrender.com

QR:
<p align="center">
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/cb463fec-0199-44cc-9252-860b8bf9ecc7" />
</p>

##  Instalación local

```bash
# 1. Clonar e instalar
git clone https://github.com...
cd fitness_api
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Variables de entorno
# Editar .env con DATABASE_URL, SUPABASE_URL, SUPABASE_KEY de Supabase

# 3. Iniciar
uvicorn main:app --reload --port 8000
```

Abrir: `http://127.0.0.1:8000`

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


## Diagrma de secuencia para mostrar usuarios 
<img width="2212" height="1046" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/7b89d065-3206-4d84-858f-89cadfc4e815" />
hecho en https://mermaid.live/

El navegador solicita /usuarios, FastAPI delega la consulta al servicio, el servicio obtiene los datos desde PostgreSQL mediante SQLAlchemy y finalmente FastAPI genera la página usuarios.html para mostrarla al usuario.

## Diagrama de despliegue
<img width="2734" height="817" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/1de18785-b311-45bd-be61-6c5b9a7c7566" />
hecho en https://mermaid.live/

el usuario accede a una aplicación FastAPI desplegada en Render, que genera páginas con Jinja2 y consulta una base de datos PostgreSQL alojada en Supabase mediante un pool de conexiones seguro.


## Tabla de reglas de negocio
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
| Cualquier dato que requiera estar en un intervalo determinado                     | Validación de rango            | `422 Unprocessable Entity` |
| Nombre del usuario no debe tener numeros o caracteres especiales                     | Validación          | `422 Unprocessable Entity` |
| Las eliminaciones son lógicas mediante `is_active=False`.         | Soft Delete                    | `200 OK`                   |
| SQLAlchemy falla.         | Inertal server error                   | `500 internal server error`                   |


## Mapa de endpoints
Frontend (Vistas HTML)
| Método | Ruta               | Funcionalidad                                               |
| ------ | ------------------ | ----------------------------------------------------------- |
| GET    | `/`                | Dashboard con estadísticas generales y gráficas de progreso |
| GET    | `/usuarios`        | Gestión y consulta de usuarios con filtros                  |
| GET    | `/usuarios/{id}`   | Detalle de usuario, foto, rutinas y progreso                |
| GET    | `/ejercicios`      | Catálogo de ejercicios con contenido multimedia             |
| GET    | `/ejercicios/{id}` | Detalle de ejercicio con imagen y video                     |
| GET    | `/rutinas`         | Gestión de rutinas y filtros por usuario/fecha              |
| GET    | `/progreso`        | Historial y gráficas de evolución física                    |
| POST    | `/api/usuarios/{usuario_id}/foto`        | cargar foto de perfil del usuario               |
| POST   | `/api/ejericios/{ejercicio_id}/imagen`        | cargar imagen del ejercicio                |

API REST

Usuarios
| Método | Endpoint                            | Acción                 | HTTP |
| ------ | ----------------------------------- | ---------------------- | ---- |
| GET    | `/api/usuarios/`                    | Listar usuarios        | 200  |
| GET    | `/api/usuarios/filtrar/`            | Filtrar por objetivo   | 200  |
| GET    | `/api/usuarios/username/{username}` | Buscar por username    | 200  |
| GET    | `/api/usuarios/{id}`                | Obtener usuario por ID | 200  |
| POST   | `/api/usuarios/`                    | Crear usuario          | 201  |
| PUT    | `/api/usuarios/{id}`                | Actualizar usuario     | 200  |
| DELETE | `/api/usuarios/{id}`                | Eliminación lógica     | 200  |

Ejercicios
| Método | Endpoint                   | Acción                                   | HTTP |
| ------ | -------------------------- | ---------------------------------------- | ---- |
| GET    | `/api/ejercicios/`         | Listar ejercicios                        | 200  |
| GET    | `/api/ejercicios/filtrar/` | Filtrar por tipo, grupo muscular o nivel | 200  |
| GET    | `/api/ejercicios/buscar/`  | Búsqueda parcial por nombre              | 200  |
| GET    | `/api/ejercicios/{id}`     | Obtener ejercicio por ID                 | 200  |
| POST   | `/api/ejercicios/`         | Crear ejercicio con multimedia           | 201  |
| PUT    | `/api/ejercicios/{id}`     | Actualizar ejercicio                     | 200  |
| DELETE | `/api/ejercicios/{id}`     | Eliminación lógica                       | 200  |

Rutinas
| Método | Endpoint                | Acción                              | HTTP |
| ------ | ----------------------- | ----------------------------------- | ---- |
| GET    | `/api/rutinas/`         | Listar rutinas                      | 200  |
| GET    | `/api/rutinas/filtrar/` | Filtrar por usuario, fecha o estado | 200  |
| POST   | `/api/rutinas/`         | Crear rutina                        | 201  |
| PUT    | `/api/rutinas/{id}`     | Actualizar o completar rutina       | 200  |
| DELETE | `/api/rutinas/{id}`     | Eliminación lógica                  | 200  |

Registros de Progreso
| Método | Endpoint                  | Acción                                | HTTP |
| ------ | ------------------------- | ------------------------------------- | ---- |
| GET    | `/api/registros/`         | Listar registros                      | 200  |
| GET    | `/api/registros/filtrar/` | Filtrar por usuario o rango de fechas | 200  |
| GET    | `/api/registros/buscar/`  | Buscar por usuario y fecha exacta     | 200  |
| POST   | `/api/registros/`         | Crear registro de progreso            | 201  |
| PUT    | `/api/registros/{id}`     | Actualizar registro                   | 200  |
| DELETE | `/api/registros/{id}`     | Eliminación lógica                    | 200  |


## Variables de entorno para Render

| Variable        | Valor                                                                  |
|-----------------|------------------------------------------------------------------------|
| `DATABASE_URL`  | `postgresql://postgres.[ref]:[pass]@pooler.supabase.com:6543/postgres` |
| `SUPABASE_URL`  | `https://[ref].supabase.co`                                            |
| `SUPABASE_KEY`  | `[SUPABASE_ANON_KEY]`                               |


## Storage en Supabase
<img width="1132" height="634" alt="image" src="https://github.com/user-attachments/assets/a6aeb611-b8b1-44ba-90c5-ac5e2af770cf" />

## Tablas en Supabase 
<img width="1548" height="572" alt="image" src="https://github.com/user-attachments/assets/4634b168-d8e0-4c45-95e7-5a576b3a0186" />

## imagenes de evidencia

<p align="center">

<img width="1893" height="925" alt="image" src="https://github.com/user-attachments/assets/5098ae26-3b8d-482d-886d-8f17a8f9b812" />

<img width="1276" height="358" alt="image" src="https://github.com/user-attachments/assets/9befed86-cac0-488e-a2bc-0ca4537df7b6" />

<img width="595" height="536" alt="image" src="https://github.com/user-attachments/assets/a3ec5919-c576-4346-9024-1fbb4356dfcb" />

<img width="1262" height="860" alt="image" src="https://github.com/user-attachments/assets/2d13f852-2e69-44aa-8b89-d50585900cc2" />

<img width="602" height="778" alt="image" src="https://github.com/user-attachments/assets/22de1308-68ad-495c-821c-c519f9eccde7" />

<img width="1263" height="755" alt="image" src="https://github.com/user-attachments/assets/fc61062b-18f5-41ca-80fc-e78507da2ac1" />

<img width="1257" height="878" alt="image" src="https://github.com/user-attachments/assets/b00ce695-1f03-4b71-8ad9-3a0ef311a90e" />
</p>




## info
Nombre: Johan Alexis Loaiza Culma

Codigo estudiantil: 67001155

Institucion: Universidad catolica de colombia

Fehca de presentacion: Mayo 2026

Tutor: Sergio Iván Galvis Motoa 

Materia: Ingenieria web 

