"""
Tests de visualizaciones para TUI v4.1 Toy Model — RL Symbiosis
Visualization tests for TUI v4.1 Toy Model — RL Symbiosis
"""
# Profesional: asegura importación robusta de 'sim'
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configurar matplotlib para backend no interactivo
import matplotlib
matplotlib.use('Agg')

from sim.visualizaciones import boxplot_metricas, heatmap_metricas, curva_riesgo_comparativa, analisis_estadistico, dashboard_metricas, heatmap_metricas_profesional, boxplot_metricas_profesional
import numpy as np

def test_boxplot_metricas():
    # Test simple version
    datos1 = np.random.normal(0, 1, 10)
    datos2 = np.random.normal(1, 1, 10)
    try:
        boxplot_metricas(datos1, datos2, 'Test', export_path=None)
    except Exception:
        assert False, "boxplot_metricas debe ejecutarse sin error"
    
    # Test with empty data
    try:
        boxplot_metricas([], [], 'Empty', export_path=None)
    except Exception:
        assert False, "boxplot_metricas empty debe ejecutarse sin error"
    
    # Direct test for boxplot_metricas_profesional
    try:
        boxplot_metricas_profesional(datos1, datos2, 'Test', export_path=None)
    except Exception:
        assert False, "boxplot_metricas_profesional debe ejecutarse sin error"

def test_heatmap_metricas():
    # Test simple version
    data = np.random.rand(5, 5)
    try:
        heatmap_metricas(data, title="Test Heatmap", show=False)
    except Exception:
        assert False, "heatmap_metricas simple debe ejecutarse sin error"
    
    # Test simple version with empty data
    try:
        heatmap_metricas(np.array([]), title="Empty Heatmap", show=False)
    except Exception:
        assert False, "heatmap_metricas empty debe ejecutarse sin error"
    
    # Test professional version to cover heatmap_metricas_profesional
    matriz = np.random.rand(3, 3)
    etiquetas = {'x': ['A', 'B', 'C'], 'y': ['1', '2', '3']}
    try:
        heatmap_metricas(matriz, etiquetas, 'Test Heatmap', export_path=None)
    except Exception:
        assert False, "heatmap_metricas profesional debe ejecutarse sin error"
    
    # Direct test for heatmap_metricas_profesional
    try:
        heatmap_metricas_profesional(matriz, etiquetas, 'Test Heatmap', export_path=None)
    except Exception:
        assert False, "heatmap_metricas_profesional debe ejecutarse sin error"

def test_curva_riesgo_comparativa():
    riesgo_control = np.random.rand(10, 20)
    riesgo_simbiosis = np.random.rand(10, 20)
    try:
        curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path=None)
    except Exception:
        assert False, "curva_riesgo_comparativa debe ejecutarse sin error"

def test_analisis_estadistico():
    metricas_control = np.random.normal(0, 1, 10)
    metricas_simbiosis = np.random.normal(1, 1, 10)
    try:
        analisis_estadistico(metricas_control, metricas_simbiosis, 'Test')
    except Exception:
        assert False, "analisis_estadistico debe ejecutarse sin error"

def test_dashboard_metricas():
    metricas_dict = {
        'Control': {'Flexibilidad': np.random.normal(0, 1, 10), 'Eficiencia': np.random.normal(1, 1, 10)},
        'Simbiosis': {'Flexibilidad': np.random.normal(0.5, 1, 10), 'Eficiencia': np.random.normal(1.5, 1, 10)}
    }
    try:
        dashboard_metricas(metricas_dict, export_path=None)
    except Exception:
        assert False, "dashboard_metricas debe ejecutarse sin error"
    
    # Test with empty dict
    try:
        dashboard_metricas({}, export_path=None)
    except Exception:
        assert False, "dashboard_metricas empty debe ejecutarse sin error"
    
    # Test with export
    try:
        dashboard_metricas(metricas_dict, export_path='test.csv')
    except Exception:
        assert False, "dashboard_metricas csv debe ejecutarse sin error"
    
    try:
        dashboard_metricas(metricas_dict, export_path='test.json')
    except Exception:
        assert False, "dashboard_metricas json debe ejecutarse sin error"
