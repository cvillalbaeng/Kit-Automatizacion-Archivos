# Importamos la librería del sistema operativo para leer carpetas
import os

# Importamos json para guardar el snapshot como un archivo estructurado
import json

# Importamos datetime para saber la hora exacta de las operaciones
from datetime import datetime

# Importamos functools, una buena práctica para que el decorador no borre el nombre de la función original
import functools


def registro_auditoria(funcion):
    """
    Decorador que atrapa la ejecución de una función, mide su tiempo
    y anota en el audit.log si fue exitosa o si dio error.
    """

    @functools.wraps(
        funcion
    )  # Mantiene el nombre original de la función que vamos a envolver
    def envoltorio(
        *args, **kwargs
    ):  # *args y **kwargs permiten recibir cualquier parámetro
        # Guardamos la hora exacta en la que arranca la función
        inicio = datetime.now()

        # Bloque try-except para manejar cualquier error durante la ejecución
        try:
            # Ejecutamos la función real y guardamos lo que retorne
            resultado = funcion(*args, **kwargs)

            # --- CORRECCIÓN DE AUDITORÍA ---
            # Verificamos el nombre exacto de la función antes de cambiar el mensaje
            if funcion.__name__ == "organizar_por_extension":
                es_simulacion = kwargs.get("modo_simulacion", False)
                estado = (
                    "EXITO (MODO SIMULACIÓN)"
                    if es_simulacion
                    else "EXITO (ARCHIVOS MOVIDOS)"
                )
            else:
                # Para el resto de las funciones (snapshot, backup, analyzer, etc.)
                estado = "EXITO"

        except Exception as error:
            # Si explotó, capturamos el mensaje de error
            estado = f"ERROR ({str(error)})"
            # Volvemos a lanzar el error (raise) para que el main.py también se entere y no se quede callado
            raise

        finally:
            # El bloque finally se ejecuta SIEMPRE, haya error o no.
            fin = datetime.now()
            # Calculamos cuánto tardó restando el fin menos el inicio
            duracion = fin - inicio

            # Formateamos el mensaje que escribiremos en el log
            mensaje_log = f"[{inicio}] Función: {funcion.__name__} | Estado: {estado} | Duración: {duracion}\n"

            # Usamos 'with open()' en modo 'a' (append) para agregar líneas al final sin borrar lo anterior
            with open("audit.log", "a", encoding="utf-8") as archivo_log:
                archivo_log.write(mensaje_log)

        # Retornamos lo que sea que haya devuelto la función original
        return resultado

    # El decorador retorna la función envuelta lista para usarse
    return envoltorio

@registro_auditoria
def tomar_snapshot(carpeta_objetivo, archivo_salida="snapshot.json"):
    """
    Lee todos los archivos de la carpeta y guarda un 'mapa' con sus tamaños.
    """
    # Verificamos si la carpeta existe. Si no, lanzamos un error manual (raise)
    if not os.path.exists(carpeta_objetivo):
        raise FileNotFoundError(f"La carpeta '{carpeta_objetivo}' no existe.")

    # Creamos un diccionario vacío para guardar 'nombre_archivo': 'tamaño'
    snapshot = {}

    # Recorremos cada elemento dentro de la carpeta
    for nombre_archivo in os.listdir(carpeta_objetivo):
        # Unimos la ruta de la carpeta con el nombre del archivo (ej: tests_sample/archivo.txt)
        ruta_completa = os.path.join(carpeta_objetivo, nombre_archivo)

        # Verificamos que sea un archivo y no una sub-carpeta
        if os.path.isfile(ruta_completa):
            # Guardamos en el diccionario el tamaño en bytes
            snapshot[nombre_archivo] = os.path.getsize(ruta_completa)

    # Abrimos el archivo .json en modo escritura ('w' - write)
    with open(archivo_salida, "w", encoding="utf-8") as archivo_json:
        # Volcamos el diccionario de Python al archivo JSON con sangría de 4 espacios
        json.dump(snapshot, archivo_json, indent=4)

    return snapshot


@registro_auditoria
def comparar_cambios(carpeta_objetivo, archivo_snapshot="snapshot.json"):
    """
    Compara la carpeta actual contra el último snapshot guardado usando Conjuntos (Sets).
    """
    # 1. Intentamos leer el snapshot viejo (el mapa anterior)
    try:
        with open(archivo_snapshot, "r", encoding="utf-8") as archivo_json:
            snapshot_viejo = json.load(archivo_json)
    except FileNotFoundError:
        # Si no existe, lanzamos un error que el main.py atrapará
        raise ValueError(
            "No hay un snapshot previo para comparar. Por favor, ejecute la Opción 1 primero."
        )

    # 2. Tomamos un snapshot "al vuelo" (temporal) de cómo está la carpeta AHORA
    snapshot_nuevo = {}
    for nombre_archivo in os.listdir(carpeta_objetivo):
        ruta_completa = os.path.join(carpeta_objetivo, nombre_archivo)
        if os.path.isfile(ruta_completa):
            snapshot_nuevo[nombre_archivo] = os.path.getsize(ruta_completa)

# 3. CONJUNTOS (Sets):
    # Convertimos las listas de nombres de archivos en Conjuntos Matemáticos
    viejos_set = set(snapshot_viejo.keys())
    nuevos_set = set(snapshot_nuevo.keys())

    # Resta de conjuntos: Lo que está en los nuevos pero no en los viejos (Archivos agregados)
    agregados = nuevos_set - viejos_set

    # Resta de conjuntos: Lo que estaba en los viejos pero ya no está en los nuevos (Archivos borrados)
    eliminados = viejos_set - nuevos_set

            
    return {"agregados": list(agregados), "eliminados": list(eliminados)}
