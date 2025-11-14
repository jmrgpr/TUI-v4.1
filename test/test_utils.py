
"""
Tests de utilidades científicas para TUI v4.1 Toy Model — RL Symbiosis
Scientific utilities tests for TUI v4.1 Toy Model — RL Symbiosis
"""
# Profesional: asegura importación robusta de 'sim'
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.gui_utils import calcular_intervalo_confianza

def test_intervalo_confianza():
    datos = [1, 2, 3, 4, 5]
    mean, ci = calcular_intervalo_confianza(datos)
    assert isinstance(mean, float)
    assert isinstance(ci, tuple)
    assert all(isinstance(x, float) or isinstance(x, np.floating) for x in ci)
