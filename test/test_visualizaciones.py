"""
Tests de visualizaciones para TUI v4.1 Toy Model — RL Symbiosis
Visualization tests for TUI v4.1 Toy Model — RL Symbiosis
"""
# Profesional: asegura importación robusta de 'sim'
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.visualizaciones import boxplot_metricas
import numpy as np

def test_boxplot_metricas():
    datos1 = np.random.normal(0, 1, 10)
    datos2 = np.random.normal(1, 1, 10)
    try:
        boxplot_metricas(datos1, datos2, 'Test', export_path=None)
    except Exception:
        assert False, "boxplot_metricas debe ejecutarse sin error"
