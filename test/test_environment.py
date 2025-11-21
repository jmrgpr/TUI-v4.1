import pytest
from sim.environment import SimbiosisEnv

def test_env_initialization():
    env = SimbiosisEnv()
    assert env is not None
    assert hasattr(env, 'reset')
    assert hasattr(env, 'step')

def test_env_reset_and_step():
    env = SimbiosisEnv()
    state = env.reset()
    assert state is not None
    action = 0
    next_state, reward, done, info = env.step(action)
    assert isinstance(next_state, (list, tuple)) or next_state is not None
    assert isinstance(reward, (int, float))
    assert isinstance(done, bool)
    assert isinstance(info, dict)
