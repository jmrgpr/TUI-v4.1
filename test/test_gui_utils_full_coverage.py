#!/usr/bin/env python3
"""
test_gui_utils_full_coverage.py — Tests exhaustivos para cobertura total de gui_utils.py
"""
import pytest
import numpy as np
from sim.gui_utils import safe_plot, plot_heatmap, plot_dashboard, scientific_report, confidence_interval
import matplotlib.pyplot as plt


def test_safe_plot_invalid_dict():
    fig = safe_plot({'x': [], 'y': []})
    assert fig is not None

def test_safe_plot_invalid_structure():
    fig = safe_plot({'a': [1], 'b': [2]})
    assert fig is not None

def test_safe_plot_insufficient_data():
    fig = safe_plot({'x': [1], 'y': []})
    assert fig is not None

def test_safe_plot_plotting_error(monkeypatch):
    class BadArray:
        def __len__(self): return 1
        def __iter__(self): raise RuntimeError('Forzado')
    data = {'x': BadArray(), 'y': BadArray()}
    fig = safe_plot(data)
    assert fig is not None
def test_safe_plot_plot_method_error(monkeypatch):
    # Simula datos válidos pero el método plot falla
    def bad_plot(*args, **kwargs):
        raise RuntimeError('Error forzado en plot')
    monkeypatch.setattr('matplotlib.axes.Axes.plot', bad_plot)
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_backend_error(monkeypatch):
    # Simula error en matplotlib.use para cubrir el branch final del except
    import matplotlib
    original_use = matplotlib.use
    def bad_use(*args, **kwargs):
        raise RuntimeError('Error forzado en backend')
    monkeypatch.setattr(matplotlib, 'use', bad_use)
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    fig = safe_plot(data)
    assert fig is not None
    # Restaurar función original para evitar efectos colaterales
    matplotlib.use = original_use
    def bad_use(*args, **kwargs):
        raise RuntimeError('Error forzado en backend')
    monkeypatch.setattr(matplotlib, 'use', bad_use)
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    fig = safe_plot(data)
    assert fig is not None

def test_safe_plot_backend_error(monkeypatch):
    # Simula error en matplotlib.use para cubrir el branch final del except
    import matplotlib
    original_use = matplotlib.use
    def bad_use(*args, **kwargs):
        raise RuntimeError('Error forzado en backend')
    monkeypatch.setattr(matplotlib, 'use', bad_use)
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    fig = safe_plot(data)
    assert fig is not None
    # Restaurar función original para evitar efectos colaterales
    matplotlib.use = original_use
    # Restaurar función original para evitar efectos colaterales
    matplotlib.use = original_use
    # Simula datos válidos pero el método plot falla
    def bad_plot(*args, **kwargs):
        raise RuntimeError('Error forzado en plot')
    monkeypatch.setattr('matplotlib.axes.Axes.plot', bad_plot)
    data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    fig = safe_plot(data)
    assert fig is not None

def test_plot_heatmap_normal():
    data = np.array([[1,2],[3,4]])
    fig = plot_heatmap(data, ['A','B'], ['X','Y'], 'Test')
    assert fig is not None

def test_plot_heatmap_empty():
    from sim.gui_utils import plot_heatmap
    fig = plot_heatmap(np.array([]), [], [], 'Empty')
    assert fig is not None

def test_plot_dashboard_normal():
    metrics = {'A': [1,2], 'B': [3,4]}
    fig = plot_dashboard(metrics)
    assert fig is not None

def test_plot_dashboard_empty():
    from sim.gui_utils import plot_dashboard
    fig = plot_dashboard({})
    assert fig is not None

def test_confidence_interval_len1():
    mean, ci = confidence_interval([42])
    assert mean == 42
    assert ci == (42, 42)

def test_confidence_interval_aliases():
    from sim.gui_utils import confidence_interval, calcular_intervalo_confianza
    data = [1, 2, 3]
    mean1, ci1 = confidence_interval(data)
    mean2, ci2 = calcular_intervalo_confianza(data)
    assert mean1 == mean2
    assert ci1 == ci2

def test_scientific_report_full():
    results_A = {
        'flex_recov': [1,2,3],
        'robust_evol': [2,3,4],
        'q_optimal_evol': [3,4,5],
        'total_rewards': [4,5,6],
        'tripwire_steps': [5,6,7]
    }
    results_B = {
        'flex_recov': [2,3,4],
        'robust_evol': [3,4,5],
        'q_optimal_evol': [4,5,6],
        'total_rewards': [5,6,7],
        'tripwire_steps': [6,7,8]
    }
    report = scientific_report(results_A, results_B)
    assert 't-test' in report
    assert 'ANOVA' in report

def test_confidence_interval_empty():
    from sim.gui_utils import confidence_interval, calcular_intervalo_confianza
    mean, ci = confidence_interval([])
    assert np.isnan(mean)
    assert np.isnan(ci[0]) and np.isnan(ci[1])
    mean_es, ci_es = calcular_intervalo_confianza([])
    assert np.isnan(mean_es)
    assert np.isnan(ci_es[0]) and np.isnan(ci_es[1])

def test_confidence_interval_nan():
    from sim.gui_utils import confidence_interval
    mean, ci = confidence_interval([np.nan, np.nan])
    assert np.isnan(mean)
    assert np.isnan(ci[0]) and np.isnan(ci[1])

def test_t_test_and_anova():
    from sim.gui_utils import t_test, anova
    a = [1, 2, 3]
    b = [2, 3, 4]
    stat_t, p_t = t_test(a, b)
    stat_a, p_a = anova([a, b])
    assert isinstance(stat_t, float)
    assert isinstance(p_t, float)
    assert isinstance(stat_a, float)
    assert isinstance(p_a, float)

def test_scientific_report_edge():
    from sim.gui_utils import scientific_report
    results_A = {
        'flex_recov': [np.nan],
        'robust_evol': [np.nan],
        'q_optimal_evol': [np.nan],
        'total_rewards': [np.nan],
        'tripwire_steps': [np.nan]
    }
    results_B = {
        'flex_recov': [np.nan],
        'robust_evol': [np.nan],
        'q_optimal_evol': [np.nan],
        'total_rewards': [np.nan],
        'tripwire_steps': [np.nan]
    }
    report = scientific_report(results_A, results_B)
    assert 'significant' in report
    assert 'significant' in report
