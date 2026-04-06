# reports.py
import csv
from auditor import registro_auditoria


@registro_auditoria
def generar_reporte_csv(datos_reporte, nombre_archivo="reporte_analisis.csv"):
    """
    Genera un reporte en formato CSV compatible con Excel.
    Usa 'utf-8-sig' para que Excel reconozca eñes y tildes correctamente.
    """
    campos = ["Archivo", "Categoria", "Correos_Hallados"]

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        escritor.writerows(datos_reporte)

    return nombre_archivo


@registro_auditoria
def generar_reporte_txt(datos_reporte, nombre_archivo="reporte_analisis.txt"):
    """Genera un reporte en texto plano (.txt)."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo_txt:
        archivo_txt.write("REPORTE DE ANÁLISIS DE ARCHIVOS\n")
        archivo_txt.write("=" * 40 + "\n")
        for fila in datos_reporte:
            # Escribimos los datos en formato legible
            archivo_txt.write(
                f"Archivo: {fila['Archivo']} | Categ: {fila['Categoria']} | Hallazgos: {fila['Correos_Hallados']}\n"
            )
    print(f"[ÉXITO] Reporte TXT guardado en {nombre_archivo}")
    return nombre_archivo
