import numpy as np
from sim.environment import SimbiosisEnv
from sim import config


def test_red_team_move_tripwire(monkeypatch):
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_move_tripwire_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_add_shock_prob", 0.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_block_prob", 0.0)
    env = SimbiosisEnv(red_team_mode=True)
    env.reset()
    _, _, _, info = env.step("noop")
    assert info.get("red_team_action") == "move_tripwire"


def test_red_team_add_shock(monkeypatch):
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_move_tripwire_prob", 0.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_add_shock_prob", 1.0)
    monkeypatch.setitem(config.EXP_CONFIG, "red_team_block_prob", 0.0)
    env = SimbiosisEnv(red_team_mode=True)
    env.reset()
    _, _, _, info = env.step("noop")
    assert info.get("red_team_action") == "add_shock"
