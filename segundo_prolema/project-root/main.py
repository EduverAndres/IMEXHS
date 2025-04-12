from file_processor import FileProcessor  # Importamos nuestra clase personalizada
import os

# Creamos una instancia de FileProcessor con la ruta base y el archivo de registro
processor = FileProcessor(
    base_path="C:/Users/Danna/Desktop/Prueba_Tecnica/segundo_prolema/project-root/data", 
    log_file="C:/Users/Danna/Desktop/Prueba_Tecnica/segundo_prolema/project-root/logs/errors.log"
)

# Analizamos un archivo CSV y generamos un reporte
print("\n--- Análisis del archivo CSV ---")
processor.read_csv(
    filename="sample-02-csv.csv",  # Archivo que vamos a analizar
    report_path="C:/Users/Danna/Desktop/Prueba_Tecnica/segundo_prolema/project-root/reports/report.txt",  # Ruta donde se guarda el análisis
    summary=True  # Queremos también un resumen de las columnas no numéricas
)

# Analizamos un archivo DICOM y extraemos información de etiquetas y su imagen
print("\n--- Análisis del archivo DICOM: sample-02-dicom.dcm ---")
processor.read_dicom(
    filename="sample-02-dicom.dcm",  # Archivo DICOM que queremos analizar
    tags=[(0x0010, 0x0010), (0x0008, 0x0060)],  # Especificamos etiquetas para extraer
    extract_image=True  # Extraemos la imagen del archivo DICOM
)

# Analizamos un segundo archivo DICOM
print("\n--- Análisis del archivo DICOM: sample-02-dicom-2.dcm ---")
processor.read_dicom(
    filename="sample-02-dicom-2.dcm",  # Otro archivo DICOM
    tags=[(0x0010, 0x0010), (0x0008, 0x0060)],  # Reutilizamos las mismas etiquetas
    extract_image=True  # También extraemos la imagen de este archivo
)
