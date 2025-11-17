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

def test_pad_trajectories_empty():
    """Cubre la rama if not trajectories en pad_trajectories."""
    from sim.toy_ped_rl import pad_trajectories
    result = pad_trajectories([])
    assert result.shape == (0, 50)

def test_pad_trajectories_normal():
    """Test pad_trajectories with data."""
    from sim.toy_ped_rl import pad_trajectories
    trajectories = [[1,2], [3,4,5,6]]
    result = pad_trajectories(trajectories, max_len=4)
    assert result.shape == (2, 4)
    assert result[0][2] == 0.0  # padded

def test_calculate_pgf():
    """Test calculate_pgf."""
    from sim.toy_ped_rl import calculate_pgf
    result = calculate_pgf(10, 5, 1, 2, {'cost': 1})
    assert result == 10 - 5 - 1  # 4

def test_pearson_correlation():
    """Test pearson_correlation."""
    from sim.toy_ped_rl import pearson_correlation
    x = [1,2,3,4,5]
    y = [2,4,6,8,10]
    result = pearson_correlation(x, y)
    assert abs(result - 1.0) < 1e-6  # perfect correlation

def test_pearson_correlation_zero_denom():
    """Cubre la rama if denom == 0 en pearson_correlation."""
    from sim.toy_ped_rl import pearson_correlation
    x = [1,1,1]
    y = [2,2,2]
    result = pearson_correlation(x, y)
    assert result == 0.0
