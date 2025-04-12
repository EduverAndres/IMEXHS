from sqlalchemy import create_engine, MetaData  # create_engine: para conectar con la base de datos.
from sqlalchemy.orm import declarative_base, sessionmaker  # Herramientas esenciales para manejar modelos y sesiones.

# Definimos la URL de nuestra base de datos PostgreSQL.
# Formato: `postgresql://usuario:contraseña@host:puerto/base_de_datos`
DATABASE_URL = "postgresql://postgres:1085@localhost:5432/medical_images"

# Creamos el motor de conexión usando SQLAlchemy.
engine = create_engine(DATABASE_URL)

# Configuramos SessionLocal, que será responsable de manejar las interacciones con la base de datos.
# autocommit=False: Las transacciones no se confirman automáticamente. Esto nos da control total.
# autoflush=False: Evita el envío automático de cambios al motor hasta que llamemos explícitamente a commit().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaramos una clase base para los modelos de la base de datos.
# Todos los modelos que definamos heredarán de `Base`.
Base = declarative_base()

# Inicializamos `MetaData`, que es como el "catálogo" de esquemas de nuestra base de datos.
metadata = MetaData()
