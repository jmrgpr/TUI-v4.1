import torch


def test_runner_high_stakes_budget_terminates(monkeypatch):
    import sim.runner as runner_mod

    class FakeEnv:
        def __init__(self, risk_scale, risk_level, red_team_mode, size=None):
            self.risk_scale = risk_scale
            self.risk_level = risk_level
            self.red_team_mode = red_team_mode
            self.size = size or 2
            self.resources = 1.0
            self.incident_count = 0
            self.goal_pos = (self.size - 1, self.size - 1)

        def reset(self):
            self.resources = 1.0
            return (("coord_x", 0), ("coord_y", 0), ("foo", 1.0))

        def get_abstract_state(self):
            return (("coord_x", 0), ("coord_y", 0), ("foo", 1.0))

        def step(self, _action):
            info = {"starvation": True, "u_proxy": -1.0, "u_humans": -1.0, "gap_proxy_value": 0.0, "is_gaming": False}
            return (("coord_x", 0), ("coord_y", 0), ("foo", 1.0)), -1.0, True, info

    class FakeEval:
        def calcular_metricas(self, _env, _info, step, *_args, **_kwargs):
            return {"PGF": 0.1 + step, "PGF_Bruto": 0.1, "PGF_Costo": 0.0, "F": 0.0, "R_robust": 0.0}

    class FakeAgent:
        def __init__(self, name=None, resources=None):
            self.policy = {}
            self.resources = resources or 1.0
            self.purpose = "p"
            self.alignment = 1.0

        def act(self, _state):
            return "noop"

        def update_policy(self, *_args, **_kwargs):
            return None

        def remember(self, _event):
            return None

        def reprogram_purpose(self, _p):
            self.purpose = _p

    monkeypatch.setattr(runner_mod, "SimbiosisEnv", FakeEnv)
    monkeypatch.setattr(runner_mod, "EvaluatorPGF", FakeEval)
    monkeypatch.setattr(runner_mod, "Agent", FakeAgent)

    result = runner_mod.run_experiment(
        episodes=10,
        seed=1,
        risk_scale=1.2,
        agent_name="Control",
        use_pgf=False,
        use_dqn=False,
        pgf_mix=0.0,
        risk_level="high",
        red_team=False,
        stakes_mode="high",
        catastrophe_budget=1,
    )

    assert result["run_metrics"]["episodes_completed"] == 1
    assert result["run_metrics"]["budget_exhausted"] is True
    assert result["run_metrics"]["terminated_by_budget"] is True
    assert result["run_metrics"]["cfr"] == 1.0

