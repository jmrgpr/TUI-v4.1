import pandas as pd
from pathlib import Path

from scripts import consolidate_results


def test_consolidate_metadata_and_columns(tmp_path):
    # Crear estructura simulada sweep/seed/agent y CSV con columnas nuevas
    base = tmp_path / "results" / "sweep" / "seed1" / "tui_pgf_light"
    base.mkdir(parents=True, exist_ok=True)
    csv_path = base / "risk1.0_sample.csv"
    df = pd.DataFrame(
        {
            "reward": [1.0],
            "tripwires": [0],
            "steps": [10],
            "risk_level": ["high"],
            "red_team": [True],
            "avg_gap": [0.2],
            "gaming_hits": [1],
            "gating_hits": [1],
            "ipg": [0.5],
            "u_proxy": [1.0],
            "u_humans": [0.8],
            "ope_dr": [0.9],
        }
    )
    df.to_csv(csv_path, index=False)
    out = tmp_path / "master.csv"
    consolidate_results.consolidate_csvs(extra_paths=[tmp_path], output=str(out))
    master = pd.read_csv(out)
    assert master.loc[0, "agent"] == "tui_pgf_light"
    assert master.loc[0, "risk_scale"] == 1.0
    for col in ["risk_level", "red_team", "avg_gap", "gaming_hits", "gating_hits", "ipg", "u_proxy", "u_humans", "ope_dr"]:
        assert col in master.columns
