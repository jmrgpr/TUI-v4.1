import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("results/v11/data")
F2_DIR = Path("results/v11/F2_redteam")
OUT_CSV = DATA_DIR / "bootstrap_stats_v11.csv"
OUT_MD = DATA_DIR / "bootstrap_stats_v11.md"

B = 5000
RANDOM_SEED = 2025
AGENTS = ("control", "dqn_control", "simbiosis")


def parse_risk_scale(path: Path) -> float | None:
    name = path.name.lower()
    match = re.search(r"_r(\d)p(\d)_", name)
    if match:
        return float(match.group(1)) + float(match.group(2)) / 10.0
    return None


def reward_column(df: pd.DataFrame) -> str | None:
    for c in ("Recompensa", "reward_total", "reward"):
        if c in df.columns:
            return c
    for c in df.columns:
        if "recomp" in c.lower() or "reward" in c.lower():
            return c
    return None


def file_mean_reward(csv_path: Path) -> float | None:
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    col = reward_column(df)
    if not col:
        return None
    vals = pd.to_numeric(df[col], errors="coerce").dropna()
    if vals.empty:
        return None
    return float(vals.mean())


def canonical_f2_episode_csvs() -> list[Path]:
    files = []
    for path in F2_DIR.rglob("*_episodes.csv"):
        parts = [p.lower() for p in path.parts]
        if "archived" in parts:
            continue
        if "raw" in parts:
            continue
        agent = path.parent.name
        if agent not in AGENTS:
            continue
        files.append(path)
    return sorted(files)


def bootstrap_mean_diff(a_vals: np.ndarray, b_vals: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float, float]:
    n1 = len(a_vals)
    n2 = len(b_vals)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan"), float("nan"), float("nan")

    obs = float(np.mean(a_vals) - np.mean(b_vals))
    diffs = np.empty(B, dtype=np.float64)
    for i in range(B):
        samp1 = rng.choice(a_vals, size=n1, replace=True)
        samp2 = rng.choice(b_vals, size=n2, replace=True)
        diffs[i] = float(np.mean(samp1) - np.mean(samp2))

    ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
    # p-value for H0: diff == 0 using sign test on bootstrap distribution
    p_left = (np.sum(diffs <= 0) + 1) / (B + 1)
    p_right = (np.sum(diffs >= 0) + 1) / (B + 1)
    p_two = float(2 * min(p_left, p_right))
    p_two = min(p_two, 1.0)
    return obs, float(ci_lo), float(ci_hi), p_two


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    files = canonical_f2_episode_csvs()
    if not files:
        raise RuntimeError(f"No se encontraron CSV canónicos en {F2_DIR} (excluyendo raw/ y archived/).")

    rows = []
    by_risk: dict[float, dict[str, list[float]]] = {}
    for csv_path in files:
        risk = parse_risk_scale(csv_path)
        if risk is None:
            continue
        agent = csv_path.parent.name
        mean_reward = file_mean_reward(csv_path)
        if mean_reward is None:
            continue
        by_risk.setdefault(risk, {}).setdefault(agent, []).append(mean_reward)

    for risk, agent_map in sorted(by_risk.items(), key=lambda x: x[0]):
        ctrl_vals = np.array(agent_map.get("control", []), dtype=np.float64)
        for agent in ("dqn_control", "simbiosis"):
            a_vals = np.array(agent_map.get(agent, []), dtype=np.float64)
            mean_diff, ci_lo, ci_hi, p_boot = bootstrap_mean_diff(a_vals, ctrl_vals, rng)
            rows.append(
                {
                    "phase": "F2_redteam",
                    "risk_scale": risk,
                    "agent": agent,
                    "mean_diff": mean_diff,
                    "ci95_lo": ci_lo,
                    "ci95_hi": ci_hi,
                    "p_boot": p_boot,
                    "n_agent": int(len(a_vals)),
                    "n_control": int(len(ctrl_vals)),
                    "unit": "run_mean_by_file",
                    "B": B,
                }
            )

    out = pd.DataFrame(rows)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    md_lines = [
        "# Bootstrap no parametrico (cluster por seed/run) - v11",
        "",
        "Este bootstrap estima la diferencia de medias vs `control` usando como unidad primaria el promedio por archivo (`*_episodes.csv`).",
        "Se excluyen `results/v11/F2_redteam/raw` y `results/v11/archived` para evitar duplicados.",
        "",
        f"Parametros: B={B}, seed={RANDOM_SEED}.",
        "",
    ]
    if out.empty:
        md_lines.append("No se encontraron datos para generar bootstrap.")
    else:
        md_lines.append(out.to_string(index=False))
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV} and {OUT_MD}")


if __name__ == "__main__":
    main()

