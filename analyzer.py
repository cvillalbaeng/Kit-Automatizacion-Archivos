# analyzer.py
import os
import re
from auditor import registro_auditoria


# ==========================================
# EL GENERADOR OBLIGATORIO
# ==========================================
def leer_archivo_grande(ruta_archivo):
    """
    Generador que lee un archivo línea por línea.
    Usa 'yield' en lugar de 'return' para no cargar todo el archivo en la RAM.
    """
    # Usamos with open() como exige el PDF
    with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            yield linea  # Pausa la función, entrega la línea, y espera a que le pidan la siguiente


@registro_auditoria
def buscar_correos_regex(ruta_archivo):
    """
    Usa un generador y Regex para extraer todos los correos electrónicos de un archivo.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo para analizar: {ruta_archivo}"
        )

    # Este es el patrón estándar internacional de Regex para correos electrónicos
    patron_correo = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    regex = re.compile(patron_correo)

    # Usamos un CONJUNTO (set) para guardar correos únicos y evitar duplicados
    correos_encontrados = set()

    print(f"\n--- Analizando archivo: {os.path.basename(ruta_archivo)} ---")

# Consumimos el generador linea por linea
    for linea in leer_archivo_grande(ruta_archivo):
        # findall busca todas las coincidencias del regex en la linea actual
        coincidencias = regex.findall(linea)
        for correo in coincidencias:
            correos_encontrados.add(correo)  # .add() mete el elemento en el set

    return list(
        correos_encontrados
    )  # Convertimos el set a lista para retornarlo más fácil
