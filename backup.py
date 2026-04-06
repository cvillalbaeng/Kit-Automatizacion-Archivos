# Importamos shutil, la librería estándar de Python para operaciones de alto nivel con archivos (como zipear)
import shutil

# Importamos os para manejar rutas
import os

# Importamos datetime para ponerle la fecha al nombre del archivo
from datetime import datetime

# Importamos nuestro propio decorador del módulo auditor
from auditor import registro_auditoria


@registro_auditoria
def crear_respaldo(carpeta_origen, carpeta_destino="backups"):
    """
    Comprime la carpeta de pruebas en un .zip y la guarda en una carpeta aislada.
    """
    # Verificamos que la carpeta de origen (ej: tests_sample) exista
    if not os.path.exists(carpeta_origen):
        raise FileNotFoundError(
            f"Imposible respaldar. La carpeta '{carpeta_origen}' no existe."
        )

    # Se crea la carpeta de 'backups' si el usuario no la ha creado aún
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Crea un nombre único para el zip basado en la fecha y hora actual (ej: respaldo_20260327_112030)
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_base = f"respaldo_{fecha_str}"

    # Une la ruta de destino con el nombre del archivo (ej: backups/respaldo_2026...)
    ruta_guardado = os.path.join(carpeta_destino, nombre_base)

    # Utiliza shutil.make_archive para empaquetar la carpeta entera en un .zip
    # Parámetros: (donde se guarda, formato, qué carpeta se va a comprimir)
    ruta_zip_creado = shutil.make_archive(ruta_guardado, "zip", carpeta_origen)

    return ruta_zip_creado
