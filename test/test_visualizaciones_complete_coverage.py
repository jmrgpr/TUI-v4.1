#!/usr/bin/env python3
"""
test_visualizaciones_complete_coverage.py — Tests exhaustivos para cubrir 100% de visualizaciones.py
"""
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para tests
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import os
from sim.visualizaciones import (
    plot_risk_curve, boxplot_metricas, boxplot_metricas_profesional,
    heatmap_metricas, heatmap_metricas_profesional, dashboard_metricas,
    exportar_metricas, curva_riesgo_comparativa, analisis_estadistico,
    dashboard_metricas as dashboard_metricas_profesional
)

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def sample_data_2d():
    return np.random.rand(5, 5)

@pytest.fixture
def tmp_path_fixture(tmp_path):
    return tmp_path

def test_plot_risk_curve_empty():
    """Test plot_risk_curve with empty data."""
    plot_risk_curve([], show=False)
    # Should not raise error

def test_plot_risk_curve_normal(sample_data):
    """Test plot_risk_curve with normal data."""
    plot_risk_curve(sample_data, show=False)

def test_plot_risk_curve_empty_specific():
    """Test plot_risk_curve empty branch."""
    plot_risk_curve([], title="Test", show=False)

def test_boxplot_metricas_empty():
    """Test boxplot_metricas with empty data."""
    boxplot_metricas([], show=False)

def test_boxplot_metricas_normal():
    """Test boxplot_metricas with normal data."""
    data = [[1, 2, 3], [4, 5, 6]]
    boxplot_metricas(data, labels=['A', 'B'], show=False)

def test_boxplot_metricas_redirect():
    """Test boxplot_metricas redirect to professional."""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        export_path = f.name
    boxplot_metricas([1, 2, 3], [4, 5, 6], 'Test', export_path=export_path)
    assert os.path.exists(export_path)
    os.unlink(export_path)

def test_boxplot_metricas_redirect_condition():
    """Test boxplot_metricas redirect condition."""
    # This should trigger the redirect
    boxplot_metricas([1], [2], 'Test', export_path='dummy.png')

def test_boxplot_metricas_simple():
    """Test boxplot_metricas simple version."""
    boxplot_metricas([[1,2,3]], labels=['Test'], show=False)

def test_boxplot_metricas_profesional_empty():
    """Test boxplot_metricas_profesional with empty data."""
    boxplot_metricas_profesional([], [1, 2, 3], 'Test')

def test_boxplot_metricas_profesional_normal():
    """Test boxplot_metricas_profesional with normal data."""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        export_path = f.name
    boxplot_metricas_profesional([1, 2, 3], [4, 5, 6], 'Test', export_path=export_path)
    assert os.path.exists(export_path)
    os.unlink(export_path)

def test_boxplot_metricas_profesional_empty_print(capsys):
    """Cubre el print de datos vacíos en boxplot_metricas_profesional."""
    from sim.visualizaciones import boxplot_metricas_profesional
    boxplot_metricas_profesional([], [], 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_boxplot_metricas_labels_fallback(monkeypatch):
    """Cubre el fallback a labels en boxplot_metricas (línea 95)."""
    from sim.visualizaciones import boxplot_metricas
    import matplotlib.pyplot as plt
    called = {'tick': 0, 'labels': 0}
    def fake_boxplot(data, **kwargs):
        if 'tick_labels' in kwargs:
            called['tick'] += 1
            raise TypeError('tick_labels no soportado')
        if 'labels' in kwargs:
            called['labels'] += 1
            return None
    monkeypatch.setattr(plt, 'boxplot', fake_boxplot)
    boxplot_metricas([[1,2,3]], labels=['Test'], show=False)
    assert called['tick'] == 1 and called['labels'] == 1

def test_boxplot_metricas_labels_fallback_real(monkeypatch):
    """Cubre el fallback real de labels en boxplot_metricas simulando matplotlib antiguo."""
    from sim.visualizaciones import boxplot_metricas
    import matplotlib.pyplot as plt
    called = {'labels': 0}
    def fake_boxplot(data, **kwargs):
        # Simula matplotlib antiguo: solo acepta 'labels', rechaza 'tick_labels'
        if 'tick_labels' in kwargs:
            raise TypeError('tick_labels no soportado')
        if 'labels' in kwargs:
            called['labels'] += 1
            return None
        raise TypeError('Argumento no soportado')
    monkeypatch.setattr(plt, 'boxplot', fake_boxplot)
    boxplot_metricas([[1,2,3]], labels=['Test'], show=False)
    assert called['labels'] == 1
def test_heatmap_metricas_empty():
    """Test heatmap_metricas with empty data."""
    heatmap_metricas([], show=False)

def test_heatmap_metricas_normal(sample_data_2d):
    """Test heatmap_metricas with normal data."""
    heatmap_metricas(sample_data_2d, show=False)

def test_heatmap_metricas_redirect():
    """Test heatmap_metricas redirect to professional."""
    matriz = np.random.rand(3, 3)
    etiquetas = {'x': ['A', 'B', 'C'], 'y': ['1', '2', '3']}
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        export_path = f.name
    heatmap_metricas(matriz, etiquetas, 'Test', export_path=export_path)
    assert os.path.exists(export_path)
    os.unlink(export_path)

def test_heatmap_metricas_redirect_condition():
    """Test heatmap_metricas redirect condition."""
    heatmap_metricas(np.array([[1,2],[3,4]]), {'x':['a','b'], 'y':['1','2']}, 'Test', export_path='dummy.png')

def test_heatmap_metricas_simple():
    """Test heatmap_metricas simple version."""
    heatmap_metricas([[1,2],[3,4]], title="Test", show=False)

def test_heatmap_metricas_profesional_empty():
    """Test heatmap_metricas_profesional with empty matrix."""
    heatmap_metricas_profesional(np.array([]), {'x': [], 'y': []}, 'Test')

def test_heatmap_metricas_profesional_normal():
    """Test heatmap_metricas_profesional with normal data."""
    matriz = np.random.rand(3, 3)
    etiquetas = {'x': ['A', 'B', 'C'], 'y': ['1', '2', '3']}
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        export_path = f.name
    heatmap_metricas_profesional(matriz, etiquetas, 'Test', export_path=export_path)
    assert os.path.exists(export_path)
    os.unlink(export_path)

def test_heatmap_metricas_profesional_empty_print(capsys):
    """Cubre el print de datos vacíos en heatmap_metricas_profesional."""
    from sim.visualizaciones import heatmap_metricas_profesional
    import numpy as np
    heatmap_metricas_profesional(np.array([]), {'x': [], 'y': []}, 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out

def test_dashboard_metricas_empty(capsys):
    """Test dashboard_metricas (professional) with empty dict."""
    dashboard_metricas({})
    captured = capsys.readouterr()
    assert "Dashboard de métricas agregadas" in captured.out
    assert "Sin datos" in captured.out

def test_dashboard_metricas_normal():
    """Test dashboard_metricas (alias) with data."""
    data = {'Agente': {'Metrica': 1.0}}
    dashboard_metricas(data)

def test_dashboard_metricas_alias():
    """Test dashboard_metricas alias."""
    data = {'Control': {'test': [1, 2, 3]}}
    dashboard_metricas(data)

def test_exportar_metricas(tmp_path_fixture):
    """Test exportar_metricas."""
    data = {'test': 1}
    filename = tmp_path_fixture / "test.json"
    exportar_metricas(data, filename=str(filename))
    assert filename.exists()

def test_curva_riesgo_comparativa_empty():
    """Test curva_riesgo_comparativa with empty arrays."""
    curva_riesgo_comparativa(np.array([]), np.array([1, 2, 3]))

def test_curva_riesgo_comparativa_empty_control():
    """Test curva_riesgo_comparativa empty control."""
    curva_riesgo_comparativa(np.array([]), np.array([[1,2,3]]))

def test_curva_riesgo_comparativa_empty_simbiosis():
    """Test curva_riesgo_comparativa empty simbiosis."""
    curva_riesgo_comparativa(np.array([[1,2,3]]), np.array([]))

def test_curva_riesgo_comparativa_normal():
    """Test curva_riesgo_comparativa with normal data."""
    control = np.random.rand(10, 50)
    simbiosis = np.random.rand(10, 50)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        export_path = f.name
    curva_riesgo_comparativa(control, simbiosis, export_path=export_path)
    assert os.path.exists(export_path)
    os.unlink(export_path)

def test_curva_riesgo_comparativa_no_export():
    """Test curva_riesgo_comparativa with normal data and no export_path to cover plt.close()."""
    control = np.random.rand(10, 50)
    simbiosis = np.random.rand(10, 50)
    curva_riesgo_comparativa(control, simbiosis, export_path=None)

def test_curva_riesgo_comparativa_empty_print(capsys):
    """Cubre el print de datos vacíos en curva_riesgo_comparativa."""
    from sim.visualizaciones import curva_riesgo_comparativa
    import numpy as np
    curva_riesgo_comparativa(np.array([]), np.array([]))
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out

def test_analisis_estadistico(capsys):
    """Test analisis_estadistico."""
    control = [1, 2, 3, 4, 5]
    simbiosis = [2, 3, 4, 5, 6]
    analisis_estadistico(control, simbiosis, 'Test')
    captured = capsys.readouterr()
    assert 't-test' in captured.out

def test_dashboard_metricas_profesional_empty(tmp_path_fixture, capsys):
    """Test dashboard_metricas (professional) with empty dict."""
    dashboard_metricas_profesional({}, export_path=str(tmp_path_fixture / "empty.json"))
    captured = capsys.readouterr()
    assert "Sin datos" in captured.out
    assert "Interpretación bilingüe" in captured.out

def test_dashboard_metricas_profesional_normal(tmp_path_fixture, capsys):
    """Test dashboard_metricas (professional) with data."""
    data = {
        'Control': {'Flexibilidad': [1, 2, 3], 'Robustez': [4, 5, 6]},
        'Simbiosis': {'Flexibilidad': [2, 3, 4], 'Robustez': [5, 6, 7]}
    }
    dashboard_metricas_profesional(data, export_path=str(tmp_path_fixture / "dashboard.json"))
    captured = capsys.readouterr()
    assert "Dashboard" in captured.out
    assert "Interpretación bilingüe" in captured.out
    assert "Control" in captured.out
    assert "Simbiosis" in captured.out

def test_dashboard_metricas_profesional_export_csv(tmp_path_fixture):
    """Test dashboard_metricas export to CSV to cover the CSV writing loop."""
    data = {
        'Control': {'Flexibilidad': [1, 2, 3]},
    }
    export_path = str(tmp_path_fixture / "dashboard.csv")
    dashboard_metricas_profesional(data, export_path=export_path)
    assert tmp_path_fixture.joinpath("dashboard.csv").exists()

def test_plot_risk_curve_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() de plot_risk_curve."""
    from sim.visualizaciones import plot_risk_curve
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    plot_risk_curve([1,2,3], show=True)  # No debe lanzar error

def test_boxplot_metricas_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() de boxplot_metricas."""
    from sim.visualizaciones import boxplot_metricas
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    boxplot_metricas([[1,2,3]], labels=['Test'], show=True)

def test_heatmap_metricas_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() de heatmap_metricas."""
    from sim.visualizaciones import heatmap_metricas
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    heatmap_metricas([[1,2],[3,4]], title="Test", show=True)

def test_plot_risk_curve_empty_branch_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() cuando data está vacía en plot_risk_curve."""
    from sim.visualizaciones import plot_risk_curve
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    plot_risk_curve([], show=True)


def test_boxplot_metricas_empty_branch_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() cuando data está vacía en boxplot_metricas."""
    from sim.visualizaciones import boxplot_metricas
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    boxplot_metricas([], show=True)


def test_heatmap_metricas_empty_branch_show_exception(monkeypatch):
    """Cubre el except Exception en plt.show() cuando data está vacía en heatmap_metricas."""
    from sim.visualizaciones import heatmap_metricas
    import matplotlib.pyplot as plt
    def raise_exception(*args, **kwargs):
        raise RuntimeError('Forzado')
    monkeypatch.setattr(plt, 'show', raise_exception)
    heatmap_metricas([], show=True)


def test_boxplot_metricas_profesional_empty_print_full(capsys):
    """Cubre el print de datos vacíos en boxplot_metricas_profesional (ambos arrays vacíos)."""
    from sim.visualizaciones import boxplot_metricas_profesional
    boxplot_metricas_profesional([], [], 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_boxplot_metricas_profesional_empty_control_print(capsys):
    """Cubre el print de datos vacíos en boxplot_metricas_profesional (solo control vacío)."""
    from sim.visualizaciones import boxplot_metricas_profesional
    boxplot_metricas_profesional([], [1,2,3], 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_boxplot_metricas_profesional_empty_simbiosis_print(capsys):
    """Cubre el print de datos vacíos en boxplot_metricas_profesional (solo simbiosis vacío)."""
    from sim.visualizaciones import boxplot_metricas_profesional
    boxplot_metricas_profesional([1,2,3], [], 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_heatmap_metricas_profesional_empty_matrix_print(capsys):
    """Cubre el print de matriz vacía en heatmap_metricas_profesional."""
    from sim.visualizaciones import heatmap_metricas_profesional
    import numpy as np
    heatmap_metricas_profesional(np.array([]), {'x': ['A'], 'y': ['B']}, 'Test')
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_curva_riesgo_comparativa_empty_control_print(capsys):
    """Cubre el print de array control vacío en curva_riesgo_comparativa."""
    from sim.visualizaciones import curva_riesgo_comparativa
    import numpy as np
    curva_riesgo_comparativa(np.array([]), np.array([[1,2,3]]))
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_curva_riesgo_comparativa_empty_simbiosis_print(capsys):
    """Cubre el print de array simbiosis vacío en curva_riesgo_comparativa."""
    from sim.visualizaciones import curva_riesgo_comparativa
    import numpy as np
    curva_riesgo_comparativa(np.array([[1,2,3]]), np.array([]))
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_dashboard_metricas_empty_print(capsys):
    """Cubre el print de dashboard_metricas con dict vacío."""
    from sim.visualizaciones import dashboard_metricas
    dashboard_metricas({})
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out


def test_dashboard_metricas_empty_export_print(tmp_path_fixture, capsys):
    """Cubre el print de dashboard_metricas con dict vacío y export_path CSV/JSON."""
    from sim.visualizaciones import dashboard_metricas
    import os
    export_csv = str(tmp_path_fixture / "empty.csv")
    export_json = str(tmp_path_fixture / "empty.json")
    dashboard_metricas({}, export_path=export_csv)
    dashboard_metricas({}, export_path=export_json)
    captured = capsys.readouterr()
    assert 'Sin datos' in captured.out
    assert os.path.exists(export_csv)
    assert os.path.exists(export_json)

def test_dashboard_metricas_empty_agg_print(capsys):
    """Cubre el print de dashboard_metricas (agg) con dict vacío y export_path None."""
    from sim.visualizaciones import dashboard_metricas
    dashboard_metricas({}, export_path=None)
    captured = capsys.readouterr()
    assert 'Dashboard' in captured.out or 'dashboard' in captured.out


def test_dashboard_metricas_empty_agg_export_csv_json(tmp_path_fixture):
    """Cubre la exportación CSV/JSON con dict vacío en dashboard_metricas (agg)."""
    from sim.visualizaciones import dashboard_metricas
    import os
    export_csv = str(tmp_path_fixture / "empty_agg.csv")
    export_json = str(tmp_path_fixture / "empty_agg.json")
    dashboard_metricas({}, export_path=export_csv)
    dashboard_metricas({}, export_path=export_json)
    assert os.path.exists(export_csv)
    assert os.path.exists(export_json)

def test_dashboard_metricas_profesional_len1_ci(capsys, tmp_path_fixture):
    """Cubre la rama else en CI cuando len(arr) == 1."""
    from sim.visualizaciones import dashboard_metricas
    data = {
        'Control': {'Flexibilidad': [1.0]},  # len=1, cubre else en CI
    }
    dashboard_metricas(data, export_path=str(tmp_path_fixture / "len1.json"))
    captured = capsys.readouterr()
    assert 'media=1.00' in captured.out

def test_dashboard_metricas_profesional_with_nans(capsys, tmp_path_fixture):
    """Cubre el filtro de NaNs en dashboard_metricas."""
    from sim.visualizaciones import dashboard_metricas
    import numpy as np
    data = {
        'Control': {'Flexibilidad': [1.0, np.nan, 3.0]},  # Tiene NaN, cubre arr = arr[~np.isnan(arr)]
    }
    dashboard_metricas(data, export_path=str(tmp_path_fixture / "nans.json"))
    captured = capsys.readouterr()
    assert 'media=2.00' in captured.out  # (1+3)/2 = 2


def test_boxplot_metricas_prints_full(capsys):
    """Cubre todos los prints y ramas de boxplot_metricas y boxplot_metricas_profesional."""
    from sim.visualizaciones import boxplot_metricas, boxplot_metricas_profesional
    # Data vacío
    boxplot_metricas([], show=False)
    captured = capsys.readouterr()
    # Data normal
    boxplot_metricas([[1,2,3],[4,5,6]], labels=['A','B'], show=False)
    # Profesional vacío
    boxplot_metricas_profesional([], [], 'Test')
    captured = capsys.readouterr()
    assert "Sin datos" in captured.out
    # Profesional normal
    boxplot_metricas_profesional([1,2,3], [4,5,6], 'Test')


def test_heatmap_metricas_prints_full(capsys):
    """Cubre todos los prints y ramas de heatmap_metricas y heatmap_metricas_profesional."""
    from sim.visualizaciones import heatmap_metricas, heatmap_metricas_profesional
    import numpy as np
    # Data vacío
    heatmap_metricas([], show=False)
    captured = capsys.readouterr()
    # Data normal
    heatmap_metricas(np.array([[1,2],[3,4]]), show=False)
    # Profesional vacío
    heatmap_metricas_profesional(np.array([]), {'x': [], 'y': []}, 'Test')
    captured = capsys.readouterr()
    assert "Sin datos" in captured.out
    # Profesional normal
    heatmap_metricas_profesional(np.array([[1,2],[3,4]]), {'x': ['A','B'], 'y': ['1','2']}, 'Test')


def test_dashboard_metricas_loop_prints(capsys):
    """Cubre los prints del loop en dashboard_metricas con múltiples agentes y métricas."""
    from sim.visualizaciones import dashboard_metricas
    data = {
        'Control': {'Flexibilidad': [1, 2, 3], 'Robustez': [4, 5, 6]},
        'Simbiosis': {'Flexibilidad': [2, 3, 4], 'Robustez': [5, 6, 7]},
        'OtroAgente': {'MétricaExtra': [8, 9, 10]}
    }
    dashboard_metricas(data)
    captured = capsys.readouterr()
    assert 'Control' in captured.out
    assert 'Simbiosis' in captured.out
    assert 'OtroAgente' in captured.out
    assert 'Flexibilidad' in captured.out
    assert 'Robustez' in captured.out
    assert 'MétricaExtra' in captured.out

def test_boxplot_metricas_labels_fallback(monkeypatch):
    """Cubre el except TypeError en boxplot_metricas para labels fallback."""
    from sim.visualizaciones import boxplot_metricas
    import matplotlib.pyplot as plt
    original_boxplot = plt.boxplot
    def mock_boxplot(*args, **kwargs):
        if 'tick_labels' in kwargs:
            raise TypeError("tick_labels not supported")
        return original_boxplot(*args, **kwargs)
    monkeypatch.setattr(plt, 'boxplot', mock_boxplot)
    boxplot_metricas([[1,2,3]], labels=['Test'], show=False)

def test_plot_risk_curve_empty_show():
    """Test plot_risk_curve with empty data and show=True to cover if show branch."""
    plot_risk_curve([], show=True)

def test_boxplot_metricas_empty_show():
    """Test boxplot_metricas with empty data and show=True."""
    boxplot_metricas([], show=True)

def test_heatmap_metricas_empty_show():
    """Test heatmap_metricas with empty data and show=True."""
    heatmap_metricas([], show=True)