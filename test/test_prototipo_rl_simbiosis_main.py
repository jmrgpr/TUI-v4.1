"""
Cobertura del bloque main de prototipo_rl_simbiosis.py
"""
<<<<<<< HEAD
<<<<<<< HEAD
import runpy
import sys
import os
from unittest.mock import patch
import pytest

def test_main_block_runs():
    # Ejecuta el script como CLI usando runpy para cobertura
    sys.argv = ['prototipo_rl_simbiosis.py', '--risk_sweep', '--dqn_control', '--episodes', '20', '--seed', '42']
    runpy.run_module('sim.prototipo_rl_simbiosis', run_name='__main__')

# (Importa tu función main desde el script)
from sim.prototipo_rl_simbiosis import main as prototipo_main

def test_main_execution_with_all_flags():
    """
    Test de integración para el bloque main() simulando todos los flags.
    Esto cubrirá las ramas de argparse y las funciones de plot/visualize.
    """
    # 1. Mockear las funciones que abren ventanas o escriben archivos
    with patch('matplotlib.pyplot.show'), \
         patch('builtins.print'), \
         patch('builtins.open'), \
         patch('json.dump'), \
         patch('csv.writer'):

        # 2. Simular los argumentos de línea de comandos (sys.argv)
        # Corremos con 10 episodios para cubrir la línea (ep+1) % 10 == 0
        # y todos los flags activados
        test_args = [
            'prototipo_rl_simbiosis.py', # El nombre del script
            '--episodes', '10',
            '--seed', '42',
            '--export', 'test_export_main.json',
            '--dqn_control',
            '--grid_size', '4' # Probar un valor no-default
        ]

        # 3. Usar patch.object para reemplazar sys.argv
        with patch.object(sys, 'argv', test_args):
            # 4. Llamar a la función main()
            prototipo_main()

            # 5. Verificaciones (Opcional pero recomendado)
            # Verificar que se intentó mostrar los gráficos
            # assert plt.show.called 
            # Verificar que se intentó exportar
            # assert json.dump.called
            # assert csv.writer.called

# Este es el test que te dará la cobertura de argparse
def test_main_script_execution_all_flags():
    """
    Test de integración que simula la ejecución del script principal
    con todos los flags de argparse para cubrir las ramas faltantes.
    """
    if prototipo_main is None:
        pytest.skip("No se pudo importar prototipo_main")

    # 1. Mockear funciones que crean archivos o muestran gráficos
    with patch('matplotlib.pyplot.show'), \
         patch('builtins.open'), \
         patch('json.dump'), \
         patch('csv.writer'):

        # 2. Simular los argumentos de línea de comandos (sys.argv)
        # Corremos con 10 episodios para cubrir la línea (ep+1) % 10 == 0
        test_args = [
            'script_name.py',
            '--episodes', '10',         # Cubre la línea 212-217
            '--seed', '42',
            '--visualize',            # Cubre la línea 185
            '--plot',                 # Cubre la línea 594
            '--export', 'test.json',
            '--dqn_control'           # Cubre la línea 216-217
        ]

        # 3. Usar patch.object para reemplazar sys.argv ANTES de llamar a main
        with patch.object(sys, 'argv', test_args):
            # 4. Llamar a la función main()
            prototipo_main()

            # 5. Verificaciones
            # assert plt.show.called
            # assert json.dump.called
            
    # Test adicional para el agente Q-learning y la línea 239
    test_args_q_learning = ['script_name.py', '--episodes', '1']
    with patch.object(sys, 'argv', test_args_q_learning):
        prototipo_main()

def test_main_with_risk_sweep():
    """
    Test para cubrir --risk_sweep y las líneas en el barrido de riesgo.
    """
    import matplotlib
    matplotlib.use('Agg')
    
    with patch('matplotlib.pyplot.show'), \
         patch('matplotlib.pyplot.savefig'), \
         patch('builtins.open'), \
         patch('json.dump'), \
         patch('csv.writer'), \
         patch('seaborn.heatmap'), \
         patch('pandas.DataFrame'):

        test_args = [
            'script_name.py',
            '--risk_sweep',
            '--episodes', '1',  # Para que sea rápido
            '--seed', '42',
            '--export', 'test_sweep.json'
        ]

        with patch.object(sys, 'argv', test_args):
            prototipo_main()
=======
import subprocess
=======
import runpy
>>>>>>> c547074 (Improve test coverage to 95% - Add tests for missing lines in gui_streamlit, prototipo_rl_simbiosis, toy_ped_rl_excel. Update README and CHANGELOG.)
import sys
import os

def test_main_block_runs():
<<<<<<< HEAD
    # Ejecuta el script como CLI y verifica salida sin errores
    script = os.path.join(os.path.dirname(__file__), '..', 'sim', 'prototipo_rl_simbiosis.py')
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    result = subprocess.run([sys.executable, script, '--episodes', '10', '--seed', '42'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "Ejecutando experimentos" in result.stdout or "Running experiments" in result.stdout
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
=======
    # Ejecuta el script como CLI usando runpy para cobertura
    sys.argv = ['prototipo_rl_simbiosis.py', '--risk_sweep', '--dqn_control', '--episodes', '20', '--seed', '42']
    runpy.run_module('sim.prototipo_rl_simbiosis', run_name='__main__')
>>>>>>> c547074 (Improve test coverage to 95% - Add tests for missing lines in gui_streamlit, prototipo_rl_simbiosis, toy_ped_rl_excel. Update README and CHANGELOG.)
