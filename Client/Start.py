# Punto de partida desde donde se inicia el programa

import os
import sys

# Obtener la ruta del directorio raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
core_path = os.path.join(project_root, 'Core')
sys.path.insert(0, core_path)  # Añade 'Core' al principio de sys.path

# Importar y ejecutar el script principal
from CompareBeltStartUp import main

# Llamar a la función principal
main()