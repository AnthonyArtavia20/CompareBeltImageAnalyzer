# Punto de partida desde donde se inicia el programa
import os
import sys

# Obtener la ruta del directorio raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)  # Añade el directorio raíz al principio de sys.path

# Importar y ejecutar el script principal
from Core.CompareBeltStartUp import main

# Llamar a la función principal con el propósito de iniciar el programa
main()