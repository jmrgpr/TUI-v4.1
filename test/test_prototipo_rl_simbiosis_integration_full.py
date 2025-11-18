import subprocess
import sys
import os

def test_full_integration_run():
    """
    Ejecuta el script principal como un subproceso para cubrir
    todas las ramas de argparse, visualización y logging.
    """
    # Construir el comando
    cmd = [
        sys.executable, "sim/prototipo_rl_simbiosis.py",
        "--episodes", "11",       # 11 episodios para forzar el print del ep 10 (línea 212)
        "--seed", "42",
        "--visualize",            # Cubre la rama visualización (línea 185)
        "--plot",                 # Cubre la rama plot (línea 594)
        "--export", "test_integration.json",
        "--dqn_control",
        "--risk_sweep"            # Cubre toda la lógica de sweep
    ]

    # Ejecutar
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verificar éxito
    assert result.returncode == 0, f"El script falló: {result.stderr}"
    
    # Limpieza (borrar archivos generados)
    if os.path.exists("test_integration.json"): os.remove("test_integration.json")
    # ... borrar también los CSVs generados ...