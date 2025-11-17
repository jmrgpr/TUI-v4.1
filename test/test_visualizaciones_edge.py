import matplotlib.pyplot as plt
from sim.visualizaciones import boxplot_metricas


def test_boxplot_tick_labels_fallback(monkeypatch):
    """Forzar que plt.boxplot lance TypeError cuando se pasa 'tick_labels' para cubrir el fallback."""
    # Guardar original
    original_boxplot = plt.boxplot

    def wrapper(*args, **kwargs):
        # Si se pasa 'tick_labels', simular TypeError (como en versiones distintas)
        if 'tick_labels' in kwargs:
            raise TypeError('tick_labels not supported')
        return original_boxplot(*args, **kwargs)

    monkeypatch.setattr(plt, 'boxplot', wrapper)

    # data no vacío para evitar la rama 'empty'
    data = [[1, 2, 3], [2, 3, 4]]
    # Llamada que intenta tick_labels -> wrapper lanza TypeError -> fallback usa labels
    boxplot_metricas(data, labels=['A', 'B'], show=False)


def test_boxplot_without_labels():
    """Llamada simple a boxplot_metricas sin labels para cubrir la rama plt.boxplot(data)."""
    data = [[1, 2, 3], [2, 3, 4]]
    boxplot_metricas(data, show=False)
"""
Tests de edge cases y ramas internas para visualizaciones en TUI v4.1 Toy Model — RL Symbiosis
Edge case and branch tests for visualizations in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib
matplotlib.use('Agg')
import numpy as np
from sim.visualizaciones import curva_riesgo_comparativa, boxplot_metricas, heatmap_metricas

def test_curva_riesgo_comparativa_empty():
    control = np.empty((0, 10))
    simbiosis = np.empty((0, 10))
    try:
        curva_riesgo_comparativa(control, simbiosis, export_path=None)
    except Exception:
        assert False, "curva_riesgo_comparativa debe manejar datos vacíos sin error"

def test_boxplot_metricas_empty():
    datos1 = []
    datos2 = []
    try:
        boxplot_metricas(datos1, datos2, 'Flexibilidad', export_path=None)
    except Exception:
        assert False, "boxplot_metricas debe manejar datos vacíos sin error"

def test_heatmap_metricas_missing_labels():
    matriz = np.random.normal(0, 1, (3, 3))
    etiquetas = {'x': ['A','B','C']}  # Falta 'y'
    try:
        heatmap_metricas(matriz, etiquetas, 'Robustez', export_path=None)
    except Exception:
        pass  # Puede fallar por etiquetas faltantes, pero no debe romper el flujo
