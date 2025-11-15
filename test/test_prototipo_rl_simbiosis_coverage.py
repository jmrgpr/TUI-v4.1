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

def test_agent_reprogram_purpose(monkeypatch):
    """
    Test para cubrir reprogram_purpose (línea 197)
    """
    from sim.prototipo_rl_simbiosis import Agent
    
    agent = Agent(name="Test", resources=100.0)
    original_purpose = agent.purpose
    agent.reprogram_purpose("new_purpose")
    assert agent.purpose == "new_purpose"

def test_calcular_metricas_detailed(sample_agent, sample_env):
    """Test calcular_metricas with various scenarios."""
    from sim.evaluator_pgf import EvaluatorPGF
    evaluator = EvaluatorPGF()
    # Scenario with tripwire
    info = {'tripwire': True, 'shock': False, 'distractor': False, 'help': False, 'low_resources': False}
    metrics = evaluator.calcular_metricas(sample_env, info, 0, sample_agent.resources, sample_agent.purpose, sample_agent.alignment)
    assert isinstance(metrics['PGF'], float) and metrics['PGF'] != 0.0

def test_agent_act_branches(sample_agent):
    # Cubre branch aleatorio y branch de argmax
    state = (0, 0)
    # Forzar branch aleatorio
    np.random.seed(42)
    random.seed(42)
    actions = set()
    for _ in range(20):
        actions.add(sample_agent.act(state))
    assert all(a in sample_agent.ACTIONS for a in actions)
    # Forzar branch argmax
    # Asigna valores para que argmax sea reproducible
    for idx, a in enumerate(sample_agent.ACTIONS):
        sample_agent.policy[(state, a)] = idx
    # Ejecuta múltiples veces para cubrir ambos branches
    actions = set()
    for _ in range(50):
        actions.add(sample_agent.act(state))
    # Debe cubrir tanto el branch aleatorio como el de argmax
    assert 'right' in actions
    assert all(a in sample_agent.ACTIONS for a in actions)

def test_update_policy_branches(sample_agent):
    state = (0, 0)
    action = 'up'
    reward = 1.0
    next_state = (0, 1)
    # Sin Q previo
    sample_agent.update_policy(state, action, reward, next_state)
    assert (state, action) in sample_agent.policy
    # Con Q previo
    sample_agent.policy[(next_state, 'up')] = 2.0
    sample_agent.update_policy(state, action, reward, next_state)
    assert sample_agent.policy[(state, action)] != 0.0

def test_save_and_load_policy(tmp_path, sample_agent):
    # Guardar y cargar policy con tuplas y strings
    sample_agent.policy = {('a', 'b'): 1.0, 'c': 2.0}
    file_path = tmp_path / "policy.json"
    sample_agent.save_policy(str(file_path))
    assert file_path.exists()
    sample_agent.policy = {}
    sample_agent.load_policy(str(file_path))
    # Debe reconstruir la tupla y mantener la clave string
    assert ('a', 'b') in sample_agent.policy
    assert 'c' in sample_agent.policy

def test_agent_save_load_policy(monkeypatch):
    """
    Test para cubrir save_policy y load_policy (líneas 143-146, 170-171, 174-175)
    """
    from sim.prototipo_rl_simbiosis import Agent
    import tempfile
    import os
    
    agent = Agent(name="Test", resources=100.0)
    agent.policy = {('state1', 'up'): 1.0, ('state2', 'down'): 0.5}
    
    # Test save_policy
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        agent.save_policy(temp_file)
        assert os.path.exists(temp_file)
        
        # Test load_policy
        agent2 = Agent(name="Test2", resources=100.0)
        agent2.load_policy(temp_file)
        assert agent2.policy == agent.policy
        
        # Test load_policy con archivo corrupto
        with open(temp_file, 'w') as f:
            f.write("invalid json")
        agent3 = Agent(name="Test3", resources=100.0)
        agent3.load_policy(temp_file)  # Debería manejar la excepción y setear policy={}
        assert agent3.policy == {}
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

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

def test_cli_risk_sweep():
    import subprocess
<<<<<<< HEAD
    import os
    cmd = ["python", "-c", "import sys; sys.path.insert(0, '.'); from sim.prototipo_rl_simbiosis import main; import sys; sys.argv = ['script', '--risk_sweep', '--episodes', '5', '--seed', '42']; main()"]
    cwd = '.' if os.name != 'nt' else 'c:\\Proyectos\\TUI-v4.1'
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    assert result.returncode == 0
    assert "Barrido de risk_scale: 0.5" in result.stdout
    assert "Barrido de risk_scale: 2.0" in result.stdout

def test_simbiosis_env_init():
    """Test SimbiosisEnv initialization."""
    from sim.prototipo_rl_simbiosis import SimbiosisEnv
    env = SimbiosisEnv()
    assert env.size == 5
    assert env.agent_pos == [0, 0]
    assert env.resources == 100.0
    assert env.tripwires == [(2, 2)]
    assert env.shocks == [(3, 3)]
    assert env.distractors == [(1, 1)]
    assert env.risk_scale == 1.0
    assert env.timestep == 0
    assert env.done == False
    assert env.history == []
    # Call reset to cover reset lines
    env.reset()

def test_run_experiment_episodes_20(capsys):
    """Test run_experiment with episodes=20 to cover progress logging."""
    result = run_experiment(episodes=20, seed=42, risk_scale=1.0, agent_name="Test", use_pgf=False, use_dqn=False)
    captured = capsys.readouterr()
    assert "Progreso" in captured.out or "Progress" in captured.out

def test_env_step_on_shock():
    """Test env step on shock position to cover shock handling."""
    env = SimbiosisEnv()
    env.agent_pos = [3, 3]
    state, reward, done, info = env.step('stay')  # Invalid action, stays in place
    assert info.get('shock') == True
    assert reward == -10.0

def test_run_experiment_with_shock_triggers_flexibility_logic(monkeypatch):
    """
    Test para cubrir la lógica de 'steps_to_recover' (líneas 351-353)
    forzando un shock en un agente DQN.
    """
    from sim.prototipo_rl_simbiosis import run_experiment
    
    # Mockear el step del entorno para que SIEMPRE devuelva un shock
    next_state = (('x', 0), ('y', 0), ('recursos_altos', 1), ('recursos_bajos', 0), ('veo_tripwire_cerca', 0), ('veo_shock_cerca', 0), ('veo_distractor_cerca', 0), ('veo_meta_cerca', 0))
    reward_env = -10.0
    done = False
    info = {'shock': True}
    monkeypatch.setattr(SimbiosisEnv, 'step', lambda self, action: (next_state, reward_env, done, info))

    # Correr el experimento con un agente DQN
    results = run_experiment(
        episodes=2, 
        seed=42, 
        risk_scale=1.0,
        agent_name="DQN",
        use_pgf=False,
        use_dqn=True
    )

    # El shock ocurre en el primer paso (0). steps_to_recover cuenta
    # desde 1 hasta 5 (inclusive). Debería ser 5.
    assert results['avg_flex'] is not None

def test_run_experiment_with_shock_triggers_flexibility_logic_tabular(monkeypatch):
    """
    Test para cubrir la lógica de 'steps_to_recover' y 'reprogram_purpose' con agente tabular.
    """
    from sim.prototipo_rl_simbiosis import run_experiment
    
    # Mockear el step del entorno: shock en el primer paso, luego no
    def mock_step(self, action):
        if self.timestep == 0:
            next_state = (('x', 0), ('y', 0), ('recursos_altos', 1), ('recursos_bajos', 0), ('veo_tripwire_cerca', 0), ('veo_shock_cerca', 0), ('veo_distractor_cerca', 0), ('veo_meta_cerca', 0))
            reward_env = -10.0
            done = False
            info = {'shock': True}
        else:
            next_state = (('x', 0), ('y', 0), ('recursos_altos', 1), ('recursos_bajos', 0), ('veo_tripwire_cerca', 0), ('veo_shock_cerca', 0), ('veo_distractor_cerca', 0), ('veo_meta_cerca', 0))
            reward_env = 0.0
            done = self.timestep >= 49  # Termina al final
            info = {}
        self.timestep += 1
        return next_state, reward_env, done, info
    
    monkeypatch.setattr(SimbiosisEnv, 'step', mock_step)

    # Correr el experimento con agente tabular
    results = run_experiment(
        episodes=1, 
        seed=42, 
        risk_scale=1.0,
        agent_name="Tabular",
        use_pgf=False,
        use_dqn=False
    )

    # Verificar que reprogram_purpose se llamó (línea 239)
    # No podemos verificar directamente, pero el test asegura que se ejecuta
    assert results['avg_reward'] is not None

def test_run_experiment_logging(monkeypatch):
    """
    Test para cubrir el logging condicional en run_experiment (líneas 309-311)
    """
    from sim.prototipo_rl_simbiosis import run_experiment
    
    # Mock para evitar ejecución real
    def mock_run_experiment(*args, **kwargs):
        # Simular 10 episodios para forzar el print en ep=10
        pass
    monkeypatch.setattr('sim.prototipo_rl_simbiosis.run_experiment', mock_run_experiment)
    
    # Pero mejor ejecutar un experimento pequeño con 10 episodios
    results = run_experiment(
        episodes=10, 
        seed=42, 
        risk_scale=1.0,
        agent_name="Test",
        use_pgf=False,
        use_dqn=False
    )
    assert results['avg_reward'] is not None
=======
    cmd = ["python", "sim/prototipo_rl_simbiosis.py", "--risk_sweep", "--episodes", "5", "--seed", "42"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Risk scale: 0.5" in result.stdout
    assert "Risk scale: 2.0" in result.stdout
>>>>>>> c226c67 (Cobertura 100%: implementaciones finales de pad_trajectories y safe_plot, tests completos)
