"""
Test rápido y robusto para cobertura de toy_ped_rl_excel.py sin bloqueos ni procesamiento masivo de gráficos.
"""
import pytest
from sim.toy_ped_rl_excel import demo_ped_real, demo_sensibilidad_real, System
import matplotlib.pyplot as plt

@pytest.fixture
def small_systems():
    # Datos mínimos y representativos para test
    return [
        System(name="A", tipo="bio", C=0.1, F=0.2, T=0.3, I_op=0.4, vida=1, tasa=1, complejidad=1, P_riesgo=0.5, observaciones=""),
        System(name="B", tipo="ia", C=0.2, F=0.3, T=0.4, I_op=0.5, vida=2, tasa=2, complejidad=2, P_riesgo=0.6, observaciones="")
    ]

@pytest.fixture(autouse=True)
def no_show(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **kw: None)

def test_demo_ped_real_fast(small_systems):
    # Llama la función con datos mínimos, sin abrir ventanas
    demo_ped_real.__globals__["load_systems_from_csv"] = lambda path: small_systems
    demo_ped_real("dummy.csv")


def test_demo_sensibilidad_real_fast(small_systems):
    import matplotlib
    matplotlib.use('Agg', force=True)
    demo_sensibilidad_real.__globals__["load_systems_from_csv"] = lambda path: small_systems
    demo_sensibilidad_real("dummy.csv")
