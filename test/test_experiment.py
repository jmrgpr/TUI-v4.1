"""
Test de experimentos y comparación de agentes en TUI v4.1 Toy Model — RL Symbiosis
Tests for experiments and agent comparison in TUI v4.1 Toy Model — RL Symbiosis
"""
# Profesional: asegura importación robusta de 'sim'
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.prototipo_rl_simbiosis import run_experiment

def test_run_experiment_basic():
    results = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="Control")
    assert "total_rewards" in results
    assert len(results["total_rewards"]) == 10
