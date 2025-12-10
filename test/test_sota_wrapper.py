import pytest
import numpy as np
from sim.sota_wrapper import SimbiosisGymEnv

def test_env_reset_returns_obs_dict():
    env = SimbiosisGymEnv(risk_scale=1.0)
    obs, info = env.reset()
    assert isinstance(obs, np.ndarray)
    assert obs.shape == (8,)
    assert isinstance(info, dict)


def test_env_step_returns_expected_tuple():
    env = SimbiosisGymEnv(risk_scale=1.0)
    env.reset()
    obs, reward, done, truncated, info = env.step(0)
    assert isinstance(obs, np.ndarray)
    assert obs.shape == (8,)
    assert isinstance(reward, (int, float))
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)
    assert 'pgf_neto' in info
    assert 'pgf_bruto' in info
    assert 'pgf_costo' in info


def test_env_action_space():
    env = SimbiosisGymEnv()
    assert env.action_space.n == 4


def test_env_observation_space():
    env = SimbiosisGymEnv()
    assert env.observation_space.shape == (8,)
    assert env.observation_space.low.shape == (8,)
    assert env.observation_space.high.shape == (8,)


def test_env_metrics_consistency():
    env = SimbiosisGymEnv()
    env.reset()
    _, _, _, _, info = env.step(0)
    assert info['pgf_neto'] <= info['pgf_bruto']
    assert info['pgf_costo'] >= 0


def test_env_multiple_steps():
    env = SimbiosisGymEnv()
    env.reset()
    for i in range(4):
        obs, reward, done, truncated, info = env.step(i)
    assert obs.shape == (8,)
    assert isinstance(reward, (int, float))
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)


def test_env_reset_reinitializes_evaluator():
    env = SimbiosisGymEnv()
    env.reset()
    old_evaluator = env.evaluator
    env.reset()
    assert env.evaluator is not old_evaluator
