import pytest
import sys
from sim import prototipo_rl_simbiosis

def test_main_pgf_kappa_lambda_mix():
    sys.argv = ["script", "--episodes", "1", "--seed", "42", "--pgf_kappa", "0.5", "--pgf_lambda", "0.5", "--pgf_mix", "0.7", "--export", "test_pgf_mix.json"]
    prototipo_rl_simbiosis.main()
    import os
    assert os.path.exists("test_pgf_mix.json")
    os.remove("test_pgf_mix.json")
    csv_path = "test_pgf_mix_episodes.csv"
    assert os.path.exists(csv_path)
    os.remove(csv_path)


def test_main_sigma_thr_gamma_lcb_lambda_gaming():
    sys.argv = ["script", "--episodes", "1", "--seed", "42", "--sigma_thr", "0.1", "--gamma_lcb", "0.1", "--lambda_gaming", "0.1", "--export", "test_sigma_thr.json"]
    prototipo_rl_simbiosis.main()
    import os
    assert os.path.exists("test_sigma_thr.json")
    os.remove("test_sigma_thr.json")
    csv_path = "test_sigma_thr_episodes.csv"
    assert os.path.exists(csv_path)
    os.remove(csv_path)
