"""
Tests de utilidades científicas para TUI v4.1 Toy Model — RL Symbiosis
Scientific utilities tests for TUI v4.1 Toy Model — RL Symbiosis
"""
from sim.gui_utils import calcular_intervalo_confianza

def test_intervalo_confianza():
    datos = [1, 2, 3, 4, 5]
    mean, ci = calcular_intervalo_confianza(datos)
    assert isinstance(mean, float)
    assert isinstance(ci, float)
