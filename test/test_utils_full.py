"""
Tests avanzados para utilidades científicas en TUI v4.1 Toy Model — RL Symbiosis
Advanced tests for scientific utilities in TUI v4.1 Toy Model — RL Symbiosis
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib
matplotlib.use('Agg')  # Hardening: backend sin GUI para tests
import numpy as np
from sim.gui_utils import calcular_intervalo_confianza, confidence_interval, plot_heatmap, plot_dashboard

def test_confidence_interval():
    datos = [1, 2, 3, 4, 5]
    mean, ci = confidence_interval(datos)
    assert isinstance(mean, float)
    assert isinstance(ci, tuple)
    assert all(isinstance(x, float) or isinstance(x, np.floating) for x in ci)

def test_plot_heatmap():
    data = np.random.normal(0, 1, (3, 3))
    fig = plot_heatmap(data, ['A','B','C'], ['X','Y','Z'], 'Test Heatmap')
    assert fig is not None

def test_plot_dashboard():
    metrics = {'A': [1,2,3], 'B': [4,5,6]}
    fig = plot_dashboard(metrics)
    assert fig is not None
