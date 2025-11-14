"""
Tests exhaustivos de ramas y edge cases para utilidades científicas en gui_utils.py
Full branch and edge case tests for scientific utilities in gui_utils.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.gui_utils import confidence_interval, t_test, anova, scientific_report

def test_confidence_interval_nan_branch():
    arr = np.array([np.nan, np.nan])
    ci = confidence_interval(arr)
    assert isinstance(ci, tuple)

def test_t_test_branch():
    a = np.array([1,2,3])
    b = np.array([1,2,3])
    t, p = t_test(a, b)
    assert isinstance(t, float) and isinstance(p, float)

def test_anova_branch():
    groups = [np.array([1,2,3]), np.array([1,2,3]), np.array([1,2,3])]
    f, p = anova(groups)
    assert isinstance(f, float) and isinstance(p, float)

def test_scientific_report_branch():
    metricas_A = {"flex_recov": [1,2], "robust_evol": [1,2], "q_optimal_evol": [1,2], "total_rewards": [1,2], "tripwire_steps": [1,2]}
    metricas_B = {"flex_recov": [2,3], "robust_evol": [2,3], "q_optimal_evol": [2,3], "total_rewards": [2,3], "tripwire_steps": [2,3]}
    report = scientific_report(metricas_A, metricas_B)
    assert "flex_recov" in report
