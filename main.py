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
    print("Iniciando sistema...")
    # La lógica será agregada por el equipo
    pass


if __name__ == "__main__":
    main()
