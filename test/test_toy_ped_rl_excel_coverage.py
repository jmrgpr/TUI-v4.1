#!/usr/bin/env python3
"""
test_toy_ped_rl_excel_coverage.py — Tests adicionales para aumentar cobertura en toy_ped_rl_excel.py
"""
import pytest
import pandas as pd
import numpy as np
import io
import sys
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