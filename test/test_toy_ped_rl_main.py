"""
Cobertura del bloque main de toy_ped_rl.py
"""
import runpy
import sys
import os

def test_main_block_runs():
    # Ejecuta el script como CLI usando runpy para cobertura
    sys.argv = ['toy_ped_rl.py']
    runpy.run_module('sim.toy_ped_rl', run_name='__main__')

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
