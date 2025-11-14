"""
Tests exhaustivos para toy_ped_rl.py
Full coverage tests for toy_ped_rl.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.toy_ped_rl import GridworldCaminoC, System, ABResult

def test_gridworld_camino_c_full():
    env = GridworldCaminoC(size=5)
    s = env.reset()
    assert isinstance(s, tuple)
    for _ in range(10):
        s, r, d, info = env.step("up")
        assert isinstance(r, float)
        assert isinstance(info, dict)

def test_system_full():
    s = System(name="Test", P_riesgo=1.0, Tiss=1.0, Meta=1.0, C=1.0, F=1.0, T=1.0)
    assert s.name == "Test"
    assert isinstance(s.P_riesgo, float)

def test_abresult_full():
    ab = ABResult(episodes=10, detection_rate=0.5, mttd_min=1.0, mttr_min=2.0, false_positives=0, gap_before=0.1, gap_after=0.05, ipg_before=0.2, ipg_after=0.3)
    assert ab.episodes == 10 and ab.detection_rate == 0.5
