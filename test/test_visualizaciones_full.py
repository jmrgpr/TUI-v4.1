"""
Tests para todas las funciones de visualización en TUI v4.1 Toy Model — RL Symbiosis
Tests for all visualization functions in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.visualizaciones import curva_riesgo_comparativa, boxplot_metricas, heatmap_metricas

def test_curva_riesgo_comparativa():
    control = np.random.normal(0, 1, (5, 10))
    simbiosis = np.random.normal(1, 1, (5, 10))
    curva_riesgo_comparativa(control, simbiosis, export_path=None)

def test_boxplot_metricas():
    datos1 = np.random.normal(0, 1, 10)
    datos2 = np.random.normal(1, 1, 10)
    boxplot_metricas(datos1, datos2, 'Flexibilidad', export_path=None)

def test_heatmap_metricas():
    matriz = np.random.normal(0, 1, (3, 3))
    etiquetas = {'x': ['A','B','C'], 'y': ['X','Y','Z']}
    heatmap_metricas(matriz, etiquetas, 'Robustez', export_path=None)
