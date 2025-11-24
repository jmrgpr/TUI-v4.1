import numpy as np
from sim import config
from sim.runner import _behavior_prob, _target_prob


class AgentWithProbs:
    def behavior_prob(self, state, action):
        return 0.5

    def target_prob(self, state, action):
        return 0.8


class AgentNoProbs:
    pass


class AgentRaise:
    def behavior_prob(self, state, action):
        raise ValueError("fail")

    def target_prob(self, state, action):
        raise ValueError("fail")


def test_behavior_prob_custom():
    agent = AgentWithProbs()
    p = _behavior_prob(agent, state=None, action="up")
    assert p == 0.5


def test_behavior_prob_uniform():
    agent = AgentNoProbs()
    p = _behavior_prob(agent, state=None, action="up")
    assert np.isclose(p, 1.0 / len(config.AGENT_ACTIONS))

def test_behavior_prob_exception():
    agent = AgentRaise()
    p = _behavior_prob(agent, state=None, action="up")
    assert np.isclose(p, 1.0 / len(config.AGENT_ACTIONS))


def test_target_prob_custom():
    agent = AgentWithProbs()
    p = _target_prob(agent, state=None, action="up")
    assert p == 0.8


def test_target_prob_default():
    agent = AgentNoProbs()
    p = _target_prob(agent, state=None, action="up")
    assert p == 1.0

def test_target_prob_exception():
    agent = AgentRaise()
    p = _target_prob(agent, state=None, action="up")
    assert p == 1.0
