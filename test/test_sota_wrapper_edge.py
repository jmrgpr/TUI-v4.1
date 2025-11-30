import pytest
import numpy as np
from sim.sota_wrapper import SimbiosisGymEnv

def test_env_reset_shape_edge():
    env = SimbiosisGymEnv(risk_scale=1.0)
    obs, info = env.reset()
    assert obs.shape == (8,)
    assert isinstance(info, dict)


def test_env_step_shape_edge():
    env = SimbiosisGymEnv(risk_scale=1.0)
    env.reset()
    obs, reward, done, truncated, info = env.step(0)
    assert obs.shape == (8,)
    assert isinstance(reward, (int, float))
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)
    assert 'pgf_neto' in info
    assert 'pgf_bruto' in info
    assert 'pgf_costo' in info
