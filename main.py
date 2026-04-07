# main.py
import os
import auditor
import backup
import organizer
import analyzer
import reports


def mostrar_menu():
    """Imprime las opciones disponibles en la interfaz CLI."""
    print("\n" + "=" * 55)
    print("   KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN DE ARCHIVOS   ")
    print("=" * 55)
    print("1. Tomar Snapshot (Auditoría inicial de la carpeta)")
    print("2. Crear Respaldo de Seguridad (.zip)")
    print("3. Organizar (Por Extensión, Fecha y Tamaño)")
    print("4. Analizar Contenido (Buscar Correos con Regex)")
    print("5. Generar Reportes REALES (CSV y TXT)")
    print("6. Comparar Cambios (Auditoría vs. último Snapshot)")
    print("0. Salir del Sistema")
    print("=" * 55)


def main():
    carpeta_test = "tests_sample"
    # --- NUEVO: Variable para persistir los datos reales entre opciones ---
    ultimos_datos_reales = []

    if not os.path.exists(carpeta_test):
        os.makedirs(carpeta_test)
        print(f"[*] AVISO: Se creó la carpeta '{carpeta_test}'.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                auditor.tomar_snapshot(carpeta_test)
                print("\n[ÉXITO] Snapshot guardado en 'snapshot.json'.")

            elif opcion == "2":
                ruta_zip = backup.crear_respaldo(carpeta_test)
                print(f"\n[ÉXITO] Respaldo creado en: {ruta_zip}")

            elif opcion == "3":
                while True:
                    simular = (
                        input("¿Desea correr en modo simulación (dry-run)? (s/n): ")
                        .lower()
                        .strip()
                    )
                    if simular in ["s", "n"]:
                        break
                    else:
                        print("  [!] Ingrese 's' o 'n'.")

                modo_sim = True if simular == "s" else False

                # --- INTEGRACIÓN: Capturamos la lista detallada ---
                resultado_org = organizer.organizar_por_extension(
                    carpeta_test, modo_simulacion=modo_sim
                )

                # Si no fue simulación, guardamos los datos para el reporte
                if not modo_sim:
                    ultimos_datos_reales = resultado_org

                tipo_op = "Simulación" if modo_sim else "Organización"
                print(
                    f"\n[ÉXITO] {tipo_op} completada. Items detectados: {len(resultado_org)}"
                )

            elif opcion == "4":
                nombre_archivo = input("Ingrese el nombre del archivo de texto: ")
                correos = analyzer.buscar_correos_regex(nombre_archivo)
                print(
                    f"\n[ÉXITO] Análisis finalizado. Se hallaron {len(correos)} correos."
                )
                if correos:
                    for c in correos:
                        print(f" - {c}")

            elif opcion == "5":
                # --- MEJORA: Validación de datos reales para el reporte ---
                if not ultimos_datos_reales:
                    print("\n[!] AVISO: No hay datos de organización recientes.")
                    print(
                        "Se generará un reporte con datos de ejemplo para la demostración."
                    )
                    datos_a_reportar = [
                        {
                            "Archivo": "ejemplo_demo.pdf",
                            "Categoria": "pdf/demo",
                            "Correos_Hallados": 0,
                        }
                    ]
                else:
                    datos_a_reportar = ultimos_datos_reales

                # Ejecución de reportes con los datos capturados
                nombre_csv = reports.generar_reporte_csv(datos_a_reportar)
                nombre_txt = reports.generar_reporte_txt(datos_a_reportar)

                tipo_rep = "REAL" if ultimos_datos_reales else "DE EJEMPLO"
                print(f"\n[ÉXITO] Reporte {tipo_rep} generado.")
                print(f" -> CSV: {nombre_csv}\n -> TXT: {nombre_txt}")

            elif opcion == "6":
                print("\n--- Analizando diferencias en el sistema ---")
                cambios = auditor.comparar_cambios(carpeta_test)

                print("[ÉXITO] Auditoría comparativa completada:")

                # Si la lista está vacía, mostramos "Ninguno" para que se vea limpio
                agregados = cambios["agregados"] if cambios["agregados"] else "Ninguno"
                movidos = cambios["eliminados"] if cambios["eliminados"] else "Ninguno"

                print(f" -> Archivos Nuevos/Detectados: {agregados}")
                print(
                    f" -> Archivos Organizados/Reubicados: {movidos}"
                )  # <--- CAMBIO AQUÍ

                print(
                    "\n[*] Nota: Los archivos 'Reubicados' ya no están en la raíz porque"
                )
                print("    ahora residen en sus respectivas subcarpetas jerárquicas.")

            elif opcion == "0":
                print("\nCerrando el sistema... ¡Mucho éxito en la defensa, Christian!")
                break
            else:
                print("\n[!] Opción inválida (0-6).")

        except FileNotFoundError as e:
            print(f"\n[ERROR]: No se encontró el archivo o ruta: {e}")
        except ValueError as e:
            print(f"\n[ERROR]: Datos inválidos: {e}")
        except Exception as e:
            print(f"\n[ERROR CRÍTICO]: {e}")


if __name__ == "__main__":
    main()
