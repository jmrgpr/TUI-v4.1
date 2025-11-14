"""
Test de integración para el flujo completo de experimentos y logging en TUI v4.1 Toy Model — RL Symbiosis
Integration test for full experiment and logging flow in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.prototipo_rl_simbiosis import run_experiment

def test_run_experiment_full():
    results = run_experiment(episodes=5, seed=123, risk_scale=1.0, agent_name="Control")
    assert isinstance(results, dict)
    assert "total_rewards" in results
    assert len(results["total_rewards"]) == 5
    assert "flex_recov" in results
    assert "robust_evol" in results
    assert "q_optimal" in results or "q_optimal_evol" in results
    # Logging y métricas
    for key in ["flex_recov", "robust_evol", "total_rewards"]:
        assert all(isinstance(x, float) or isinstance(x, int) for x in results[key])
