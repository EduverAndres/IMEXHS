import os  # Módulo para trabajar con el sistema de archivos
import logging  # Para registrar errores y actividades importantes
import csv  # Biblioteca para leer y procesar archivos CSV
from typing import List, Tuple, Optional  # Para declarar listas, tuplas y tipos opcionales
import pydicom  # Biblioteca para leer archivos médicos DICOM
from pydicom.errors import InvalidDicomError  # Manejar errores en archivos DICOM no válidos
from PIL import Image  # Trabajar con imágenes (guardar, convertir, etc.)
import numpy as np  # Trabajar con datos numéricos, útil para procesar imágenes
from datetime import datetime  # Para manejar fechas y formatos de tiempo

class FileProcessor:
    def __init__(self, base_path: str, log_file: str):
        """
        Constructor de la clase FileProcessor: inicializa la ruta base y configura el logger.

        Args:
            base_path (str): Carpeta raíz para todas las operaciones de archivo.
            log_file (str): Archivo donde se registrarán errores y actividades relevantes.
        """
        self.base_path = base_path
        # Aseguramos que la carpeta base exista
        os.makedirs(self.base_path, exist_ok=True)

        # Configuramos el logger para registrar errores importantes
        logging.basicConfig(
            filename=log_file,  # Archivo de log donde guardaremos los errores
            level=logging.ERROR,  # Registramos solo errores graves
            format="%(asctime)s - %(levelname)s - %(message)s"  # Formato detallado para el log
        )
        self.logger = logging.getLogger()  # Inicializamos el logger para usarlo en los métodos

    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        """
        Lista los contenidos de una carpeta específica, opcionalmente incluye detalles.

        Args:
            folder_name (str): Nombre de la carpeta relativa a la ruta base.
            details (bool): Si es True, muestra tamaño de archivos y fechas de modificación.

        Returns:
            None: Solo imprime la información al usuario.
        """
        folder_path = os.path.join(self.base_path, folder_name)  # Ruta completa de la carpeta

        # Verificamos si la carpeta existe
        if not os.path.exists(folder_path):
            self.logger.error(f"La carpeta {folder_name} no existe.")  # Registramos el error en el log
            print(f"Error: La carpeta {folder_name} no existe.")  # Informamos al usuario
            return

        # Listamos todos los elementos en la carpeta
        files = os.listdir(folder_path)
        print(f"Carpeta: {folder_path}")
        print(f"Número de elementos: {len(files)}")  # Mostramos el número de archivos y carpetas

        files_list, folders_list = [], []  # Separaremos archivos y carpetas en dos listas

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):  # Si el elemento es un archivo
                if details:  # Si queremos más información
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Calculamos el tamaño en MB
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                    files_list.append(f"- {file_name} ({size_mb:.2f} MB, Última Modificación: {last_modified})")
                else:
                    files_list.append(f"- {file_name} (Archivo)")
            elif os.path.isdir(file_path):  # Si el elemento es una carpeta
                last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                folders_list.append(f"- {file_name} (Última Modificación: {last_modified})")

        # Mostramos los resultados al usuario
        print("Archivos:")
        print("\n".join(files_list))  # Listamos los archivos
        print("Carpetas:")
        print("\n".join(folders_list))  # Listamos las carpetas
    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        """
        Analiza un archivo CSV, mostrando estadísticas para columnas numéricas
        y un resumen para las columnas no numéricas. También permite generar un reporte.

        Args:
            filename (str): Nombre del archivo CSV a procesar.
            report_path (Optional[str]): Ruta donde se guardará el análisis (opcional).
            summary (bool): Si es True, incluye un resumen de columnas no numéricas.
        """
        file_path = os.path.join(self.base_path, filename) if not os.path.isabs(filename) else filename

        # Verificamos si el archivo existe
        if not os.path.exists(file_path):
            self.logger.error(f"El archivo {filename} no existe.")  # Registramos el error en el log
            print(f"Error: El archivo {filename} no existe.")  # Informamos al usuario
            return

        try:
            # Abrimos el archivo y usamos el lector de CSV
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                headers = next(reader)  # Capturamos las columnas
                rows = list(reader)  # Convertimos el contenido en una lista de filas

                print(f"Columnas: {headers}")
                print(f"Número de filas: {len(rows)}")

                # Procesamos las columnas numéricas
                numeric_data = {header: [] for header in headers}  # Diccionario para los datos numéricos
                for row in rows:
                    for i, value in enumerate(row):
                        try:
                            numeric_data[headers[i]].append(float(value))  # Convertimos a float si es posible
                        except ValueError:
                            pass  # Ignoramos los valores no numéricos

                # Calculamos estadísticas para columnas numéricas
                for header, values in numeric_data.items():
                    if values:
                        avg = sum(values) / len(values)  # Calculamos el promedio
                        std = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5  # Calculamos la desviación estándar
                        print(f"- {header}: Promedio = {avg:.2f}, Desv. Est. = {std:.2f}")

                # Guardamos el análisis en un archivo si se especifica una ruta
                if report_path:
                    with open(report_path, "w") as report:
                        for header, values in numeric_data.items():
                            if values:
                                avg = sum(values) / len(values)
                                std = (sum((x - avg) ** 2 for x in values)) ** 0.5
                                report.write(f"{header}: Promedio = {avg:.2f}, Desv. Est. = {std:.2f}\n")
                    print(f"Reporte guardado en {report_path}")

                # Procesamos columnas no numéricas si se solicita
                if summary:
                    for header in headers:
                        non_numeric = [row[headers.index(header)] for row in rows if not row[headers.index(header)].isdigit()]
                        unique_values = set(non_numeric)  # Obtenemos valores únicos
                        print(f"- {header}: Valores únicos = {len(unique_values)}")

        except Exception as e:
            self.logger.error(f"Error al leer el archivo CSV: {e}")  # Registramos cualquier error
            print(f"Error al leer el archivo CSV: {e}")  # Informamos al usuario

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        """
        Procesa un archivo DICOM para extraer información médica y opcionalmente guardar la imagen.

        Args:
            filename (str): Nombre del archivo DICOM.
            tags (Optional[List[Tuple[int, int]]]): Etiquetas específicas para extraer información adicional.
            extract_image (bool): Si es True, extrae la imagen DICOM y la guarda como PNG.
        """
        file_path = os.path.join(self.base_path, filename) if not os.path.isabs(filename) else filename

        # Verificamos si el archivo existe
        if not os.path.exists(file_path):
            self.logger.error(f"El archivo DICOM {filename} no existe.")  # Registramos el error en el log
            print(f"Error: El archivo DICOM {filename} no existe.")  # Informamos al usuario
            return

        try:
            dicom_file = pydicom.dcmread(file_path)  # Usamos pydicom para leer el archivo DICOM
            print(f"Nombre del Paciente: {dicom_file.PatientName}")  # Mostramos el nombre del paciente
            print(f"Fecha del Estudio: {dicom_file.StudyDate}")  # Mostramos la fecha del estudio
            print(f"Modalidad: {dicom_file.Modality}")  # Mostramos la modalidad del estudio

            # Extraemos etiquetas si se especifican
            if tags:
                for tag in tags:
                    print(f"Etiqueta {tag}: {dicom_file.get(tag, 'No encontrada')}")

            # Si se solicita, extraemos la imagen y la guardamos como PNG
            if extract_image:
                if hasattr(dicom_file, "pixel_array"):  # Verificamos si el archivo contiene datos de píxeles
                    try:
                        # Normalizamos los datos de píxeles y convertimos a imagen
                        pixel_array = dicom_file.pixel_array
                        normalized_array = (pixel_array / pixel_array.max() * 255).astype(np.uint8)
                        img = Image.fromarray(normalized_array)  # Convertimos los píxeles en una imagen
                        output_path = os.path.join(self.base_path, f"{os.path.splitext(filename)[0]}.png")
                        img.save(output_path)  # Guardamos la imagen como PNG
                        print(f"Imagen extraída guardada en {output_path}")
                    except Exception as e:
                        self.logger.error(f"No se pudo procesar la imagen DICOM: {e}")  # Registramos cualquier error
                        print(f"Error: No se pudo procesar la imagen DICOM.")  # Informamos al usuario
                else:
                    print("El archivo DICOM no contiene datos de imagen.")  # Informamos que no hay datos de píxeles

        except InvalidDicomError as e:
            self.logger.error(f"Archivo DICOM inválido: {e}")  # Registramos el error si el archivo no es válido
            print(f"Error: Archivo DICOM inválido.")  # Informamos al usuario
