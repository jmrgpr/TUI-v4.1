import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("results/v11")
F2_DIR = ROOT / "F2_redteam"
DATA_DIR = ROOT / "data"
OUT_CSV = DATA_DIR / "f2_final_checks.csv"
OUT_MD = DATA_DIR / "f2_final_checks.md"
LEGACY_MD = ROOT / "f2_final_checks.md"

AGENTS = {"control", "dqn_control", "simbiosis"}


def is_canonical_f2_episode_csv(path: Path) -> bool:
    parts = [p.lower() for p in path.parts]
    if "f2_redteam" not in parts:
        return False
    if "raw" in parts or "archived" in parts:
        return False
    if path.parent.name not in AGENTS:
        return False
    return path.name.lower().endswith("_episodes.csv")


def parse_seed(path: Path) -> int | None:
    match = re.search(r"seed(\d+)", path.name.lower())
    return int(match.group(1)) if match else None


def parse_grid(path: Path) -> int | None:
    joined = "/".join(path.parts).lower()
    match = re.search(r"grid(\d+)", joined)
    return int(match.group(1)) if match else None


def compute_pct_tripwires(df: pd.DataFrame) -> float:
    if "Tripwires" not in df.columns:
        return float("nan")
    vals = pd.to_numeric(df["Tripwires"], errors="coerce").fillna(0.0)
    return float(100.0 * (vals > 0).mean())


def main() -> None:
    if not F2_DIR.exists():
        raise FileNotFoundError(f"No existe el directorio de F2: {F2_DIR}")

    files = sorted([p for p in F2_DIR.rglob("*_episodes.csv") if is_canonical_f2_episode_csv(p)])
    if not files:
        raise FileNotFoundError(f"No se encontraron CSV canonicos de F2 bajo {F2_DIR} (excluyendo raw/ y archived/).")

    rows = []
    for csv_path in files:
        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:
            raise RuntimeError(f"No se pudo leer {csv_path}: {exc}") from exc

        agent = csv_path.parent.name
        seed = parse_seed(csv_path)
        grid = parse_grid(csv_path)

        if "Recompensa" not in df.columns:
            raise RuntimeError(f"Columna 'Recompensa' no encontrada en {csv_path}")
        rewards = pd.to_numeric(df["Recompensa"], errors="coerce").dropna()
        if rewards.empty:
            raise RuntimeError(f"Sin recompensas validas en {csv_path}")

        n = int(len(rewards))
        rows.append(
            {
                "file": str(csv_path),
                "agent": agent,
                "seed": seed,
                "grid": grid,
                "n": n,
                "mean_reward": float(rewards.mean()),
                "std_reward": float(rewards.std(ddof=1)) if n > 1 else 0.0,
                "pct_tripwires": compute_pct_tripwires(df),
            }
        )

    df_runs = pd.DataFrame(rows).sort_values(["agent", "grid", "seed"], na_position="last")

    expected_n = float(df_runs["n"].median())
    df_runs["low_n"] = df_runs["n"] < 0.9 * expected_n

    df_runs["z_mean"] = 0.0
    df_runs["z_trip"] = 0.0
    for agent, group in df_runs.groupby("agent"):
        if len(group) >= 2 and group["mean_reward"].std(ddof=0) > 0:
            df_runs.loc[group.index, "z_mean"] = (group["mean_reward"] - group["mean_reward"].mean()) / group["mean_reward"].std(ddof=0)
        if len(group) >= 2 and group["pct_tripwires"].std(ddof=0) > 0:
            df_runs.loc[group.index, "z_trip"] = (group["pct_tripwires"] - group["pct_tripwires"].mean()) / group["pct_tripwires"].std(ddof=0)

    df_runs["outlier"] = (df_runs["z_mean"].abs() > 3) | (df_runs["z_trip"].abs() > 3) | df_runs["low_n"]

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_runs.to_csv(OUT_CSV, index=False)

    flagged = df_runs[df_runs["outlier"]]
    md_lines = [
        "# F2 Final Checks - Canonico (seeds y outliers)",
        "",
        f"Archivos inspeccionados (F2 canonico): {len(files)}",
        "",
        "Exclusiones: `raw/` y `archived/`. Unidad primaria: archivo `*_episodes.csv` (seed/run).",
        "",
        f"Criterios: `low_n` si `n` < 90% de la mediana (mediana={expected_n:.1f}); outlier si |z(mean_reward)|>3 o |z(pct_tripwires)|>3 o `low_n`.",
        "",
        "Tabla por run:",
        "",
        df_runs.to_string(index=False),
        "",
        "Runs marcados como potencialmente problematicos:",
        "",
        ("Ninguno." if flagged.empty else flagged.to_string(index=False)),
        "",
    ]
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    LEGACY_MD.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {OUT_CSV}, {OUT_MD} and {LEGACY_MD}")


if __name__ == "__main__":
    main()

