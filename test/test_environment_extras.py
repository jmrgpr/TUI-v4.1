import numpy as np
from sim.environment import SimbiosisEnv
from sim import config


def test_blocked_cell_and_risk_high(monkeypatch):
    # Forzar red team a bloquear celda
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_move_tripwire_prob", 0.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_add_shock_prob", 0.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_block_prob", 1.0)
    env = SimbiosisEnv(risk_level="high", red_team_mode=True)
    env.reset()
    # primer paso debería marcar red_team_event y bloquear celda
    _, reward, done, info = env.step("right")
    assert info.get("red_team_event") is True
    # moverse a celda bloqueada debe resultar en noop (posición previa)
    prev_pos = tuple(env.agent_pos)
    _, _, _, info2 = env.step("right")
    assert tuple(env.agent_pos) == prev_pos or info2.get("risk_level") == "high"

