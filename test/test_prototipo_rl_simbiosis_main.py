"""
Cobertura del bloque main de prototipo_rl_simbiosis.py
"""
import subprocess
import sys
import os

def test_main_block_runs():
    # Ejecuta el script como CLI y verifica salida sin errores
    script = os.path.join(os.path.dirname(__file__), '..', 'sim', 'prototipo_rl_simbiosis.py')
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    result = subprocess.run([sys.executable, script, '--episodes', '10', '--seed', '42'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "Ejecutando experimentos" in result.stdout or "Running experiments" in result.stdout
