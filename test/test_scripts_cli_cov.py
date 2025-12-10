import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
import runpy

from scripts.experimentos_previos import consolidate_results, merge_summaries


def _fake_subprocess_run(*args, **kwargs):
    return SimpleNamespace(returncode=0)


def _fake_subprocess_run_fail(*args, **kwargs):
    return SimpleNamespace(returncode=1)


def test_consolidate_results_basic(tmp_path, monkeypatch):
    # Crear CSV mínimo con columnas reward/tripwires/steps
    df = pd.DataFrame(
        {
            "reward": [1.0],
            "tripwires": [0],
            "steps": [10],
            "risk_level": ["high"],
            "red_team": [True],
            "avg_gap": [0.1],
            "gaming_hits": [1],
            "gating_hits": [2],
            "ipg": [0.5],
            "u_proxy": [1.0],
            "u_humans": [0.8],
            "ope_dr": [0.9],
        }
    )
    sample_dir = tmp_path / "sweep" / "seed42" / "tui_pgf_light"
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample = sample_dir / "risk1.0_sample.csv"
    df.to_csv(sample, index=False)
    out = tmp_path / "master.csv"
    consolidate_results.consolidate_csvs(extra_paths=[tmp_path], output=str(out))
    assert out.exists()
    master = pd.read_csv(out)
    # Columnas nuevas deben existir aunque sean NaN
    for col in ["agent", "risk_scale", "avg_gap", "ipg"]:
        assert col in master.columns


def test_merge_summaries(tmp_path):
    # Crear dos summary CSV y fusionar
    df1 = pd.DataFrame({"a": [1], "b": [2]})
    df2 = pd.DataFrame({"a": [3], "b": [4]})
    s1 = tmp_path / "one_summary.csv"
    s2 = tmp_path / "two_summary.csv"
    df1.to_csv(s1, index=False)
    df2.to_csv(s2, index=False)
    out = tmp_path / "merged.csv"
    merge_summaries.merge_summaries(str(tmp_path), str(out))
    merged = pd.read_csv(out)
    assert len(merged) == 2


def test_merge_summaries_main(monkeypatch, tmp_path):
    # Simula __main__ con archivos ficticios
    f = tmp_path / "a_summary.csv"
    f.write_text("x,y\n1,2\n", encoding="utf-8")
    monkeypatch.setattr(merge_summaries.glob, "glob", lambda pattern: [str(f)])
    monkeypatch.setattr(merge_summaries, "merge_summaries", lambda *a, **k: None)
    runpy.run_path(str(Path("scripts/experimentos_previos/merge_summaries.py")), run_name="__main__")


def test_run_ablation_quick_main(monkeypatch, tmp_path):
    import scripts.experimentos_previos.run_ablation_quick as run_ablation_quick
    monkeypatch.setattr(run_ablation_quick, "OUTPUT_BASE", tmp_path)
    monkeypatch.setattr(run_ablation_quick, "LOG_FILE", tmp_path / "log.txt")
    monkeypatch.setattr(run_ablation_quick.subprocess, "run", _fake_subprocess_run)
    sys.argv = ["run_ablation_quick.py", "--test"]
    assert run_ablation_quick.main() == 0


def test_run_full_experiment_main(monkeypatch, tmp_path):
    import scripts.experimentos_previos.run_full_experiment as run_full_experiment
    monkeypatch.setattr(run_full_experiment.subprocess, "run", _fake_subprocess_run)
    monkeypatch.setattr(run_full_experiment.Path, "mkdir", lambda *a, **k: None)
    sys.argv = [
        "run_full_experiment.py",
        "--seeds",
        "1",
        "--episodes_default",
        "1",
        "--episodes_robust",
        "1",
        "--output_base",
        str(tmp_path / "out"),
        "--red_team",
        "--sigma_thr",
        "0.3",
        "--gamma_lcb",
        "2.0",
        "--lambda_gaming",
        "1.0",
    ]
    # No assertions, solo validar que main retorna sin error
    run_full_experiment.main()


def test_run_full_experiment_stop_on_fail(monkeypatch, tmp_path):
    import scripts.experimentos_previos.run_full_experiment as run_full_experiment
    monkeypatch.setattr(run_full_experiment.subprocess, "run", _fake_subprocess_run_fail)
    monkeypatch.setattr(run_full_experiment.Path, "mkdir", lambda *a, **k: None)
    sys.argv = [
        "run_full_experiment.py",
        "--seeds",
        "1",
        "--episodes_default",
        "1",
        "--episodes_robust",
        "1",
        "--output_base",
        str(tmp_path / "out"),
        "--stop_on_fail",
    ]
    with pytest.raises(SystemExit):
        run_full_experiment.main()


def test_run_search_pgf_main(monkeypatch, tmp_path):
    import scripts.experimentos_previos.run_search_pgf as run_search_pgf
    monkeypatch.setattr(run_search_pgf, "OUTPUT_BASE", tmp_path)
    monkeypatch.setattr(run_search_pgf, "LOG_FILE", tmp_path / "log.txt")
    sys.argv = ["run_search_pgf.py"]
    assert run_search_pgf.main() == 0
    # cubrir bloque __main__ pero esperando SystemExit
    with pytest.raises(SystemExit):
        runpy.run_path(str(Path("scripts/run_search_pgf.py")), run_name="__main__")


def test_run_ablation_quick_fail(monkeypatch, tmp_path):
    # Simula fallo en un comando y stop_on_fail no está, debe seguir y devolver 0 con fallidos
    import scripts.experimentos_previos.run_ablation_quick as run_ablation_quick
    monkeypatch.setattr(run_ablation_quick, "OUTPUT_BASE", tmp_path)
    monkeypatch.setattr(run_ablation_quick, "LOG_FILE", tmp_path / "log.txt")
    monkeypatch.setattr(run_ablation_quick.subprocess, "run", _fake_subprocess_run_fail)
    sys.argv = ["run_ablation_quick.py", "--test"]
    # No lanzamos SystemExit, solo verificamos que main retorna 1 (fallidos)
    assert run_ablation_quick.main() == 1
