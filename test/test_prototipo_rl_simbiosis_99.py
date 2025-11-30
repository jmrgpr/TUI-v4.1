import pytest
import os
import sys
import tempfile
from sim import prototipo_rl_simbiosis

def test_main_export_json_and_csv():
    # Test exportación de JSON y CSV en main()
    tmpdir = tempfile.gettempdir()
    export_path = os.path.join(tmpdir, "test_export_99.json")
    sys.argv = ["script", "--episodes", "2", "--seed", "42", "--export", export_path]
    prototipo_rl_simbiosis.main()
    assert os.path.exists(export_path)
    csv_path = export_path.replace(".json", "_episodes.csv")
    assert os.path.exists(csv_path)
    os.remove(export_path)
    os.remove(csv_path)


def test_main_tui_only_branch():
    # Test branch TUI-only en main()
    tmpdir = tempfile.gettempdir()
    export_path = os.path.join(tmpdir, "test_export_tui_only.json")
    sys.argv = ["script", "--episodes", "2", "--seed", "42", "--export", export_path, "--tui_only"]
    prototipo_rl_simbiosis.main()
    assert os.path.exists(export_path)
    os.remove(export_path)
    csv_path = export_path.replace(".json", "_episodes.csv")
    assert os.path.exists(csv_path)
    os.remove(csv_path)


def test_main_dqn_control_branch():
    # Test branch DQN-control en main()
    tmpdir = tempfile.gettempdir()
    export_path = os.path.join(tmpdir, "test_export_dqn_control.json")
    sys.argv = ["script", "--episodes", "2", "--seed", "42", "--export", export_path, "--dqn_control"]
    prototipo_rl_simbiosis.main()
    assert os.path.exists(export_path)
    os.remove(export_path)
    csv_path = export_path.replace(".json", "_episodes.csv")
    assert os.path.exists(csv_path)
    os.remove(csv_path)
