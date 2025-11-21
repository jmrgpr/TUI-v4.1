import pytest
from sim.runner import run_experiment
from sim.dqn_agent import DQNAgent
from sim import environment, config, agent

def test_run_experiment_basic():
    # Este test parece obsoleto o incorrecto para la estructura actual.
    # run_experiment ahora crea sus propios agentes internamente.
    # Lo adaptamos para que sea un test de integración simple.
    results = run_experiment(episodes=2, seed=42, risk_scale=1.0, agent_name="Test", use_dqn=True)
    assert isinstance(results, dict)
    assert 'avg_reward' in results
    assert 'total_rewards' in results
    assert isinstance(results['total_rewards'], list)

def test_run_experiment_zero_episodes_dqn():
    """Test run_experiment with episodes=0 and use_dqn=True to cover agent initialization."""
    results = run_experiment(episodes=0, seed=42, risk_scale=1.0, agent_name="Test", use_dqn=True)
    assert results['total_rewards'] == []
    assert results['policy'] is not None  # Should have DQN model
