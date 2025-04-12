import logging  # Para registrar solicitudes, respuestas y cualquier actividad relevante
from fastapi import FastAPI  # Framework para crear la API RESTful
from .database import Base, engine  # Base (modelos) y engine (conexión a la base de datos)
from .routers import elements  # Importamos las rutas de los endpoints desde `routers/elements.py`
import os  # Para trabajar con rutas y directorios

# Asegurar que exista la carpeta para guardar los logs
os.makedirs("logs", exist_ok=True)

# Configuración básica del logger
logging.basicConfig(
    filename="logs/api.log",  # Archivo donde se guardarán los logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato detallado: incluye fecha, nivel, y mensaje
    level=logging.INFO  # Registramos eventos de nivel INFO o superior
)

# Crear tablas en la base de datos si aún no existen
# Esto toma los modelos definidos con SQLAlchemy y asegura que sus tablas sean creadas
Base.metadata.create_all(bind=engine)

# Instanciamos la aplicación FastAPI
app = FastAPI()

# Middleware para registrar cada solicitud que llegue a la API y su correspondiente respuesta
@app.middleware("http")
async def log_requests(request, call_next):
    """
    Middleware que registra cada solicitud y respuesta HTTP.
    - Captura el método (GET, POST, etc.) y la URL de la solicitud.
    - También registra el código de estado (200, 404, 500, etc.) de la respuesta.
    """
    logging.info(f"Solicitud: {request.method} {request.url}")  # Log de la solicitud entrante
    response = await call_next(request)  # Procesamos la solicitud y obtenemos la respuesta
    logging.info(f"Respuesta: {response.status_code}")  # Log del código de estado de la respuesta
    return response

# Registrar los endpoints (routers) en la aplicación principal
# `prefix` es el prefijo que tendrán todas las rutas registradas aquí. Ejemplo: "/api/elements/"
# `tags` es solo para organizar y categorizar en la documentación automática que genera FastAPI.
app.include_router(elements.router, prefix="/api", tags=["elements"])
