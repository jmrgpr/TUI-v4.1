import sys
import json
import numpy as np
import torch
import os
import matplotlib.pyplot as mpl_plt

from pathlib import Path
# Ensure workspace root is importable (the package `sim` is a sibling folder)
ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
import sim.prototipo_rl_simbiosis as prs


def test_stringify_policy_various_types():
    # Prep: policy with numpy arrays, torch tensors, nested structures
    policy = {
        'arr': np.array([1, 2, 3]),
        'scalar_t': torch.tensor(2.5),
        'vec_t': torch.tensor([0.1, 0.2]),
        'nested': {'a': np.array([7.0]), 'b': [torch.tensor(1.0), 3]},
        'none': None
    }
    ser = prs.stringify_policy(policy)
    # Ensure serializable types
    assert isinstance(ser, dict)
    assert ser['arr'] == [1, 2, 3]
    # torch scalar becomes float
    assert isinstance(ser['scalar_t'], float)
    # torch vector becomes list
    assert isinstance(ser['vec_t'], list) and all(isinstance(x, float) for x in ser['vec_t'])
    assert ser['nested']['a'] == [7.0]
    assert ser['none'] is None


def test_run_experiment_episodes_zero_returns_empty_sets():
    res = prs.run_experiment(episodes=0, seed=0, risk_scale=1.0, agent_name='EdgeCase', use_pgf=False, use_dqn=False)
    assert res['avg_reward'] == 0.0
    assert res['total_rewards'] == []
    assert res['policy'] == {}


def test_main_risk_sweep_fast_mode_runs(tmp_path, monkeypatch):
    # Run main in fast+risk_sweep mode inside a temp directory to avoid side effects.
    monkeypatch.chdir(tmp_path)
    # Prevent matplotlib from writing files by patching savefig globally
    monkeypatch.setattr(mpl_plt, 'savefig', lambda *a, **k: None)
    # Reduce verbosity of prints by capturing stdout via argv and ensuring fast mode
    orig_argv = sys.argv.copy()
    sys.argv[:] = ['prog', '--fast', '--risk_sweep', '--export', str(tmp_path / 'sweep_out.json')]
    try:
        # This should run without raising
        prs.main()
    finally:
        sys.argv[:] = orig_argv
    # Results directory may have been created; ensure function completed
    assert True
