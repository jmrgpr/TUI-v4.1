"""
Tests para ramas internas y edge cases de DQNAgent en TUI v4.1 Toy Model — RL Symbiosis
Branch and edge case tests for DQNAgent in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.dqn_agent import DQNAgent

def test_calcular_metricas_branches():
    agent = DQNAgent(state_dim=2, action_dim=2)
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
        agent.calcular_metricas(env, info, step=0)
        assert hasattr(agent, 'PGF')
        assert hasattr(agent, 'P_riesgo')
        assert hasattr(agent, 'I_op')

def test_act_epsilon_branch():
    agent = DQNAgent(state_dim=2, action_dim=2, epsilon=1.0)
    state = np.array([0.0, 1.0], dtype=np.float32)
    # Con epsilon=1.0 siempre debe explorar
    actions = [agent.act(state) for _ in range(10)]
    assert all(isinstance(a, int) for a in actions)
    # Con epsilon=0.0 siempre debe explotar
    agent.epsilon = 0.0
    actions = [agent.act(state) for _ in range(10)]
    assert all(isinstance(a, int) for a in actions)
