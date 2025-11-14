"""
Tests para toy_ped_rl.py — Simulación toy de PED + A/B adversario
Unit tests for toy_ped_rl.py — PED toy simulation and adversarial A/B
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from sim.toy_ped_rl import GridworldCaminoC, System, ABResult

def test_gridworld_camino_c_init():
    env = GridworldCaminoC(size=5)
    assert env.size == 5
    assert hasattr(env, 'alpha')
    assert hasattr(env, 'beta')

def test_system_dataclass():
    s = System(name="Test", P_riesgo=1.0, Tiss=0.5, Meta=0.5, C=0.5, F=0.5, T=0.5)
    assert s.name == "Test"
    assert s.P_riesgo == 1.0

def test_abresult_dataclass():
    r = ABResult(episodes=10, detection_rate=0.9, mttd_min=1.0, mttr_min=2.0, false_positives=0, gap_before=0.1, gap_after=0.05, ipg_before=0.2, ipg_after=0.1)
    assert r.episodes == 10
    assert r.detection_rate == 0.9
