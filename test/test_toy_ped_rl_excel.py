"""
Tests para toy_ped_rl_excel.py — Simulación y análisis con datos reales
Unit tests for toy_ped_rl_excel.py — Real data simulation and analysis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.toy_ped_rl_excel import System, load_systems_from_csv, compute_I_justo

def test_system_dataclass_excel():
    s = System(name="Test", tipo="IA", C=0.5, F=0.5, T=0.5, I_op=0.5, vida=10, tasa=100, complejidad=1.0, P_riesgo=0.1, observaciones="Ninguna")
    assert s.name == "Test"
    assert s.tipo == "IA"
    assert s.P_riesgo == 0.1

def test_compute_I_justo():
    s = System(name="Test", tipo="IA", C=1.0, F=1.0, T=1.0, I_op=1.0, vida=10, tasa=100, complejidad=1.0, P_riesgo=0.1, observaciones="Ninguna")
    I = compute_I_justo(s)
    assert isinstance(I, float)
