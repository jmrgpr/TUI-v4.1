"""
Test unitarios para agentes del TUI v4.1 Toy Model — RL Symbiosis
Unit tests for agents in TUI v4.1 Toy Model — RL Symbiosis
"""
# Profesional: asegura importación robusta de 'sim'
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from sim.dqn_agent import DQNAgent
from sim.prototipo_rl_simbiosis import Agent

def test_agent_init():
    agent = Agent(name="Control", resources=100)
    assert agent.name == "Control"
    assert agent.resources == 100

def test_dqn_agent_init():
    agent = DQNAgent(state_dim=5, action_dim=4)
    assert agent.model is not None
    assert agent.memory is not None
