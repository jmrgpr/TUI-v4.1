"""
Tests exhaustivos de ramas internas y edge cases para run_experiment en prototipo_rl_simbiosis.py
Full branch and edge case tests for run_experiment in prototipo_rl_simbiosis.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.prototipo_rl_simbiosis import run_experiment

def test_run_experiment_control():
    # Control agent, PGF off, DQN off
    results = run_experiment(episodes=5, seed=123, risk_scale=1.0, agent_name="Control", use_pgf=False, use_dqn=False)
    assert "avg_reward" in results
    assert isinstance(results["avg_reward"], float)

def test_run_experiment_simbiosis_dqn():
    # Simbiosis agent, PGF off, DQN on
    results = run_experiment(episodes=5, seed=123, risk_scale=1.0, agent_name="Simbiosis", use_pgf=False, use_dqn=True)
    assert "avg_reward" in results
    assert isinstance(results["avg_reward"], float)

def test_run_experiment_pgf_on():
    # PGF on, DQN off
    results = run_experiment(episodes=5, seed=123, risk_scale=1.0, agent_name="Control", use_pgf=True, use_dqn=False)
    assert "avg_flex" in results
    assert isinstance(results["avg_flex"], float)

def test_run_experiment_zero_episodes():
    # Edge case: zero episodes
    results = run_experiment(episodes=0, seed=123, risk_scale=1.0, agent_name="Control")
    assert results["total_rewards"] == []
    assert results["avg_reward"] == 0.0

def test_run_experiment_invalid_agent():
    # Edge case: invalid agent name
    results = run_experiment(episodes=2, seed=123, risk_scale=1.0, agent_name="NoExiste")
    assert "avg_reward" in results
