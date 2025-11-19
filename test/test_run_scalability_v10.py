import sys
from pathlib import Path

import pandas as pd
import pytest

import scripts.run_scalability_v10 as scal


class DummyEnv:
    def __init__(self, size: int):
        self.size = size

    def reset(self):
        return ("coord_x", 0.0)


class DummyAgent:
    def __init__(self, saved_paths):
        self.saved_paths = saved_paths

    def save(self, path: str):
        self.saved_paths.append(path)


def test_make_agent_regularization_flags():
    agent_reg = scal.make_agent(state_dim=4, action_dim=2, regularization=True)
    assert pytest.approx(agent_reg.optimizer.param_groups[0]["weight_decay"]) == 1e-5
    assert agent_reg.model.dropout is not None
    assert pytest.approx(agent_reg.model.dropout.p) == 0.10

    agent_plain = scal.make_agent(state_dim=4, action_dim=2, regularization=False)
    assert agent_plain.optimizer.param_groups[0]["weight_decay"] == 0.0
    assert agent_plain.model.dropout is None


def _mock_training(monkeypatch, tmp_path: Path, gate_passed: bool = True):
    created = {}

    def fake_create_env(grid_size, max_steps_multiplier):
        created["grid_size"] = grid_size
        created["max_steps_multiplier"] = max_steps_multiplier
        return DummyEnv(grid_size)

    monkeypatch.setattr(scal, "create_env", fake_create_env)
    monkeypatch.setattr(scal, "state_to_vector", lambda state: [0.1, 0.2])

    saved_paths = []
    monkeypatch.setattr(
        scal,
        "make_agent",
        lambda **kwargs: DummyAgent(saved_paths),
    )

    metrics = {
        "success": [1, 0, 1],
        "rewards": [10, 5, 8],
        "steps": [5, 6, 7],
        "resources": [3, 2, 4],
        "epsilon": [0.5, 0.4, 0.3],
        "first_success": 2,
    }

    def fake_train_phase(env, agent, num_episodes, phase_name, gate_threshold):
        assert env.size == 16
        return {
            "metrics": metrics,
            "success_rate": 0.5,
            "last_100_success": 0.5,
            "gate_passed": gate_passed,
            "first_success": 2,
        }

    monkeypatch.setattr(scal, "train_phase", fake_train_phase)

    summary_path = scal.run_scalability(
        grid="16x16",
        seed=7,
        episodes=200,
        output_dir=tmp_path,
        regularization=True,
        config_name="config_F_16x16_reg",
    )

    summary_df = pd.read_csv(summary_path)
    assert summary_df.loc[0, "config"] == "config_F_16x16_reg"
    assert bool(summary_df.loc[0, "gate_passed"]) == gate_passed

    episodes_files = list(tmp_path.glob("scalability_16x16_seed0007_episodes_*.csv"))
    assert len(episodes_files) == 1
    episodes_df = pd.read_csv(episodes_files[0])
    assert list(episodes_df.columns) == list(metrics.keys())

    if gate_passed:
        assert len(saved_paths) == 1
    else:
        assert not saved_paths

    return created


def test_run_scalability_creates_outputs(tmp_path, monkeypatch):
    created = _mock_training(monkeypatch, tmp_path, gate_passed=True)
    assert created["grid_size"] == 16
    assert created["max_steps_multiplier"] == 5.0


def test_run_scalability_skips_model_save_when_gate_fails(tmp_path, monkeypatch):
    _mock_training(monkeypatch, tmp_path, gate_passed=False)


def test_main_routes_config(monkeypatch, tmp_path):
    called = {}

    def fake_run_scalability(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr(scal, "run_scalability", fake_run_scalability)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_scalability_v10.py",
            "--config",
            "E_16x16_noreg",
            "--episodes",
            "123",
            "--seed",
            "9",
            "--output",
            str(tmp_path),
        ],
    )

    scal.main()

    assert called["grid"] == "16x16"
    assert called["regularization"] is False
    assert called["config_name"] == "config_E_16x16_noreg"
    assert called["episodes"] == 123
    assert called["seed"] == 9
    assert str(tmp_path) in str(called["output_dir"])
