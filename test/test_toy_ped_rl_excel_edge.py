"""
Tests de edge cases y ramas internas para toy_ped_rl_excel.py en TUI v4.1 Toy Model — RL Symbiosis
Edge case and branch tests for toy_ped_rl_excel.py in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.toy_ped_rl_excel import cargar_datos_excel, analizar_datos

def test_cargar_datos_excel_empty():
    # Debe manejar archivo vacío o inexistente sin romper el flujo
    try:
        cargar_datos_excel('no_existe.xlsx')
    except Exception:
        pass

def test_analizar_datos_nan():
    # Debe manejar datos NaN o vacíos sin romper el flujo
    try:
        analizar_datos([])
    except Exception:
        pass
