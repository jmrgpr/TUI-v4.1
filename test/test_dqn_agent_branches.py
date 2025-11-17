"""
Tests para ramas internas y edge cases de DQNAgent en TUI v4.1 Toy Model — RL Symbiosis
Branch and edge case tests for DQNAgent in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.dqn_agent import DQNAgent

def test_calcular_metricas_branches():
    from sim.evaluator_pgf import EvaluatorPGF
    evaluator = EvaluatorPGF()
    class DummyEnv:
        resources = 100.0
    env = DummyEnv()
    # Todos los casos de info
    info_cases = [
        {},
        {'shock': True},
        {'help': True},
        {'tripwire': True},
        {'low_resources': True},
        {'distractor': True},
        {'shock': True, 'help': True, 'tripwire': True, 'low_resources': True, 'distractor': True}
    ]
    for info in info_cases:
        metrics = evaluator.calcular_metricas(env, info, 0, 100.0, 'survive_and_help', 1.0)
        assert 'PGF' in metrics
        assert 'P_riesgo' in metrics
        assert 'I_op' in metrics

def test_pgf_logic_independence():
    """Test that PGF logic is independent of the agent - agent does not have calcular_metricas."""
    agent = DQNAgent(state_dim=2, action_dim=2)
    # Ensure agent does not have calcular_metricas method
    assert not hasattr(agent, 'calcular_metricas')
    # Ensure evaluator has it
    from sim.evaluator_pgf import EvaluatorPGF
    evaluator = EvaluatorPGF()
    assert hasattr(evaluator, 'calcular_metricas')
    # Test that run_experiment works with use_pgf=True and use_dqn=True
    from sim.prototipo_rl_simbiosis import run_experiment
    result = run_experiment(episodes=5, seed=42, risk_scale=1.0, agent_name="IndependenceTest", use_pgf=True, use_dqn=True)
    assert 'policy' in result
    assert 'pgf_evol' in result
