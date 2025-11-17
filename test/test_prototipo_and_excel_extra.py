from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import types
import matplotlib.pyplot as mpl_plt
import sim.prototipo_rl_simbiosis as prs
import sim.toy_ped_rl_excel as tpex


def test_run_experiment_with_agent_policy_Q(monkeypatch):
    # Create a deterministic Agent subclass with a 'Q' entry in policy
    class MyAgent(prs.Agent):
        def __init__(self, name="Agent", resources=100.0):
            super().__init__(name=name, resources=resources)
            # ensure Q exists to hit q_opt branch in logging
            self.policy = {'Q': np.array([0.1, 0.2, 0.3, 0.4])}
        def act(self, state):
            return 'up'

    monkeypatch.setattr(prs, 'Agent', MyAgent)
    res = prs.run_experiment(episodes=2, seed=1, risk_scale=1.0, agent_name='QA', use_pgf=False, use_dqn=False)
    assert 'avg_reward' in res
    assert isinstance(res['avg_reward'], float)


def test_transfer_test_returns_int():
    policy = {}
    count = prs.transfer_test(policy, seed=2, risk_scale=1.0)
    assert isinstance(count, int)


def test_cargar_datos_excel_invalid_path_returns_empty():
    res = tpex.cargar_datos_excel('this_file_does_not_exist_hopefully.csv')
    assert res == []


def test_demo_ped_real_show_exception_and_save(monkeypatch, tmp_path):
    # Ensure plotting does not write files and plt.show raises to hit except path
    monkeypatch.setattr(mpl_plt, 'savefig', lambda *a, **k: None)
    def raise_on_show():
        raise RuntimeError("no-show")
    monkeypatch.setattr(mpl_plt, 'show', raise_on_show)
    # Call demo_ped_real with empty csv -> load_systems_from_csv returns []
    tpex.demo_ped_real(str(tmp_path / 'no.csv'))


def test_export_to_excel_suppresses_exceptions(monkeypatch, tmp_path):
    # Force pandas.DataFrame to raise when called
    def bad_dataframe(*a, **k):
        raise Exception("pd boom")
    monkeypatch.setattr(tpex.pd, 'DataFrame', bad_dataframe)
    # Should not raise
    tpex.export_to_excel([{'a': 1}], str(tmp_path / 'out.csv'))
