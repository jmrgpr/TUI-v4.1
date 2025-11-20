import os
import sys
import json
import tempfile
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import torch
from sim.dqn_agent import DQNAgent
from sim.prototipo_rl_simbiosis import Agent


def test_target_network_exists_and_updates():
    agent = DQNAgent(state_dim=4, action_dim=2, batch_size=2, memory_size=10, target_update_freq=1)
    # fill memory with two transitions to allow a learn step
    for _ in range(2):
        s = np.zeros(4)
        a = 0
        r = 0.0
        ns = np.zeros(4)
        d = 0
        agent.remember(s, a, r, ns, d)
    # capture state dicts
    before_model = {k: v.clone() for k, v in agent.model.state_dict().items()}
    before_target = {k: v.clone() for k, v in agent.target_model.state_dict().items()}
    # run learn which should update model and then copy to target (freq=1)
    agent.learn()
    # After learn and update, target should equal model
    for k in agent.model.state_dict():
        assert torch.allclose(agent.model.state_dict()[k], agent.target_model.state_dict()[k])


def test_load_policy_safe_tempfile():
    # create a dummy Agent and a policy file with tuple keys serialized as strings
    a = Agent(name='test')
    policy = {"(1, 2)": 0.5, "(0, 0)": 1.0}
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    with open(path, 'w') as f:
        json.dump(policy, f)
    # load policy
    a.load_policy(path)
    # keys should be tuples, not raw strings
    assert (1, 2) in a.policy
    assert (0, 0) in a.policy
    os.remove(path)
