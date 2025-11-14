"""
Tests de ramas profundas y edge cases para prototipo_rl_simbiosis.py
Deep branch and edge case tests for prototipo_rl_simbiosis.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.prototipo_rl_simbiosis import run_experiment

def test_run_experiment_max_steps():
    # Test de límite de pasos por episodio
    results = run_experiment(episodes=2, seed=42, risk_scale=1.0, agent_name="Control")
    assert len(results["pgf_evol"][0]) <= 50

def test_run_experiment_tripwire_shock():
    # Test de logging y métricas con tripwire y shock
    results = run_experiment(episodes=2, seed=42, risk_scale=1.0, agent_name="Control")
    assert isinstance(results["tripwire_steps"], list)
    assert isinstance(results["shocks_evol"], list)

def test_run_experiment_survival_evol():
    # Test de evolución de supervivencia
    results = run_experiment(episodes=2, seed=42, risk_scale=1.0, agent_name="Control")
    assert isinstance(results["survival_evol"], list)
    assert all(isinstance(x, float) for x in results["survival_evol"])
