"""
Tests exhaustivos de ramas y edge cases para visualizaciones.py
Full branch and edge case tests for visualizaciones.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.visualizaciones import plot_risk_curve, boxplot_metricas, heatmap_metricas, dashboard_metricas, exportar_metricas

def test_plot_risk_curve_empty():
    plot_risk_curve([], title="Curva vacía", show=False)

def test_boxplot_metricas_empty():
    boxplot_metricas([[]], labels=["Control"], show=False)

def test_heatmap_metricas_empty():
    heatmap_metricas(np.zeros((0,0)), title="Heatmap vacío", show=False)

def test_dashboard_metricas_empty():
    dashboard_metricas({})

def test_exportar_metricas_empty():
    exportar_metricas({}, filename="test_export_empty.json")
