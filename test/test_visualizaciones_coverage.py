"""
Tests adicionales para aumentar cobertura de visualizaciones.py
Additional tests to increase coverage of visualizaciones.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para tests

import numpy as np
from sim.visualizaciones import plot_risk_curve, boxplot_metricas_profesional, heatmap_metricas_profesional, curva_riesgo_comparativa, analisis_estadistico

def test_plot_risk_curve_empty_data():
    plot_risk_curve([], title="Empty", show=False)

def test_boxplot_metricas_profesional_empty():
    boxplot_metricas_profesional([], [], 'Test', export_path=None)

def test_heatmap_metricas_profesional_empty():
    etiquetas = {'x': ['A'], 'y': ['B']}
    heatmap_metricas_profesional(np.zeros((0,0)), etiquetas, 'Test', export_path=None)

def test_curva_riesgo_comparativa_empty():
    curva_riesgo_comparativa(np.zeros((0,10)), np.zeros((0,10)), export_path=None)

def test_analisis_estadistico():
    analisis_estadistico([1,2,3], [4,5,6], 'Test')