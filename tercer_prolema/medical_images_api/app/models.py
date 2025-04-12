# Importamos los módulos necesarios desde SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base  # Importamos la clase Base que conecta con nuestra base de datos

# Modelo para los dispositivos médicos
class Device(Base):  
    __tablename__ = "devices"  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, index=True)  
    # id: Clave primaria de tipo entero, única para cada dispositivo. `index=True` para optimizar búsquedas.
    
    device_name = Column(String, nullable=False)  
    # Nombre del dispositivo. Obligatorio (`nullable=False`).

    # Relación uno-a-muchos con la tabla "processing_results"
    results = relationship("ProcessingResult", back_populates="device")  
    # `relationship` crea un vínculo lógico entre esta tabla (Device) y ProcessingResult.
    # Es decir, un dispositivo puede tener múltiples resultados asociados.

# Modelo para los resultados del procesamiento
class ProcessingResult(Base):  
    __tablename__ = "processing_results"  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, index=True)  
    # id: Clave primaria de tipo entero para identificar cada resultado. `index=True` acelera consultas.

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)  
    # Clave foránea que conecta este resultado con un dispositivo en la tabla "devices".
    # Es obligatorio (`nullable=False`).

    average_before_normalization = Column(Float, nullable=False)  
    # Promedio de los datos antes de ser normalizados, como flotante. Obligatorio.

    average_after_normalization = Column(Float, nullable=False)  
    # Promedio de los datos después de ser normalizados, también flotante y obligatorio.

    data_size = Column(Integer, nullable=False)  
    # Tamaño del conjunto de datos (número total de valores procesados). Es obligatorio.

    created_date = Column(TIMESTAMP, server_default=func.current_timestamp())  
    # Fecha de creación del registro. Por defecto, usa la fecha y hora actuales (`server_default`).

    updated_date = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())  
    # Fecha de actualización del registro. Se actualiza automáticamente cada vez que el registro cambia.

    # Relación inversa con el modelo "Device"
    device = relationship("Device", back_populates="results")  
    # Crea un vínculo hacia el dispositivo asociado a este resultado. `back_populates` sincroniza ambas tablas.
