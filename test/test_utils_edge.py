"""
Tests de edge cases y ramas internas para utilidades científicas en TUI v4.1 Toy Model — RL Symbiosis
Edge case and branch tests for scientific utilities in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.gui_utils import confidence_interval, calcular_intervalo_confianza
from scipy.stats import ttest_ind, f_oneway

def test_confidence_interval_empty():
    datos = []
    mean, ci = confidence_interval(datos)
    assert isinstance(mean, float)
    assert isinstance(ci, tuple)

def test_confidence_interval_nan():
    datos = [np.nan, np.nan]
    mean, ci = confidence_interval(datos)
    assert np.isnan(mean)
    assert all(np.isnan(x) for x in ci)

def test_ttest_ind_edge():
    a = [1, 2, 3]
    b = [1, 2, 3]
    stat, p = ttest_ind(a, b)
    assert isinstance(stat, float)
    assert isinstance(p, float)

def test_f_oneway_edge():
    a = [1, 2, 3]
    b = [1, 2, 3]
    stat, p = f_oneway(a, b)
    assert isinstance(stat, float)
    assert isinstance(p, float)
