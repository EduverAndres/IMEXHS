from pydantic import BaseModel  # Clase base para definir esquemas de datos validados
from typing import List  # Para manejar listas en los tipos

# Clase base para el dispositivo
class DeviceBase(BaseModel):
    device_name: str  # El nombre del dispositivo, es obligatorio

# Clase para la creación de un dispositivo
class DeviceCreate(DeviceBase):
    pass  # No agregamos nuevos campos, simplemente heredamos de DeviceBase

# Clase base para los resultados del procesamiento
class ProcessingResultBase(BaseModel):
    device_id: int  # Identificador del dispositivo asociado (clave foránea)
    average_before_normalization: float  # Promedio calculado antes de la normalización
    average_after_normalization: float  # Promedio calculado después de la normalización
    data_size: int  # Cantidad de datos procesados

# Clase para la creación de resultados de procesamiento
class ProcessingResultCreate(ProcessingResultBase):
    pass  # No necesitamos nuevos campos, heredamos de ProcessingResultBase

# Clase para los resultados completos (usada en respuestas de la API)
class ProcessingResult(ProcessingResultBase):
    id: int  # ID único del resultado
    created_date: str  # Fecha en que se creó el registro, representada como string
    updated_date: str  # Fecha en que se actualizó el registro, representada como string

    class Config:
        from_attributes = True  # Habilita la conversión directa desde modelos o atributos
