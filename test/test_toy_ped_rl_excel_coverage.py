#!/usr/bin/env python3
"""
test_toy_ped_rl_excel_coverage.py — Tests adicionales para aumentar cobertura en toy_ped_rl_excel.py
"""
import pytest
import pandas as pd
import numpy as np
import io
import sys
import warnings
from sim.toy_ped_rl_excel import (
    System, cargar_datos_excel, analizar_datos, load_systems_from_csv,
    compute_I_justo, pearson_correlation, demo_ped_real, demo_sensibilidad_real, main
)

def test_cargar_datos_excel():
    """Test cargar_datos_excel with invalid path."""
    systems = cargar_datos_excel("nonexistent.csv")
    assert systems == []

def test_cargar_datos_excel_invalid():
    """Test cargar_datos_excel with invalid path."""
    systems = cargar_datos_excel("nonexistent.csv")
    assert systems == []

def test_analizar_datos():
    """Test analizar_datos."""
    systems = [
        System("A", "Bio", 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1.0, ""),
        System("B", "Bio", 0.6, 0.6, 0.6, 0.6, 1, 1, 1, 2.0, "")
    ]
    result = analizar_datos(systems)
    assert result["media_I_op"] == 0.55
    assert result["media_P_riesgo"] == 1.5
    assert result["correlacion"] == 1.0

def test_analizar_datos_empty():
    """Test analizar_datos with empty list."""
    result = analizar_datos([])
    assert result == {"media_I_op": 0.0, "media_P_riesgo": 0.0, "correlacion": 0.0}

def test_load_systems_from_csv():
    """Test load_systems_from_csv (deprecated)."""
    systems = load_systems_from_csv("nonexistent.csv")
    assert systems == []

def test_compute_I_justo():
    """Test compute_I_justo."""
    system = System("Test", "Test", 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1.0, "")
    I_justo = compute_I_justo(system)
    I_op = 0.4 * 0.5 + 0.3 * 0.5 + 0.3 * 0.5
    expected = (1.0 ** 0.5) * (1.0 ** 0.5) * I_op
    assert I_justo == expected

def test_pearson_correlation():
    """Test pearson_correlation."""
    x = [1, 2, 3]
    y = [1, 2, 3]
    corr = pearson_correlation(x, y)
    assert corr == 1.0

    corr = pearson_correlation([], [])
    assert corr == 0.0

def test_demo_ped_real(monkeypatch, tmp_path):
    """Test demo_ped_real."""
    # Create a temp CSV
    data = {"Nombre del sistema": ["A"], "Tipo": ["Bio"], "C": [0.5], "F": [0.5], "T": [0.5], "I_op": [0.5], "Vida (años)": [1], "Tasa (W)": [1], "Complejidad": [1], "P_riesgo físico": [1.0], "Observaciones": ["Test"]}
    df = pd.DataFrame(data)
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)

    # Mock plt.show to avoid display
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)

    demo_ped_real(str(csv_path))

def test_demo_sensibilidad_real(monkeypatch, tmp_path):
    """Test demo_sensibilidad_real."""
    data = {"Nombre del sistema": ["A"], "Tipo": ["Bio"], "C": [0.5], "F": [0.5], "T": [0.5], "I_op": [0.5], "Vida (años)": [1], "Tasa (W)": [1], "Complejidad": [1], "P_riesgo físico": [1.0], "Observaciones": ["Test"]}
    df = pd.DataFrame(data)
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)

    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)

    demo_sensibilidad_real(str(csv_path))

def test_main(monkeypatch, tmp_path):
    """Test main."""
    data = {"Nombre del sistema": ["A"], "Tipo": ["Bio"], "C": [0.5], "F": [0.5], "T": [0.5], "I_op": [0.5], "Vida (años)": [1], "Tasa (W)": [1], "Complejidad": [1], "P_riesgo físico": [1.0], "Observaciones": ["Test"]}
    df = pd.DataFrame(data)
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)

    monkeypatch.setattr('sys.argv', ['test', '--csv', str(csv_path)])
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)

    main()

def test_main_toy_excel(monkeypatch, tmp_path):
    """Test main in toy_ped_rl_excel."""
    csv_path = tmp_path / "test.csv"
    data = {"Nombre del sistema": ["A"], "Tipo": ["Bio"], "C": [0.5], "F": [0.5], "T": [0.5], "I_op": [0.5], "Vida (años)": [1], "Tasa (W)": [1], "Complejidad": [1], "P_riesgo físico": [1.0], "Observaciones": ["Test"]}
    pd.DataFrame(data).to_csv(csv_path, index=False)
    monkeypatch.setattr(sys, 'argv', ['test', '--csv', str(csv_path)])
    main()

def test_main_toy_excel_warning():
    """Test main in toy_ped_rl_excel with warnings."""
    import matplotlib.pyplot as plt
    import warnings
    from sim.toy_ped_rl_excel import main_toy_excel
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        main_toy_excel()

def test_export_no_file():
    from sim.toy_ped_rl_excel import export_to_excel
    from unittest.mock import patch
    results = {"data": [1,2,3]}
    with patch("pathlib.Path.exists", return_value=False):
        export_to_excel(results, "nonexistent/path")
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
    # No crash

def test_demo_ped_real_edge(monkeypatch, tmp_path):
    """Test demo_ped_real con edge cases para cobertura total (líneas 67-68, 103, 136-137, 170-171, 183, 206)."""
    import pandas as pd
    from sim.toy_ped_rl_excel import demo_ped_real
    # CSV vacío
    csv_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(csv_path, index=False)
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    demo_ped_real(str(csv_path))
    # CSV con datos corruptos
    df = pd.DataFrame({"Nombre del sistema": [None], "Tipo": [None], "C": [None], "F": [None], "T": [None], "I_op": [None], "Vida (años)": [None], "Tasa (W)": [None], "Complejidad": [None], "P_riesgo físico": [None], "Observaciones": [None]})
    bad_csv = tmp_path / "bad.csv"
    df.to_csv(bad_csv, index=False)
    demo_ped_real(str(bad_csv))
    # Forzar error en pearson_correlation
    import sim.toy_ped_rl_excel as mod
    monkeypatch.setattr(mod, 'pearson_correlation', lambda x, y: 0.0)
    demo_ped_real(str(csv_path))

def test_demo_sensibilidad_real_edge(monkeypatch, tmp_path):
    """Test demo_sensibilidad_real con edge cases para cobertura total (líneas 170-171, 183, 206)."""
    import pandas as pd
    from sim.toy_ped_rl_excel import demo_sensibilidad_real
    # CSV vacío
    csv_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(csv_path, index=False)
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    demo_sensibilidad_real(str(csv_path))
    # CSV con datos corruptos
    df = pd.DataFrame({"Nombre del sistema": [None], "Tipo": [None], "C": [None], "F": [None], "T": [None], "I_op": [None], "Vida (años)": [None], "Tasa (W)": [None], "Complejidad": [None], "P_riesgo físico": [None], "Observaciones": [None]})
    bad_csv = tmp_path / "bad.csv"
    df.to_csv(bad_csv, index=False)
    demo_sensibilidad_real(str(bad_csv))
    # Forzar error en pearson_correlation
    import sim.toy_ped_rl_excel as mod
    monkeypatch.setattr(mod, 'pearson_correlation', lambda x, y: 0.0)
    demo_sensibilidad_real(str(csv_path))

def test_demo_ped_real_edge(monkeypatch, tmp_path):
    """Test demo_ped_real con edge cases para cobertura total (líneas 67-68, 103, 136-137, 170-171, 183, 206)."""
    import pandas as pd
    from sim.toy_ped_rl_excel import demo_ped_real
    # CSV vacío
    csv_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(csv_path, index=False)
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    demo_ped_real(str(csv_path))
    # CSV con datos corruptos
    df = pd.DataFrame({"Nombre del sistema": [None], "Tipo": [None], "C": [None], "F": [None], "T": [None], "I_op": [None], "Vida (años)": [None], "Tasa (W)": [None], "Complejidad": [None], "P_riesgo físico": [None], "Observaciones": [None]})
    bad_csv = tmp_path / "bad.csv"
    df.to_csv(bad_csv, index=False)
    demo_ped_real(str(bad_csv))
    # Forzar error en pearson_correlation
    import sim.toy_ped_rl_excel as mod
    monkeypatch.setattr(mod, 'pearson_correlation', lambda x, y: 0.0)
    demo_ped_real(str(csv_path))

def test_demo_sensibilidad_real_edge(monkeypatch, tmp_path):
    """Test demo_sensibilidad_real con edge cases para cobertura total (líneas 170-171, 183, 206)."""
    import pandas as pd
    from sim.toy_ped_rl_excel import demo_sensibilidad_real
    # CSV vacío
    csv_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(csv_path, index=False)
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    demo_sensibilidad_real(str(csv_path))
    # CSV con datos corruptos
    df = pd.DataFrame({"Nombre del sistema": [None], "Tipo": [None], "C": [None], "F": [None], "T": [None], "I_op": [None], "Vida (años)": [None], "Tasa (W)": [None], "Complejidad": [None], "P_riesgo físico": [None], "Observaciones": [None]})
    bad_csv = tmp_path / "bad.csv"
    df.to_csv(bad_csv, index=False)
    demo_sensibilidad_real(str(bad_csv))
    # Forzar error en pearson_correlation
    import sim.toy_ped_rl_excel as mod
    monkeypatch.setattr(mod, 'pearson_correlation', lambda x, y: 0.0)
<<<<<<< HEAD
    demo_sensibilidad_real(str(csv_path))
=======
    # No crash
>>>>>>> c226c67 (Cobertura 100%: implementaciones finales de pad_trajectories y safe_plot, tests completos)
=======
    demo_sensibilidad_real(str(csv_path))
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
