import logging  # Para registrar actividades y errores en el sistema
from fastapi import APIRouter, Depends, HTTPException  # APIRouter: Para definir rutas. HTTPException: Para manejar errores.
from sqlalchemy.orm import Session  # Maneja las interacciones con la base de datos
from ..database import SessionLocal  # Importamos la configuración de la base de datos (sesión)
from ..models import Device, ProcessingResult  # Modelos de la base de datos (Device y ProcessingResult)
from ..schemas import DeviceCreate, ProcessingResultCreate  # Schemas para validar y estructurar datos
from ..utils import normalize_data  # Función para normalizar los datos

router = APIRouter()  # Instanciamos el router para registrar las rutas de este módulo

# Dependencia para obtener una sesión de la base de datos
def get_db():
    """
    Abre una conexión a la base de datos y la cierra automáticamente al terminar.
    """
    db = SessionLocal()
    try:
        yield db  # Permite usar `db` en los endpoints
    finally:
        db.close()  # Cerramos la conexión para evitar fugas


@router.post("/elements/")
def create_processing_results(payload: dict, db: Session = Depends(get_db)):
    """
    Crea nuevos resultados de procesamiento basados en los datos recibidos en formato JSON.

    Args:
        payload (dict): Carga JSON con dispositivos y datos para procesar.
        db (Session): Sesión de la base de datos proporcionada por `get_db`.

    Returns:
        dict: Mensaje indicando si los datos fueron procesados exitosamente.
    """
    try:
        for key, value in payload.items():  # Iteramos sobre los elementos en la carga JSON
            # Verificamos si el dispositivo ya existe en la base de datos
            device = db.query(Device).filter(Device.device_name == value["deviceName"]).first()
            if not device:  # Si no existe, lo creamos
                device = Device(device_name=value["deviceName"])
                db.add(device)  # Agregamos el dispositivo a la sesión
                db.commit()  # Confirmamos los cambios
                db.refresh(device)  # Refrescamos para obtener el ID generado

            # Procesamos los datos (normalización y cálculo de promedios)
            data = [list(map(int, row.split())) for row in value["data"]]  # Convertimos las cadenas en números
            avg_before, avg_after, data_size = normalize_data(data)

            # Creamos un nuevo registro de resultados en la base de datos
            result = ProcessingResult(
                device_id=device.id,
                average_before_normalization=avg_before,
                average_after_normalization=avg_after,
                data_size=data_size
            )
            db.add(result)  # Agregamos el resultado a la sesión
            db.commit()  # Confirmamos los cambios

        logging.info("Datos procesados exitosamente")
        return {"detail": "Datos procesados exitosamente"}  # Mensaje de éxito
    except Exception as e:
        logging.error(f"Error al procesar datos: {str(e)}")  # Registramos el error
        raise HTTPException(status_code=500, detail="Error al procesar los datos")  # Lanzamos una excepción HTTP


@router.get("/elements/")
def read_processing_results(db: Session = Depends(get_db)):
    """
    Recupera todos los resultados de procesamiento almacenados en la base de datos.

    Args:
        db (Session): Sesión de la base de datos proporcionada por `get_db`.

    Returns:
        list: Lista de resultados de procesamiento.
    """
    try:
        results = db.query(ProcessingResult).all()  # Consultamos todos los resultados
        logging.info(f"Se obtuvieron {len(results)} resultados")
        return results  # Devolvemos la lista
    except Exception as e:
        logging.error(f"Error al obtener resultados: {str(e)}")  # Registramos el error
        raise HTTPException(status_code=500, detail="Error al obtener los resultados")  # Lanzamos una excepción HTTP


@router.get("/elements/{id}/")
def read_processing_result(id: int, db: Session = Depends(get_db)):
    """
    Recupera un resultado de procesamiento específico por su ID.

    Args:
        id (int): Identificador único del resultado.
        db (Session): Sesión de la base de datos proporcionada por `get_db`.

    Returns:
        ProcessingResult: Resultado encontrado o excepción en caso de error.
    """
    try:
        result = db.query(ProcessingResult).filter(ProcessingResult.id == id).first()
        if not result:  # Si no se encuentra el resultado, lanzamos un error 404
            logging.warning(f"Resultado con ID {id} no encontrado")
            raise HTTPException(status_code=404, detail="Resultado no encontrado")
        logging.info(f"Resultado con ID {id} obtenido exitosamente")
        return result  # Devolvemos el resultado encontrado
    except Exception as e:
        logging.error(f"Error al obtener el resultado con ID {id}: {str(e)}")  # Registramos el error
        raise HTTPException(status_code=500, detail="Error al obtener el resultado")  # Lanzamos una excepción HTTP


@router.put("/elements/{id}/")
def update_device_name(id: int, updated_data: DeviceCreate, db: Session = Depends(get_db)):
    """
    Actualiza el nombre del dispositivo asociado a un resultado de procesamiento.

    Args:
        id (int): Identificador único del dispositivo.
        updated_data (DeviceCreate): Datos actualizados para el dispositivo.
        db (Session): Sesión de la base de datos proporcionada por `get_db`.

    Returns:
        Device: Dispositivo actualizado o excepción en caso de error.
    """
    try:
        device = db.query(Device).filter(Device.id == id).first()
        if not device:  # Si no se encuentra el dispositivo, lanzamos un error 404
            logging.warning(f"Dispositivo con ID {id} no encontrado")
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        device.device_name = updated_data.device_name  # Actualizamos el nombre del dispositivo
        db.commit()  # Confirmamos los cambios
        db.refresh(device)  # Refrescamos los datos para asegurar que están actualizados
        logging.info(f"Dispositivo con ID {id} actualizado exitosamente")
        return device  # Devolvemos el dispositivo actualizado
    except Exception as e:
        logging.error(f"Error al actualizar el dispositivo con ID {id}: {str(e)}")  # Registramos el error
        raise HTTPException(status_code=500, detail="Error al actualizar el dispositivo")  # Lanzamos una excepción HTTP


@router.delete("/elements/{id}/")
def delete_processing_result(id: int, db: Session = Depends(get_db)):
    """
    Elimina un resultado de procesamiento específico por su ID.

    Args:
        id (int): Identificador único del resultado.
        db (Session): Sesión de la base de datos proporcionada por `get_db`.

    Returns:
        dict: Mensaje indicando que el resultado fue eliminado exitosamente.
    """
    try:
        result = db.query(ProcessingResult).filter(ProcessingResult.id == id).first()
        if not result:  # Si no se encuentra el resultado, lanzamos un error 404
            logging.warning(f"Resultado con ID {id} no encontrado")
            raise HTTPException(status_code=404, detail="Resultado no encontrado")
        db.delete(result)  # Eliminamos el resultado
        db.commit()  # Confirmamos los cambios
        logging.info(f"Resultado con ID {id} eliminado exitosamente")
        return {"detail": "Resultado eliminado exitosamente"}  # Mensaje de éxito
    except Exception as e:
        logging.error(f"Error al eliminar el resultado con ID {id}: {str(e)}")  # Registramos el error
        raise HTTPException(status_code=500, detail="Error al eliminar el resultado")  # Lanzamos una excepción HTTP

