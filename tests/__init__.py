"""
Paquete de Pruebas del Sistema Experto Médico
Inicialización y configuración común
"""

import sys
import os

# Agregar el directorio src al path de Python
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Configuración global de pruebas
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

# Crear directorio de salida si no existe
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

__version__ = '1.0.0'
__author__ = 'Sistema Experto Médico Team'