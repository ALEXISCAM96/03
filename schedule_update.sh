#!/bin/bash

# Activar entorno virtual si se usa (opcional)
# source /ruta/a/tu/entorno/bin/activate

# Navegar al directorio donde está tu proyecto
cd /ruta/a/tu/proyecto

# Ejecutar el script
python update_csv_to_github_secure.py >> logs/update_log.txt 2>&1
