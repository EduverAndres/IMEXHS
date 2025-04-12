# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# 1. Crea la base de datos llamada "medical_images"
psql -U postgres -c "CREATE DATABASE medical_images;"

# 2. Conéctate a la base de datos recién creada
psql -U postgres -d medical_images

# 3. Crear tabla para almacenar dispositivos médicos
psql -U postgres -d medical_images -c "
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,             -- Identificador único para cada dispositivo
    device_name VARCHAR(255) NOT NULL  -- Nombre descriptivo del dispositivo
);
"

# 4. Crear tabla para almacenar resultados del procesamiento de imágenes
psql -U postgres -d medical_images -c "
CREATE TABLE processing_results (
    id SERIAL PRIMARY KEY,                      -- Identificador único para cada resultado
    device_id INT NOT NULL,                     -- Relación con la tabla devices
    average_before_normalization FLOAT NOT NULL,-- Promedio antes de la normalización
    average_after_normalization FLOAT NOT NULL, -- Promedio después de la normalización
    data_size INT NOT NULL,                     -- Cantidad de datos procesados
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Marca de tiempo de creación
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Marca de tiempo de última actualización
    FOREIGN KEY (device_id) REFERENCES devices (id)   -- Clave foránea
);
"

# --- CONFIGURACIÓN DEL ENTORNO ---
# 5. Crear un entorno virtual
python -m venv env

# 6. Activar el entorno virtual (en Windows)
.\env\Scripts\activate

# --- INSTALACIÓN DE DEPENDENCIAS ---
# 7. Instalar las librerías necesarias
pip install fastapi         # Framework para la API RESTful
pip install uvicorn         # Servidor ASGI para ejecutar la API
pip install sqlalchemy      # ORM para manejar la base de datos
pip install pydantic        # Validación de datos para los schemas
pip install psycopg2-binary # Driver PostgreSQL
pip install numpy           # Librería para cálculos numéricos (normalización)

# --- ARCHIVO REQUIREMENTS.TXT ---
# 8. Crear un archivo para registrar las dependencias
pip freeze > requirements.txt

# --- LEVANTAR EL SERVIDOR ---
# 9. Iniciar el servidor FastAPI con Uvicorn
.\env\Scripts\activate
uvicorn app.main:app --reload
deactivate
