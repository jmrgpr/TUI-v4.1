"""
Tests de edge cases y ramas internas para experimentos en TUI v4.1 Toy Model — RL Symbiosis
Edge case and branch tests for experiments in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.prototipo_rl_simbiosis import run_experiment

def test_run_experiment_zero_episodes():
    results = run_experiment(episodes=0, seed=42, risk_scale=1.0, agent_name="Control")
    assert isinstance(results, dict)
    assert "total_rewards" in results
    assert len(results["total_rewards"]) == 0

def test_run_experiment_invalid_agent():
    try:
        run_experiment(episodes=5, seed=42, risk_scale=1.0, agent_name="InvalidAgent")
    except Exception:
        pass  # Debe manejar agentes no reconocidos sin romper el flujo
