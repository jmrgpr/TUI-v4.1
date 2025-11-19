"""
Tests avanzados para utilidades científicas en TUI v4.1 Toy Model — RL Symbiosis
Advanced tests for scientific utilities in TUI v4.1 Toy Model — RL Symbiosis
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib
matplotlib.use('Agg')  # Hardening: backend sin GUI para tests
import numpy as np
from sim.gui_utils import calcular_intervalo_confianza, confidence_interval, plot_heatmap, plot_dashboard, safe_plot

def test_confidence_interval():
    datos = [1, 2, 3, 4, 5]
    mean, ci = confidence_interval(datos)
    assert isinstance(mean, float)
    assert isinstance(ci, tuple)
    assert all(isinstance(x, float) or isinstance(x, np.floating) for x in ci)

def test_confidence_interval_empty():
    """Cubre la rama len(arr) == 0 en confidence_interval."""
    mean, ci = confidence_interval([])
    assert np.isnan(mean)
    assert all(np.isnan(c) for c in ci)

def test_plot_heatmap():
    data = np.random.normal(0, 1, (3, 3))
    fig = plot_heatmap(data, ['A','B','C'], ['X','Y','Z'], 'Test Heatmap')
    assert fig is not None

def test_plot_dashboard():
    metrics = {'A': [1,2,3], 'B': [4,5,6]}
    fig = plot_dashboard(metrics)
    assert fig is not None

def test_confidence_interval_len1():
    """Cubre la rama len(arr) == 1 en confidence_interval."""
    datos = [5.0]
    mean, ci = confidence_interval(datos)
    assert mean == 5.0
    assert ci == (5.0, 5.0)

def test_safe_plot_normal():
    """Test safe_plot with normal data."""
    data = {"x": [1,2,3], "y": [4,5,6]}
    fig = safe_plot(data, "Normal Plot")
    assert fig is not None

def test_safe_plot_not_dict():
    """Test safe_plot with not dict."""
    data = [1,2,3]
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_no_x():
    """Test safe_plot without 'x'."""
    data = {"y": [1,2,3]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_no_y():
    """Test safe_plot without 'y'."""
    data = {"x": [1,2,3]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_empty_x():
    """Test safe_plot with empty x."""
    data = {"x": [], "y": [1,2,3]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_empty_y():
    """Test safe_plot with empty y."""
    data = {"x": [1,2,3], "y": []}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_different_len():
    """Test safe_plot with different lengths."""
    data = {"x": [1,2], "y": [1,2,3]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_exception():
    """Test safe_plot with exception."""
    # Mock to raise exception
    import matplotlib.pyplot as plt
    original_plot = plt.plot
    def raise_exc(*args, **kwargs):
        raise ValueError("Test exception")
    plt.plot = raise_exc
    try:
        data = {"x": [1,2,3], "y": [4,5,6]}
        fig = safe_plot(data)
        assert fig is not None
    finally:
        plt.plot = original_plot

def test_t_test():
    """Test t_test."""
    from sim.gui_utils import t_test
    a = [1,2,3]
    b = [4,5,6]
    stat, p = t_test(a, b)
    assert isinstance(stat, float)
    assert isinstance(p, float)

def test_anova():
    """Test anova."""
    from sim.gui_utils import anova
    groups = [[1,2,3], [4,5,6], [7,8,9]]
    stat, p = anova(groups)
    assert isinstance(stat, float)
    assert isinstance(p, float)

def test_scientific_report():
    """Test scientific_report."""
    from sim.gui_utils import scientific_report
    results_A = {
        'flex_recov': [1,2,3],
        'robust_evol': [4,5,6],
        'q_optimal_evol': [7,8,9],
        'total_rewards': [10,11,12],
        'tripwire_steps': [13,14,15]
    }
    results_B = {
        'flex_recov': [2,3,4],
        'robust_evol': [5,6,7],
        'q_optimal_evol': [8,9,10],
        'total_rewards': [11,12,13],
        'tripwire_steps': [14,15,16]
    }
    report = scientific_report(results_A, results_B)
    assert isinstance(report, str)
    assert 'flex_recov' in report
