"""
Tests exhaustivos de ramas y edge cases para toy_ped_rl_excel.py
Full branch and edge case tests for toy_ped_rl_excel.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.toy_ped_rl_excel import cargar_datos_excel, analizar_datos, compute_I_justo, pearson_correlation

def test_cargar_datos_excel_inexistente():
    sistemas = cargar_datos_excel('no_existe.csv')
    assert sistemas == []

def test_analizar_datos_empty():
    resultados = analizar_datos([])
    assert resultados["media_I_op"] == 0.0
    assert resultados["correlacion"] == 0.0

def test_compute_I_justo_branch():
    class Dummy:
        C = 1.0
        F = 1.0
        T = 1.0
        Tiss = 1.0
        Meta = 1.0
    val = compute_I_justo(Dummy())
    assert isinstance(val, float)

def test_pearson_correlation_branch():
    x = [1,2,3]
    y = [1,2,3]
    corr = pearson_correlation(x, y)
    assert corr == 1.0
    corr_zero = pearson_correlation([],[])
    assert corr_zero == 0.0
