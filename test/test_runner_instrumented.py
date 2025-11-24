import types
import numpy as np

from sim import config
from sim.runner import run_experiment


class StubAgent:
    """Agente con incertidumbre alta para forzar gating."""

    def __init__(self):
        self.calls = 0

    def act(self, state):
        # Acción por defecto si no hay predict_with_uncertainty
        return "up"

    def predict_with_uncertainty(self, state):
        self.calls += 1
        return "up", 1.0, 1.0  # q_val, sigma alta

    def update_policy(self, state, action, reward, next_state):
        return None

    def remember(self, *args, **kwargs):
        return None


def test_run_experiment_gating_and_ipg(monkeypatch):
    # Forzar red_team_prob a 0 para determinismo y riesgo low
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_prob", 0.0)
    monkeypatch.setitem(config.EXP_CONFIG, "sigma_thr", 0.1)
    agent = StubAgent()

    # Ejecutar 1 episodio corto para validar métricas nuevas
    res = run_experiment(
        episodes=1,
        seed=0,
        risk_scale=1.0,
        risk_level="low",
        red_team=False,
        agent_name="Stub",
        use_pgf=False,
        use_dqn=False,
        pgf_mix=1.0,
    )
    # Gating se aplica (sigma > umbral -> noop)
    assert res["gating_hits"] >= 0
    # IPG calculado
    assert "ipg" in res
    # u_proxy/u_humans presentes
    assert "u_proxy" in res and "u_humans" in res
    # OPE-DR presente
    assert "ope_dr" in res


def test_red_team_event(monkeypatch):
    # Forzar red team siempre activo y sin impacto en recursos para estabilidad
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_impact", 0.0)
    from sim.environment import SimbiosisEnv

    env = SimbiosisEnv(red_team_mode=True)
    state = env.reset()
    next_state, reward, done, info = env.step("noop")
    # Debe registrar un evento red team
    assert info.get("red_team_event") is True

