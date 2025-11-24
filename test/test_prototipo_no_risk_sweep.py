import runpy
import sys


def test_main_no_risk_sweep(monkeypatch):
    # Ejecuta main sin risk_sweep para cubrir ruta de comparación simple
    sys.argv = [
        "prototipo_rl_simbiosis.py",
        "--episodes",
        "1",
        "--seed",
        "0",
        "--risk_scale",
        "1.0",
        "--pgf_mix",
        "0.5",
    ]
    # Sólo verificar que no lanza excepciones
    runpy.run_path("sim/prototipo_rl_simbiosis.py", run_name="__main__")
