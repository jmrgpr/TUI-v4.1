#!/usr/bin/env python3
"""
test_prototipo_rl_simbiosis_coverage.py — Tests adicionales para aumentar cobertura en prototipo_rl_simbiosis.py

Tests adicionales para aumentar cobertura en prototipo_rl_simbiosis.py, enfocados en líneas no cubiertas.
"""
import pytest
import numpy as np
import random
import torch
from sim.prototipo_rl_simbiosis import Agent, SimbiosisEnv, run_experiment, transfer_test, main
from sim.dqn_agent import DQNAgent
import argparse
import sys
import os

@pytest.fixture
def sample_env():
    return SimbiosisEnv(size=5, initial_resources=100.0, tripwires=[(2,2)], shocks=[(3,3)], distractors=[(1,1)], risk_scale=1.0)

@pytest.fixture
def sample_agent():
    return Agent(name="TestAgent", resources=100.0)

def test_agent_class_attributes():
    """Test atributos de clase en Agent."""
    assert Agent.T == 0.0
    assert Agent.I_op == 0.0
    assert Agent.P_riesgo == 0.0
    assert Agent.P_genuino == 0.0
    assert Agent.eta_extendido == 0.0
    assert Agent.PGF == 0.0
    assert Agent.C_costo == 0.0
    assert Agent.S_auto == 0.0
    assert Agent.R_robust == 0.0
    assert Agent.I_rep == 0.0

def test_agent_reprogram_purpose(sample_agent):
    """Test reprogram_purpose method."""
    sample_agent.reprogram_purpose("survive_and_help")
    assert sample_agent.purpose == "survive_and_help"
    assert sample_agent.alignment == 1.0

    sample_agent.reprogram_purpose("other")
    assert sample_agent.purpose == "other"
    assert sample_agent.alignment == 0.8

def test_calcular_metricas_detailed(sample_agent, sample_env):
    """Test calcular_metricas with various scenarios."""
    # Scenario with tripwire
    info = {'tripwire': True, 'shock': False, 'distractor': False, 'help': False, 'low_resources': False}
    sample_agent.calcular_metricas(sample_env, info, 0)
    assert sample_agent.P_riesgo_actual == 20.0
    assert sample_agent.P_riesgo == 20.0
    assert sample_agent.P_riesgo_prev == 20.0

    # Scenario with shock
    info = {'tripwire': False, 'shock': True, 'distractor': False, 'help': False, 'low_resources': False}
    sample_agent.calcular_metricas(sample_env, info, 1)
    assert sample_agent.P_riesgo_actual == 30.0  # 20 + 10

    # Scenario with distractor
    info = {'tripwire': False, 'shock': False, 'distractor': True, 'help': False, 'low_resources': False}
    sample_agent.calcular_metricas(sample_env, info, 2)
    assert sample_agent.P_riesgo_actual == 35.0  # 30 + 5

    # Scenario with help
    info = {'tripwire': False, 'shock': False, 'distractor': False, 'help': True, 'low_resources': False}
    sample_agent.calcular_metricas(sample_env, info, 3)
    assert sample_agent.I_rep == 1.0

    # Scenario with low resources
    info = {'tripwire': False, 'shock': False, 'distractor': False, 'help': False, 'low_resources': True}
    sample_agent.calcular_metricas(sample_env, info, 4)
    assert sample_agent.C_costo == 1.0

def test_run_experiment_episodes_zero():
    """Test run_experiment with episodes=0."""
    result = run_experiment(episodes=0, seed=42, risk_scale=1.0, agent_name="Test", use_pgf=False, use_dqn=False)
    assert result['avg_reward'] == 0.0
    assert result['total_rewards'] == []

def test_run_experiment_use_dqn():
    """Test run_experiment with use_dqn=True."""
    result = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="DQNTest", use_pgf=False, use_dqn=True)
    assert 'policy' in result
    assert isinstance(result['policy'], dict)  # state_dict

def test_run_experiment_use_pgf():
    """Test run_experiment with use_pgf=True."""
    result = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="PGFTest", use_pgf=True, use_dqn=False)
    assert 'pgf_evol' in result

def test_test_transferencia():
    """Test test_transferencia function."""
    policy = {((('recursos_altos', 0), ('recursos_bajos', 0), ('veo_tripwire_cerca', 0), ('veo_shock_cerca', 0), ('veo_distractor_cerca', 0), ('veo_meta_cerca', 0)), 'up'): 1.0}
    tripwires = transfer_test(policy, seed=42, risk_scale=1.0)
    assert isinstance(tripwires, int)

def test_main_risk_sweep(monkeypatch, tmp_path):
    """Test main with --risk_sweep."""
    # Mock sys.argv
    export_path = tmp_path / "sweep.json"
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--risk_sweep', '--export', str(export_path)])
    monkeypatch.chdir(tmp_path)
    # Mock matplotlib to avoid display issues
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    monkeypatch.setattr('matplotlib.pyplot.savefig', lambda *args, **kwargs: None)
    # This will run the risk sweep
    main()

def test_main_export(monkeypatch, tmp_path):
    """Test main with --export."""
    export_path = tmp_path / "test_export.json"
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--export', str(export_path)])
    monkeypatch.chdir(tmp_path)
    main()
    assert export_path.exists()

def test_main_visualize(monkeypatch):
    """Test main with --visualize."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '5', '--seed', '42', '--visualize'])
    main()

def test_main_plot(monkeypatch):
    """Test main with --plot."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '5', '--seed', '42', '--plot'])
    main()

def test_main_grid_size(monkeypatch):
    """Test main with different grid_size."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '5', '--seed', '42', '--grid_size', '3'])
    main()

def test_main_risk_scale(monkeypatch):
    """Test main with different risk_scale."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '5', '--seed', '42', '--risk_scale', '0.5'])
    main()

def test_run_experiment_use_dqn_true():
    """Test run_experiment with use_dqn=True."""
    result = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="DQN", use_pgf=False, use_dqn=True)
    assert 'policy' in result

def test_run_experiment_use_pgf_true():
    """Test run_experiment with use_pgf=True."""
    result = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="PGF", use_pgf=True, use_dqn=False)
    assert 'pgf_evol' in result

def test_run_experiment_different_risk_scale():
    """Test run_experiment with different risk_scale."""
    result = run_experiment(episodes=10, seed=42, risk_scale=2.0, agent_name="Test", use_pgf=False, use_dqn=False)
    assert result['avg_reward'] is not None

def test_main_with_visualize(monkeypatch):
    """Test main with --visualize."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--visualize'])
    main()

def test_main_with_plot(monkeypatch):
    """Test main with --plot."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--plot'])
    main()

def test_main_with_grid_size(monkeypatch):
    """Test main with --grid_size."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--grid_size', '3'])
    main()

def test_main_with_risk_scale(monkeypatch):
    """Test main with --risk_scale."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42', '--risk_scale', '0.5'])
    main()

def test_main_normal_run(monkeypatch, capsys):
    """Test main normal run without special flags."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '10', '--seed', '42'])
    main()
    captured = capsys.readouterr()
    assert "Ejecutando experimentos" in captured.out

def test_run_experiment_with_logging(capsys):
    """Test run_experiment with logging activated."""
    result = run_experiment(episodes=10, seed=42, risk_scale=1.0, agent_name="LogTest", use_pgf=False, use_dqn=False)
    captured = capsys.readouterr()
    assert "Progreso" in captured.out or "Episode" in captured.out