from sim.environment import SimbiosisEnv
from sim import config


def test_risk_penalty_high_applied(monkeypatch):
    monkeypatch.setitem(config.EXP_CONFIG, "risk_penalty_high", 50.0)
    env = SimbiosisEnv(risk_level="high", red_team_mode=False)
    env.reset()
    # Forzar terminación
    env.resources = 0
    _, reward, done, info = env.step("noop")
    assert done
    assert info.get("risk_penalty_applied") is True
    assert reward == 49.5
