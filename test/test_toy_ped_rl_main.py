"""
Cobertura del bloque main de toy_ped_rl.py
"""
<<<<<<< HEAD
import runpy
=======
import subprocess
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
import sys
import os

def test_main_block_runs():
<<<<<<< HEAD
    # Ejecuta el script como CLI usando runpy para cobertura
    sys.argv = ['toy_ped_rl.py']
    runpy.run_module('sim.toy_ped_rl', run_name='__main__')
=======
    # Ejecuta el script como CLI y verifica salida sin errores
    script = os.path.join(os.path.dirname(__file__), '..', 'sim', 'toy_ped_rl.py')
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    assert result.returncode == 0
    # Verifica presencia de mensajes clave sin hardcoding exacto
    assert any("SIMULACIONES" in line for line in result.stdout.splitlines())
    assert any("FIN" in line for line in result.stdout.splitlines())
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)

def test_calculate_pgf():
    from sim.toy_ped_rl import calculate_pgf
    config = {'cost': 5.0}
    result = calculate_pgf(10.0, 3.0, 1.0, 2.0, config)
    assert result == 2.0  # 10 - 3 - 5

def test_pearson_correlation():
    from sim.toy_ped_rl import pearson_correlation
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    corr = pearson_correlation(x, y)
    assert abs(corr - 1.0) < 1e-8
    # Caso borde: listas vacías
    assert pearson_correlation([], []) == 0.0
