# organizer.py
import os
import shutil  # Para mover archivos
import re  # Librería de Expresiones Regulares
import time  # Para manejar fechas de modificación
from auditor import registro_auditoria


@registro_auditoria
def organizar_por_extension(carpeta_origen, modo_simulacion=False):
    """
    Clasifica los archivos por extensión, fecha (Año-Mes) y tamaño.
    Retorna una lista de diccionarios con el detalle de cada archivo procesado.
    """
    if not os.path.exists(carpeta_origen):
        raise FileNotFoundError(f"La carpeta '{carpeta_origen}' no existe.")

    # Lista para almacenar datos reales para el reporte
    datos_para_reporte = []

    print(
        f"\n--- Iniciando Organización Multifactorial (Extensión, Fecha y Tamaño) ---"
    )

    for archivo in os.listdir(carpeta_origen):
        ruta_archivo = os.path.join(carpeta_origen, archivo)

        # Ignoramos subcarpetas y archivos ocultos
        if not os.path.isfile(ruta_archivo) or archivo.startswith("."):
            continue

        nombre, extension = os.path.splitext(archivo)
        if not extension:
            continue

        # 1. OBTENCIÓN DE METADATOS
        stats = os.stat(ruta_archivo)
        tamano_kb = stats.st_size / 1024
        cat_tamano = "Grandes" if tamano_kb > 1024 else "Pequeños"

        fecha_struct = time.localtime(stats.st_mtime)
        cat_fecha = time.strftime("%Y-%m", fecha_struct)
