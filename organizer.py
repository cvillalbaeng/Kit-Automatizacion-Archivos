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

        # 2. DEFINICIÓN DE ESTRUCTURA
        ext_limpia = extension.replace(".", "").lower()
        subcarpeta_destino = os.path.join(
            carpeta_origen, ext_limpia, cat_fecha, cat_tamano
        )
        ruta_destino_final = os.path.join(subcarpeta_destino, archivo)

        # 3. PREVENCIÓN DE SOBRESCRITURA
        nombre_final = archivo
        if os.path.exists(ruta_destino_final):
            nombre_final = f"{nombre}_copia{extension}"
            ruta_destino_final = os.path.join(subcarpeta_destino, nombre_final)

        # GUARDAR DATOS PARA EL REPORTE
        datos_para_reporte.append(
            {
                "Archivo": nombre_final,
                "Categoria": f"{ext_limpia}/{cat_fecha}/{cat_tamano}",
                "Correos_Hallados": 0,
            }
        )

        if modo_simulacion:
            if nombre_final != archivo:
                print(
                    f"[Simulación] PRECAUCIÓN: '{archivo}' ya existe. Se renombraría a '{nombre_final}'"
                )
            print(
                f"[Simulación] Ubicaría '{archivo}' en: {ext_limpia}/{cat_fecha}/{cat_tamano}/"
            )
        else:
            if not os.path.exists(subcarpeta_destino):
                os.makedirs(subcarpeta_destino)

            shutil.move(ruta_archivo, ruta_destino_final)

            if nombre_final != archivo:
                print(
                    f"[Movido] '{archivo}' ---> {ext_limpia}/{cat_fecha}/{cat_tamano}/{nombre_final} (Renombrado)"
                )
            else:
                print(
                    f"[Movido] '{archivo}' ---> {ext_limpia}/{cat_fecha}/{cat_tamano}/"
                )

    return datos_para_reporte


@registro_auditoria
def renombrar_con_regex(
    carpeta_origen, patron_buscar, texto_reemplazo, modo_simulacion=False
):
    """
    Busca archivos cuyos nombres coincidan con una Expresión Regular y los renombra.
    Retorna la lista de cambios para el reporte.
    """
    datos_para_reporte = []
    print(f"\n--- Iniciando Renombrado con Regex: '{patron_buscar}' ---")

    try:
        regex = re.compile(patron_buscar)
    except re.error:
        raise ValueError(f"El patrón Regex '{patron_buscar}' no es válido.")

    for archivo in os.listdir(carpeta_origen):
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        if not os.path.isfile(ruta_archivo):
            continue

        nuevo_nombre = regex.sub(texto_reemplazo, archivo)

        # Si el nombre cambió, hubo un "match"
        if nuevo_nombre != archivo:
            ruta_nueva = os.path.join(carpeta_origen, nuevo_nombre)

            # Guardar el cambio para el reporte
            datos_para_reporte.append(
                {
                    "Archivo": nuevo_nombre,
                    "Categoria": "Renombrado por Regex",
                    "Correos_Hallados": 0,
                }
            )

            if modo_simulacion:
                print(f"[Simulación] Renombraría: '{archivo}' ---> '{nuevo_nombre}'")
            else:
                os.rename(ruta_archivo, ruta_nueva)
                print(f"[Renombrado] '{archivo}' ---> '{nuevo_nombre}'")

    return datos_para_reporte
