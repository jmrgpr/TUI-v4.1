from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as mpl_plt
import sim.prototipo_rl_simbiosis as prs
import sim.toy_ped_rl as tpr
import sim.toy_ped_rl_excel as tpex


def test_run_experiment_with_q_policy_logging(monkeypatch):
    # Force agent to have 'Q' in policy to hit q_opt branch in logging
    class TestAgent(prs.Agent):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.policy = {'Q': np.array([1.0, 2.0, 3.0, 4.0])}  # Force Q branch
    monkeypatch.setattr(prs, 'Agent', TestAgent)
    # Run with low episodes to trigger logging
    res = prs.run_experiment(episodes=2, seed=1, risk_scale=1.0, agent_name='TestQ', use_pgf=False, use_dqn=False)
    assert 'avg_reward' in res


def test_main_risk_sweep_fast_no_plots(tmp_path, monkeypatch):
    # Patch plt.savefig to avoid file writes
    monkeypatch.setattr(mpl_plt, 'savefig', lambda *a, **k: None)
    monkeypatch.setattr(mpl_plt, 'show', lambda: None)
    monkeypatch.setattr(mpl_plt, 'close', lambda *a: None)
    # Change to tmp_path
    monkeypatch.chdir(tmp_path)
    # Mock sys.argv for risk_sweep fast
    orig_argv = sys.argv.copy()
    sys.argv[:] = ['prog', '--fast', '--risk_sweep', '--export', 'test_sweep.json']
    try:
        prs.main()
    finally:
        sys.argv[:] = orig_argv
    # Should complete without error


def test_toy_ped_rl_main_execution(monkeypatch):
    # Patch prints to avoid long output
    def mock_print(*args, **kwargs):
        pass
    monkeypatch.setattr('builtins.print', mock_print)
    # Execute the __main__ block
    tpr.demo_gridworld_camino_c()
    tpr.demo_ped_arbol_humano()
    tpr.demo_sensibilidad_pesos()


def test_toy_ped_rl_excel_cargar_datos_valid_csv():
    # Use the real CSV file
    csv_path = ROOT / 'data' / 'Sistemas_naturales_IA_utf8_limpio.csv'
    systems = tpex.cargar_datos_excel(str(csv_path))
    assert len(systems) > 0


def test_demo_ped_real_with_csv(monkeypatch):
    # Use real CSV
    csv_path = ROOT / 'data' / 'Sistemas_naturales_IA_utf8_limpio.csv'
    # Patch plt
    monkeypatch.setattr(mpl_plt, 'savefig', lambda *a, **k: None)
    monkeypatch.setattr(mpl_plt, 'show', lambda: None)
    monkeypatch.setattr(mpl_plt, 'close', lambda *a: None)
    # Run
    tpex.demo_ped_real(str(csv_path))


def test_main_export_normal(tmp_path, monkeypatch):
    # Test main with --export to cover export branches
    monkeypatch.setattr(mpl_plt, 'savefig', lambda *a, **k: None)
    monkeypatch.setattr(mpl_plt, 'show', lambda: None)
    monkeypatch.setattr(mpl_plt, 'close', lambda *a: None)
    monkeypatch.chdir(tmp_path)
    orig_argv = sys.argv.copy()
    sys.argv[:] = ['prog', '--episodes', '1', '--fast', '--export', 'test_export.json']
    try:
        prs.main()
    finally:
        sys.argv[:] = orig_argv


def test_toy_ped_rl_main_block(tmp_path, monkeypatch):
    # Execute the __main__ block of toy_ped_rl.py
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    # Import and run the main block
    exec(open(ROOT / 'sim' / 'toy_ped_rl.py').read(), {'__name__': '__main__'})


def test_agent_act_random_branch(monkeypatch):
    # Force random.random < 0.2 to hit the random action branch
    monkeypatch.setattr('random.random', lambda: 0.1)
    agent = prs.Agent()
    state = {}
    action = agent.act(state)
    assert action in agent.ACTIONS


def test_run_experiment_agent_init_and_resources():
    # This should cover agent = Agent(...) and agent.resources = env.resources
    res = prs.run_experiment(episodes=1, seed=1, risk_scale=1.0, agent_name='Test', use_pgf=False, use_dqn=False)
    assert 'policy' in res


def test_run_experiment_remember_event():
    # To cover agent.remember(Event())
    res = prs.run_experiment(episodes=1, seed=1, risk_scale=1.0, agent_name='Test', use_pgf=False, use_dqn=False)
    # The remember is called inside the loop


def test_cargar_datos_excel_exception(monkeypatch):
    # To cover the except in the for loop
    import pandas as pd
    invalid_df = pd.DataFrame({
        'Nombre': ['name'],
        'Tipo': ['tipo'],
        'C': ['invalid'],
        'F': ['0.0'],
        'T': ['0.0'],
        'I_op': ['0.0'],
        'Vida (años)': ['0.0'],
        'Tasa (W)': ['0.0'],
        'Complejidad': ['0.0'],
        'P_riesgo físico': ['0.0'],
        'Observaciones': ['obs']
    })
    monkeypatch.setattr(tpex.pd, 'read_csv', lambda *a, **k: invalid_df)
    systems = tpex.cargar_datos_excel('dummy.csv')
    assert systems == []


def test_run_experiment_episodes_zero():
    # To cover the episodes == 0 branch
    res = prs.run_experiment(episodes=0, seed=42, risk_scale=1.0, agent_name="Test", use_pgf=False, use_dqn=False)
    assert res['avg_reward'] == 0.0
    assert res['total_rewards'] == []
    assert res['policy'] == {}


def test_demo_ped_real_plt_show_exception(monkeypatch):
    # To cover the except in plt.show
    def bad_show():
        raise Exception("show error")
    monkeypatch.setattr(mpl_plt, 'show', bad_show)
    # Call demo_ped_real, which has try: plt.show() except: pass
    tpex.demo_ped_real('data/Sistemas_naturales_IA_utf8_limpio.csv')


def test_demo_sensibilidad_real_plt_show_exception(monkeypatch):
    # To cover the except in plt.show in demo_sensibilidad_real
    def bad_show():
        raise Exception("show error")
    monkeypatch.setattr(mpl_plt, 'show', bad_show)
    # Call demo_sensibilidad_real
    tpex.demo_sensibilidad_real('data/Sistemas_naturales_IA_utf8_limpio.csv')


def test_export_to_excel(tmp_path, monkeypatch):
    # To cover export_to_excel lines
    monkeypatch.chdir(tmp_path)
    results = [{'a': 1, 'b': 2}]
    tpex.export_to_excel(results, 'test.csv')
    # Should create file without error


def test_export_to_excel_xlsx(tmp_path, monkeypatch):
    # To cover df.to_excel in export_to_excel
    monkeypatch.chdir(tmp_path)
    results = [{'a': 1, 'b': 2}]
    tpex.export_to_excel(results, 'test.xlsx')
    # Should create file without error


