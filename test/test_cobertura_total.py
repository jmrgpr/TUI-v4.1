import sys
import os
from unittest.mock import patch
import matplotlib.pyplot as plt
from sim.prototipo_rl_simbiosis import main as prototipo_main, run_experiment, SimbiosisEnv

def test_main_con_todos_los_flags():
    """
    Ejecuta el main() simulando argumentos de línea de comandos.
    Cubre: argparse, visualización, plots, exportación y lógica de selección de agente.
    """
    args_simulados = [
        'prototipo_rl_simbiosis.py',
        '--episodes', '11',
        '--seed', '42',
        '--visualize',
        '--plot',
        '--export', 'dummy.json',
        '--risk_sweep',
        '--dqn_control'
    ]
    with patch('matplotlib.pyplot.show'), \
         patch('matplotlib.pyplot.savefig'), \
         patch('builtins.print'), \
         patch('builtins.open'), \
         patch('json.dump'), \
         patch('csv.writer'), \
         patch.object(sys, 'argv', args_simulados):
        prototipo_main()
    # No se puede usar plt.show.called directamente, pero se valida que no hay error

def test_agente_tabular_y_reprogramacion():
    """
    Cubre la inicialización de la clase Agent base y la reprogramación de propósito.
    """
    run_experiment(
        episodes=2,
        seed=42,
        risk_scale=1.0,
        agent_name="TestTabular",
        use_pgf=False,
        use_dqn=False
    )

def test_logica_recuperacion_shock():
    """
    Fuerza un 'shock' en el entorno para obligar al código a entrar en la lógica de recuperación (steps_to_recover).
    """
    original_step = SimbiosisEnv.step
    def step_con_shock_forzado(self, action):
        state, reward, done, info = original_step(self, action)
        if self.timestep == 1:
            info['shock'] = True
        return state, reward, done, info
    with patch.object(SimbiosisEnv, 'step', side_effect=step_con_shock_forzado, autospec=True):
        run_experiment(episodes=1, seed=42, risk_scale=1.0, agent_name="ShockTest", use_dqn=True)
