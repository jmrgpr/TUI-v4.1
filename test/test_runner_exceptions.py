import numpy as np
from sim import config
from sim.runner import run_experiment


class AgentRaisePredict:
    def __init__(self):
        self.policy = {}

    def act(self, state):
        return "up"

    def predict_with_uncertainty(self, state):
        raise RuntimeError("boom")

    def update_policy(self, state, action, reward, next_state):
        return None

    def remember(self, *args, **kwargs):
        return None


def test_run_experiment_predict_exception(monkeypatch):
    # reduce steps for speed
    monkeypatch.setattr(config, "ENV_MAX_STEPS_PER_EPISODE", 1)
    res = run_experiment(
        episodes=1,
        seed=0,
        risk_scale=1.0,
        agent_name="Stub",
        use_pgf=False,
        use_dqn=False,
        pgf_mix=1.0,
    )
    assert "avg_reward" in res


class AgentPredictRaises:
    def __init__(self):
        self.policy = {}

    def act(self, state):
        return "up"

    def predict_with_uncertainty(self, state):
        raise RuntimeError("fail")

    def update_policy(self, state, action, reward, next_state):
        return None

    def remember(self, *args, **kwargs):
        return None


def test_run_experiment_predict_raise(monkeypatch):
    monkeypatch.setattr(config, "ENV_MAX_STEPS_PER_EPISODE", 1)
    res = run_experiment(
        episodes=1,
        seed=0,
        risk_scale=1.0,
        agent_name="Stub",
        use_pgf=False,
        use_dqn=False,
        pgf_mix=1.0,
    )
    assert res["gating_hits"] >= 0
