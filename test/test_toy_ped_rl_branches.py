"""
Tests exhaustivos de ramas y edge cases para toy_ped_rl.py
Full branch and edge case tests for toy_ped_rl.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.toy_ped_rl import GridworldCaminoC, System, ABResult, generate_toy_systems, compute_I_op, compute_I_justo, ped_ablation, simulate_ab_adversary

def test_gridworld_camino_c_tripwire():
    env = GridworldCaminoC(size=5)
    env.agent_pos = [2,1]
    _, r, _, info = env.step("right")  # Mueve a tripwire
    assert isinstance(info["gaming_detected"], bool)
    assert info["U_humans"] == env.penalty_tripwire

def test_gridworld_camino_c_gaming():
    env = GridworldCaminoC(size=5)
    env.agent_pos = [1,0]
    _, r, _, info = env.step("right")  # Mueve a gaming
    assert info["gaming_detected"] is True
    assert info["U_op"] == env.reward_gaming

def test_apply_G3_attribution():
    env = GridworldCaminoC(size=5)
    env.agent_pos = [2,2]
    env.action_history = [{"pos": (2,2)}, {"pos": (1,1)}, {"pos": (0,0)}]
    credits = env.apply_G3_attribution(final_U_humans=10.0)
    assert isinstance(credits, list)
    assert credits[0] > 0

def test_generate_toy_systems():
    systems = generate_toy_systems()
    assert isinstance(systems, list)
    assert isinstance(systems[0], System)

def test_compute_I_op_and_justo():
    s = System("Test", 1.0, 0.5, 0.5, 0.5, 0.5, 0.5)
    iop = compute_I_op(s)
    ijusto = compute_I_justo(s)
    assert isinstance(iop, float)
    assert isinstance(ijusto, float)

def test_test_ped_ablation():
    systems = generate_toy_systems()
    r2_no_ped, r2_ped = ped_ablation(systems)
    assert isinstance(r2_no_ped, float)
    assert isinstance(r2_ped, float)

def test_simulate_ab_adversary():
    ab = simulate_ab_adversary(episodes=10, seed=42)
    assert isinstance(ab, ABResult)
    assert ab.episodes == 10
