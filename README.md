# Proyecto Final

# 🗂️ Kit Multifuncional de Automatización de Archivos

## 📖 Descripción del Proyecto

Este proyecto es una herramienta de Interfaz de Línea de Comandos (CLI) desarrollada íntegramente en Python. Su objetivo es automatizar el manejo, organización, auditoría y análisis de grandes volúmenes de archivos en sistemas de almacenamiento local.

Fue diseñado bajo el principio de **Separación de Responsabilidades (SRP)**, garantizando un código modular, escalable y sin dependencias de librerías externas (Zero Dependencies).

## ✨ Características Principales

- **📂 Organización Jerárquica:** Clasifica archivos automáticamente creando un árbol de directorios basado en extensión, fecha de modificación (Año-Mes) y tamaño del archivo.
- **🛡️ Prevención de Colisiones:** Sistema inteligente de renombrado (`_copia`) para evitar la sobrescritura y pérdida de datos.
- **📊 Auditoría por Conjuntos:** Utiliza teoría de conjuntos (Sets) con complejidad `O(1)` para comparar y detectar cambios exactos entre snapshots del sistema.
- **🔍 Análisis Léxico Eficiente:** Implementa Generadores (`yield`) y Expresiones Regulares (Regex) para procesar archivos de texto masivos sin desbordar la memoria RAM.
- **📑 Reportes Dinámicos:** Genera reportes del estado real de los archivos procesados en formatos `.txt` y `.csv` (con soporte UTF-8-SIG para compatibilidad regional en MS Excel).
- **📦 Seguridad y Respaldo:** Creación automática de copias de seguridad en formato comprimido `.zip`.

## 🏗️ Estructura del Proyecto

```text
📦 Kit-Automatizacion-Archivos
 ┣ 📜 main.py          # Orquestador del flujo y menú CLI
 ┣ 📜 organizer.py     # Lógica de clasificación multifactorial
 ┣ 📜 auditor.py       # Trazabilidad, logs y comparación de snapshots
 ┣ 📜 analyzer.py      # Búsqueda de patrones con Regex
 ┣ 📜 reports.py       # Generación de archivos CSV y TXT
 ┣ 📜 backup.py        # Compresión de seguridad
 ┣ 📜 README.md        # Documentación del proyecto
 ┣ 📂 tests_sample/    # Directorio de pruebas (Generado automáticamente)
 ┗ 📂 backups/         # Repositorio de respaldos (Generado automáticamente)


**## 👨‍💻 Equipo de Desarrollo (Autores):**


1. **Christian Villalba** - Modulos Main y Backup
2. **[Wilmer Maldonado]** - Modulo Auditor
3. **[David González]**   - Modulos Reports Analyzer
4. **[José Ruíz]**        - Modulo Organyzer


⚙️ Requisitos Previos
Python 3.8 o superior instalado en el sistema.

No se requieren librerías externas (usa exclusivamente la Standard Library de Python: os, shutil, re, time, json, csv).


🚀 Instalación y Ejecución
1. Clonar el repositorio:

Bash
git clone [https://github.com/cvillalbaeng/Kit-Automatizacion-Archivos.git]
cd Kit-Automatizacion-Archivos
2. Crear y activar un entorno virtual (Recomendado):

En Windows (Git Bash / MINGW64):

Bash
python -m venv venv
source venv/Scripts/activate
En macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Ejecutar la herramienta:

Bash
python main.py


## 🕹️ Guía de Uso:

Al ejecutar main.py, se desplegará el siguiente menú interactivo:

1- Tomar Snapshot: Escanea la carpeta tests_sample y guarda su estado base en snapshot.json.

2- Crear Respaldo: Comprime la carpeta de pruebas y la guarda en backups/.

3- Organizar Archivos: Solicita confirmación para modo simulación (dry-run) o ejecución real. Clasifica los archivos y guarda los datos en memoria.

4- Analizar Contenido: Permite buscar correos electrónicos en un archivo de texto específico usando Regex.

5- Generar Reportes: Exporta los resultados de la última organización a CSV y TXT.

6-Comparar Cambios: Audita el estado actual contra el último Snapshot para reportar archivos nuevos o reubicados.

7- Salir: Cierra el sistema de forma segura.
```
