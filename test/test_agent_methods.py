"""
Tests avanzados para todos los métodos de Agent y DQNAgent en TUI v4.1 Toy Model — RL Symbiosis
Advanced tests for all Agent and DQNAgent methods in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import torch
from sim.dqn_agent import DQNAgent
from sim.prototipo_rl_simbiosis import Agent

def test_agent_act():
    agent = Agent(name="Test", resources=100)
    state = (0, 0)
    action = agent.act(state)
    assert action in agent.ACTIONS

def test_agent_update_policy():
    agent = Agent(name="Test", resources=100)
    state = (0, 0)
    action = 'up'
    next_state = (0, 1)
    agent.update_policy(state, action, 1.0, next_state)
    key = (state, action)
    assert key in agent.policy

def test_agent_remember_and_memory():
    agent = Agent(name="Test", resources=100)
    agent.remember("evento")
    assert len(agent.memory) == 1
    for i in range(101):
        agent.remember(f"evento{i}")
    assert len(agent.memory) == 100

def test_agent_reprogram_purpose():
    agent = Agent(name="Test", resources=100)
    agent.reprogram_purpose("survive_and_help")
    assert agent.purpose == "survive_and_help"
    assert agent.alignment == 1.0
    agent.reprogram_purpose("other")
    assert agent.alignment == 0.8

def test_dqn_agent_act_and_learn():
    agent = DQNAgent(state_dim=2, action_dim=2)
    state = np.array([0.0, 1.0], dtype=np.float32)
    action = agent.act(state)
    assert isinstance(action, int)
    agent.remember(state, action, 1.0, state, False)
    agent.learn()  # No error si memoria insuficiente
    for _ in range(agent.batch_size):
        agent.remember(state, action, 1.0, state, False)
    agent.learn()  # Debe ejecutar el aprendizaje

def test_dqn_agent_save_and_load(tmp_path):
    agent = DQNAgent(state_dim=2, action_dim=2)
    filename = tmp_path / "policy.pt"
    agent.save(str(filename))
    agent.load(str(filename))
    assert os.path.exists(filename)
