"""
Cobertura del bloque main de prototipo_rl_simbiosis.py
"""
import runpy
import sys
import os

def test_main_block_runs():
    # Ejecuta el script como CLI usando runpy para cobertura
    sys.argv = ['prototipo_rl_simbiosis.py', '--risk_sweep', '--fast', '--dqn_control', '--seed', '42']
    runpy.run_module('sim.prototipo_rl_simbiosis', run_name='__main__')
