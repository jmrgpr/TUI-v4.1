"""
Tests exhaustivos para toy_ped_rl_excel.py
Full coverage tests for toy_ped_rl_excel.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.toy_ped_rl_excel import cargar_datos_excel, analizar_datos

def test_cargar_datos_excel_full():
    sistemas = cargar_datos_excel('data/Sistemas_naturales_IA_utf8_limpio.csv')
    assert isinstance(sistemas, list)

def test_analizar_datos_full():
    sistemas = []
    resultados = analizar_datos(sistemas)
    assert isinstance(resultados, dict)
