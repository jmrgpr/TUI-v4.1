from sim.toy_ped_rl_excel import demo_ped_real, demo_sensibilidad_real, System
import matplotlib.pyplot as plt

import pytest

@pytest.fixture
def small_systems():
    # Datos mínimos y representativos para test
    return [
        System(name="A", tipo="bio", C=0.1, F=0.2, T=0.3, I_op=0.4, vida=1, tasa=1, complejidad=1, P_riesgo=0.5, observaciones=""),
        System(name="B", tipo="ia", C=0.2, F=0.3, T=0.4, I_op=0.5, vida=2, tasa=2, complejidad=2, P_riesgo=0.6, observaciones="")
    ]

@pytest.fixture(autouse=True)
def no_show(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **kw: None)

def test_demo_ped_real_branches(small_systems):
    demo_ped_real.__globals__["load_systems_from_csv"] = lambda path: small_systems
    demo_ped_real("dummy.csv")

def test_demo_sensibilidad_real_branches(small_systems):
    import matplotlib
    matplotlib.use('Agg', force=True)
    demo_sensibilidad_real.__globals__["load_systems_from_csv"] = lambda path: small_systems
    demo_sensibilidad_real("dummy.csv")
import pytest
from sim.toy_ped_rl_excel import cargar_datos_excel, analizar_datos, export_to_excel
import os
import pandas as pd

# Test: cargar_datos_excel con archivo inexistente (branch except)
def test_cargar_datos_excel_inexistente():
    result = cargar_datos_excel("no_existe.csv")
    assert result == []

# Test: cargar_datos_excel con archivo CSV vacío (branch for except)
def test_cargar_datos_excel_vacio(tmp_path):
    csv_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(csv_path)
    result = cargar_datos_excel(str(csv_path))
    assert result == []

# Test: export_to_excel con excepción (branch except)
def test_export_to_excel_exception(monkeypatch):
    class BadDF:
        def to_csv(self, *a, **kw): raise Exception("fail")
        def to_excel(self, *a, **kw): raise Exception("fail")
    monkeypatch.setattr("pandas.DataFrame", lambda *a, **kw: BadDF())
    export_to_excel([{"a":1}], "file.csv")  # No debe lanzar excepción

# Test: analizar_datos con lista vacía (branch if not sistemas)
def test_analizar_datos_vacio():
    result = analizar_datos([])
    assert result == {"media_I_op": 0.0, "media_P_riesgo": 0.0, "correlacion": 0.0}
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
