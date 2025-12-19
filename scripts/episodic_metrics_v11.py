import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("results/v11")
MANIFEST = ROOT / "CANONICAL_DATASET_v11.md"
OUT_DIR = ROOT / "data"

OUT_CSV = OUT_DIR / "episodic_metrics_v11.csv"
OUT_MD = OUT_DIR / "episodic_metrics_v11.md"
OUT_CSV_FULL = OUT_DIR / "episodic_metrics_v11_full.csv"
OUT_MD_FULL = OUT_DIR / "episodic_metrics_v11_full.md"

PHASES = ("F0_baseline", "F1_highrisk", "F2_redteam")


def canonical_episode_csvs() -> list[Path]:
    if not MANIFEST.exists():
        raise FileNotFoundError(f"Manifiesto no encontrado: {MANIFEST}. Ejecuta `python scripts/generate_canonical_dataset_v11.py`.")
    csvs: list[Path] = []
    for line in MANIFEST.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("| F"):
            continue
        match = re.search(r"`([^`]+_episodes\.csv)`", line)
        if not match:
            continue
        csvs.append(Path(match.group(1)))
    return csvs


def detect_phase(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    for phase in PHASES:
        if phase.lower() in parts:
            return phase
    return "untracked"


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    series = pd.Series(values, dtype=float)
    cum = series.cumsum()
    peak = cum.cummax()
    drawdown = peak - cum
    return float(drawdown.max())


def cvar_left(values: np.ndarray, alpha: float = 0.05) -> float:
    if values.size == 0:
        return float("nan")
    vals = values[~np.isnan(values)]
    if vals.size == 0:
        return float("nan")
    k = max(1, int(np.ceil(alpha * vals.size)))
    worst = np.sort(vals)[:k]
    return float(np.mean(worst))


def iqr(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    vals = values[~np.isnan(values)]
    if vals.size == 0:
        return float("nan")
    q75, q25 = np.percentile(vals, [75, 25])
    return float(q75 - q25)


def env_episode_totals_from_json(json_path: Path) -> np.ndarray:
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return np.array([], dtype=np.float64)
    evol = payload.get("reward_env_evol")
    if not isinstance(evol, list) or not evol:
        return np.array([], dtype=np.float64)

    totals: list[float] = []
    for ep in evol:
        if isinstance(ep, list) and ep:
            s = 0.0
            for x in ep:
                try:
                    s += float(x)
                except Exception:
                    pass
            totals.append(s)
        elif isinstance(ep, (int, float)):
            totals.append(float(ep))
    return np.array(totals, dtype=np.float64)


def parse_seed_from_name(name: str) -> int | None:
    match = re.search(r"seed(\d+)", name.lower())
    return int(match.group(1)) if match else None


def parse_grid_from_path(path: Path) -> int | None:
    joined = "/".join(path.parts).lower()
    match = re.search(r"grid(\d+)", joined)
    return int(match.group(1)) if match else None


def compute_run_metrics(csv_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    if "Recompensa" not in df.columns:
        raise RuntimeError(f"Columna 'Recompensa' no encontrada en {csv_path}")
    total_rewards = pd.to_numeric(df["Recompensa"], errors="coerce").dropna().to_numpy(dtype=np.float64)
    tripwires = pd.to_numeric(df["Tripwires"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float64) if "Tripwires" in df.columns else np.array([], dtype=np.float64)

    json_path = csv_path.with_name(csv_path.name.replace("_episodes.csv", ".json"))
    config = {}
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        config = payload.get("config") or {}
    env_rewards = env_episode_totals_from_json(json_path) if json_path.exists() else np.array([], dtype=np.float64)

    phase = detect_phase(csv_path)
    agent = csv_path.parent.name
    grid = config.get("grid_size") if config else None
    seed = config.get("seed") if config else None
    risk_scale = config.get("risk_scale") if config else None
    risk_level = config.get("risk_level") if config else None
    red_team = config.get("red_team") if config else None
    pgf_mix = config.get("pgf_mix") if config else None

    grid = int(grid) if grid is not None else parse_grid_from_path(csv_path)
    seed = int(seed) if seed is not None else parse_seed_from_name(csv_path.name)
    try:
        risk_scale = float(risk_scale) if risk_scale is not None else None
    except Exception:
        risk_scale = None

    pct_tripwires = float(100.0 * (tripwires > 0).mean()) if tripwires.size else float("nan")

    row = {
        "phase": phase,
        "agent": agent,
        "grid_size": grid,
        "seed": seed,
        "risk_scale": risk_scale,
        "risk_level": risk_level,
        "red_team": red_team,
        "pgf_mix": pgf_mix,
        "n_episodes_total": int(total_rewards.size),
        "n_episodes_env": int(env_rewards.size),
        "pct_tripwires": pct_tripwires,
        "mean_reward_total": float(np.mean(total_rewards)) if total_rewards.size else float("nan"),
        "median_reward_total": float(np.median(total_rewards)) if total_rewards.size else float("nan"),
        "iqr_reward_total": iqr(total_rewards),
        "cvar05_reward_total": cvar_left(total_rewards, alpha=0.05),
        "max_drawdown_reward_total": max_drawdown(total_rewards),
        "mean_reward_env_total": float(np.mean(env_rewards)) if env_rewards.size else float("nan"),
        "median_reward_env_total": float(np.median(env_rewards)) if env_rewards.size else float("nan"),
        "iqr_reward_env_total": iqr(env_rewards),
        "cvar05_reward_env_total": cvar_left(env_rewards, alpha=0.05),
        "max_drawdown_reward_env_total": max_drawdown(env_rewards),
        "file": csv_path.as_posix(),
    }
    return row


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df.columns, pd.MultiIndex):
        return df
    df = df.copy()
    df.columns = ["_".join([str(c) for c in col if c]) for col in df.columns.to_flat_index()]
    return df


def main() -> None:
    csvs = canonical_episode_csvs()
    if not csvs:
        raise RuntimeError("No se encontraron CSV canonicos en el manifiesto.")

    rows = []
    for csv_path in csvs:
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV canonico no encontrado: {csv_path}")
        rows.append(compute_run_metrics(csv_path))

    full = pd.DataFrame(rows).sort_values(["phase", "agent", "risk_scale", "grid_size", "seed"], na_position="last")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    full.to_csv(OUT_CSV_FULL, index=False)

    agg = (
        full.groupby(["phase", "agent", "risk_scale"])
        .agg(
            n_runs=("file", "count"),
            pct_tripwires_mean=("pct_tripwires", "mean"),
            mean_reward_total_mean=("mean_reward_total", "mean"),
            mean_reward_total_std=("mean_reward_total", "std"),
            median_reward_total_mean=("median_reward_total", "mean"),
            iqr_reward_total_mean=("iqr_reward_total", "mean"),
            cvar05_reward_total_mean=("cvar05_reward_total", "mean"),
            max_drawdown_reward_total_mean=("max_drawdown_reward_total", "mean"),
            mean_reward_env_total_mean=("mean_reward_env_total", "mean"),
            mean_reward_env_total_std=("mean_reward_env_total", "std"),
            median_reward_env_total_mean=("median_reward_env_total", "mean"),
            iqr_reward_env_total_mean=("iqr_reward_env_total", "mean"),
            cvar05_reward_env_total_mean=("cvar05_reward_env_total", "mean"),
            max_drawdown_reward_env_total_mean=("max_drawdown_reward_env_total", "mean"),
        )
        .reset_index()
    )
    agg = flatten_columns(agg)
    agg.to_csv(OUT_CSV, index=False)

    md_lines = [
        "# Metricas episodicas (agregado por run/seed) - v11",
        "",
        "Este archivo resume metricas calculadas a nivel episodio, pero agregadas por run/seed (unidad primaria = archivo).",
        "Se usan solo CSV canonicos listados en `results/v11/CANONICAL_DATASET_v11.md` (excluye `raw/` y `archived/`).",
        "",
        "Columnas clave:",
        "- `*_reward_total_*`: usa `Recompensa` (recompensa total exportada; puede incluir mezcla con PGF cuando `pgf_mix>0`).",
        "- `*_reward_env_total_*`: usa reward ambiental por episodio estimado desde `reward_env_evol` en el JSON del run.",
        "- `cvar05_*`: promedio del 5% peor (cola izquierda).",
        "",
        agg.to_string(index=False),
        "",
    ]
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")

    md_full_lines = [
        "# Metricas episodicas (por run) - v11",
        "",
        "Tabla por run/seed (una fila por archivo canonico).",
        "",
        full.to_string(index=False),
        "",
    ]
    OUT_MD_FULL.write_text("\n".join(md_full_lines), encoding="utf-8")

    print(f"Wrote {OUT_CSV} and {OUT_MD} (full: {OUT_CSV_FULL}, {OUT_MD_FULL})")


if __name__ == "__main__":
    main()

