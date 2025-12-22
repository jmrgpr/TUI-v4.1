import math
import re
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

MASTER_CSV = Path("results/master_results_clean.csv")
DATA_DIR = Path("results/v11/data")
OUT_CSV = DATA_DIR / "f3_preregistered_stats_v11.csv"
OUT_MD = DATA_DIR / "f3_preregistered_report_v11.md"

B = 5000
RANDOM_SEED = 2025


@dataclass(frozen=True)
class Comparison:
    key: str
    condition: str  # F1_highrisk | F2_redteam
    grid: int | None  # None = pooled
    group_a: tuple[str, float]  # (agent, pgf_mix)
    group_b: tuple[str, float]


def parse_condition(path: str) -> str:
    lowered = path.replace("\\", "/").lower()
    if "/f1_highrisk/" in lowered:
        return "F1_highrisk"
    if "/f2_redteam/" in lowered:
        return "F2_redteam"
    raise ValueError(f"No se pudo inferir condición desde filename: {path}")


def parse_grid(path: str) -> int:
    m = re.search(r"grid(\d+)", path.lower())
    if not m:
        raise ValueError(f"No se pudo inferir grid desde filename: {path}")
    return int(m.group(1))


def parse_pgf_mix(path: str) -> float:
    # ..._m0p0_v11_episodes.csv
    m = re.search(r"_m(\d+)p(\d+)_v11_episodes\.csv$", path.lower().replace("\\", "/"))
    if not m:
        raise ValueError(f"No se pudo inferir pgf_mix desde filename: {path}")
    a = int(m.group(1))
    b = int(m.group(2))
    return float(f"{a}.{b}")


def reward_env_evol_sha256(json_path: Path) -> str | None:
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    evol = payload.get("reward_env_evol")
    if not isinstance(evol, list):
        return None
    # Hash estable del contenido (no del JSON completo)
    raw = repr(evol).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def holm_bonferroni(pvals: dict[str, float]) -> dict[str, float]:
    items = [(k, float(v)) for k, v in pvals.items() if not math.isnan(float(v))]
    if not items:
        return {}
    items_sorted = sorted(items, key=lambda x: x[1])
    m = len(items_sorted)
    adjusted: dict[str, float] = {}
    for i, (k, p) in enumerate(items_sorted, start=1):
        adjusted[k] = min(1.0, (m - i + 1) * p)
    return adjusted


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
    p_left = (np.sum(diffs <= 0) + 1) / (B + 1)
    p_right = (np.sum(diffs >= 0) + 1) / (B + 1)
    p_two = float(2 * min(p_left, p_right))
    p_two = min(p_two, 1.0)
    return obs, float(ci_lo), float(ci_hi), p_two


def load_master() -> pd.DataFrame:
    if not MASTER_CSV.exists():
        raise FileNotFoundError(f"No existe {MASTER_CSV}; ejecuta scripts/rebuild_master_from_episodes.py")
    master = pd.read_csv(MASTER_CSV)
    if "filename" not in master.columns:
        raise ValueError("master_results_clean.csv no tiene columna 'filename'")
    if "agent" not in master.columns:
        raise ValueError("master_results_clean.csv no tiene columna 'agent'")
    if "reward_env_total" not in master.columns:
        raise ValueError("master_results_clean.csv no tiene columna 'reward_env_total'")
    return master


def prepare_f3(master: pd.DataFrame) -> pd.DataFrame:
    df = master.copy()
    df["filename_norm"] = df["filename"].astype(str).str.replace("\\\\", "/", regex=True)
    df = df[df["filename_norm"].str.contains("results/v11/F3/", case=False, na=False)].copy()
    if df.empty:
        raise RuntimeError("No se detectaron filas F3 en results/master_results_clean.csv")
    df["condition"] = df["filename_norm"].apply(parse_condition)
    df["grid_size"] = df["filename_norm"].apply(parse_grid)
    df["pgf_mix"] = df["filename_norm"].apply(parse_pgf_mix)
    df["reward_env_total"] = pd.to_numeric(df["reward_env_total"], errors="coerce")
    df = df[df["reward_env_total"].notna()].copy()
    if df.empty:
        raise RuntimeError("F3 no tiene reward_env_total (requiere JSON local para derivación)")
    return df


def group_values(df: pd.DataFrame, *, condition: str, grid: int | None, agent: str, pgf_mix: float) -> np.ndarray:
    subset = df[df["condition"] == condition]
    if grid is not None:
        subset = subset[subset["grid_size"] == grid]
    subset = subset[(subset["agent"] == agent) & (subset["pgf_mix"] == pgf_mix)]
    vals = pd.to_numeric(subset["reward_env_total"], errors="coerce").dropna().to_numpy(dtype=np.float64)
    return vals


def paired_sanity_checks(f3: pd.DataFrame) -> dict:
    """
    Sanity check para el bloque P1 (ablación):
    - Verifica si reward_env_total cambia entre pgf_mix=0.0 y 0.2 (por par seed+grid+condición en simbiosis).
    - Verifica si reward_total cambia (debería, por diseño de shaping cuando pgf_mix>0).
    """
    s = f3[f3["agent"] == "simbiosis"].copy()
    keys = ["condition", "grid_size", "seed"]
    pairs = {}
    for _, row in s.iterrows():
        k = tuple(row[c] for c in keys)
        pairs.setdefault(k, {})[float(row["pgf_mix"])] = row

    env_diffs: list[float] = []
    total_diffs: list[float] = []
    missing = 0
    evol_hash_equal = 0
    evol_hash_missing = 0
    config_mix_mismatch = 0
    for k, v in pairs.items():
        if 0.0 not in v or 0.2 not in v:
            missing += 1
            continue
        r0 = v[0.0]
        r2 = v[0.2]
        env_diffs.append(float(r2["reward_env_total"]) - float(r0["reward_env_total"]))
        total_diffs.append(float(r2["reward_total"]) - float(r0["reward_total"]))

        # Comprobar que los JSON existen y que pgf_mix está aplicado allí.
        # r0/r2["filename"] es una ruta relativa en Windows; el JSON asociado está al lado del CSV.
        p0_csv = Path(str(r0["filename"]))
        p2_csv = Path(str(r2["filename"]))
        p0 = p0_csv.with_name(p0_csv.name.replace("_episodes.csv", ".json"))
        p2 = p2_csv.with_name(p2_csv.name.replace("_episodes.csv", ".json"))
        if not p0.exists() or not p2.exists():
            evol_hash_missing += 1
            continue
        try:
            j0 = json.loads(p0.read_text(encoding="utf-8"))
            j2 = json.loads(p2.read_text(encoding="utf-8"))
            mix0 = float(j0.get("config", {}).get("pgf_mix", -1))
            mix2 = float(j2.get("config", {}).get("pgf_mix", -1))
            if mix0 != 0.0 or mix2 != 0.2:
                config_mix_mismatch += 1
        except Exception:
            evol_hash_missing += 1
            continue
        h0 = reward_env_evol_sha256(p0)
        h2 = reward_env_evol_sha256(p2)
        if h0 is None or h2 is None:
            evol_hash_missing += 1
            continue
        if h0 == h2:
            evol_hash_equal += 1

    env = np.array(env_diffs, dtype=np.float64) if env_diffs else np.array([], dtype=np.float64)
    tot = np.array(total_diffs, dtype=np.float64) if total_diffs else np.array([], dtype=np.float64)
    return {
        "pairs_total": int(len(pairs)),
        "pairs_missing": int(missing),
        "env_diff_min": float(np.min(env)) if env.size else float("nan"),
        "env_diff_max": float(np.max(env)) if env.size else float("nan"),
        "env_diff_mean": float(np.mean(env)) if env.size else float("nan"),
        "env_diff_unique_rounded_12": int(len(set([round(float(x), 12) for x in env_diffs])) if env_diffs else 0),
        "total_diff_min": float(np.min(tot)) if tot.size else float("nan"),
        "total_diff_max": float(np.max(tot)) if tot.size else float("nan"),
        "total_diff_mean": float(np.mean(tot)) if tot.size else float("nan"),
        "evol_hash_equal": int(evol_hash_equal),
        "evol_hash_missing": int(evol_hash_missing),
        "config_mix_mismatch": int(config_mix_mismatch),
    }


def comparisons() -> list[Comparison]:
    comps: list[Comparison] = []
    # pooled comparisons (grid=None)
    comps.extend(
        [
            Comparison("F1:m0p0_simbiosis_vs_control", "F1_highrisk", None, ("simbiosis", 0.0), ("control", 0.0)),
            Comparison("F1:m0p0_simbiosis_vs_dqn_control", "F1_highrisk", None, ("simbiosis", 0.0), ("dqn_control", 0.0)),
            Comparison("F2:m0p0_simbiosis_vs_control", "F2_redteam", None, ("simbiosis", 0.0), ("control", 0.0)),
            Comparison("F2:m0p0_simbiosis_vs_dqn_control", "F2_redteam", None, ("simbiosis", 0.0), ("dqn_control", 0.0)),
            Comparison("F1:pgf_ablation_m0p2_vs_m0p0", "F1_highrisk", None, ("simbiosis", 0.2), ("simbiosis", 0.0)),
            Comparison("F2:pgf_ablation_m0p2_vs_m0p0", "F2_redteam", None, ("simbiosis", 0.2), ("simbiosis", 0.0)),
        ]
    )
    # sensitivity by grid
    for grid in (8, 16):
        comps.extend(
            [
                Comparison(f"grid{grid}:F1:m0p0_simbiosis_vs_control", "F1_highrisk", grid, ("simbiosis", 0.0), ("control", 0.0)),
                Comparison(f"grid{grid}:F1:m0p0_simbiosis_vs_dqn_control", "F1_highrisk", grid, ("simbiosis", 0.0), ("dqn_control", 0.0)),
                Comparison(f"grid{grid}:F2:m0p0_simbiosis_vs_control", "F2_redteam", grid, ("simbiosis", 0.0), ("control", 0.0)),
                Comparison(
                    f"grid{grid}:F2:m0p0_simbiosis_vs_dqn_control", "F2_redteam", grid, ("simbiosis", 0.0), ("dqn_control", 0.0)
                ),
                Comparison(f"grid{grid}:F1:pgf_ablation_m0p2_vs_m0p0", "F1_highrisk", grid, ("simbiosis", 0.2), ("simbiosis", 0.0)),
                Comparison(f"grid{grid}:F2:pgf_ablation_m0p2_vs_m0p0", "F2_redteam", grid, ("simbiosis", 0.2), ("simbiosis", 0.0)),
            ]
        )
    return comps


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)

    master = load_master()
    f3 = prepare_f3(master)
    sanity = paired_sanity_checks(f3)

    rows = []
    pvals_primary: dict[str, float] = {}
    for comp in comparisons():
        a_agent, a_mix = comp.group_a
        b_agent, b_mix = comp.group_b
        a_vals = group_values(f3, condition=comp.condition, grid=comp.grid, agent=a_agent, pgf_mix=a_mix)
        b_vals = group_values(f3, condition=comp.condition, grid=comp.grid, agent=b_agent, pgf_mix=b_mix)
        mean_diff, ci_lo, ci_hi, p_two = bootstrap_mean_diff(a_vals, b_vals, rng)
        row = {
            "comparison": comp.key,
            "condition": comp.condition,
            "grid": "" if comp.grid is None else int(comp.grid),
            "metric": "reward_env_total",
            "group_a": f"{a_agent} (pgf_mix={a_mix})",
            "group_b": f"{b_agent} (pgf_mix={b_mix})",
            "n_a": int(len(a_vals)),
            "n_b": int(len(b_vals)),
            "mean_diff": mean_diff,
            "ci95_lo": ci_lo,
            "ci95_hi": ci_hi,
            "p_bootstrap_two_sided": p_two,
        }
        rows.append(row)
        if comp.grid is None and comp.key.startswith(("F1:", "F2:")):
            pvals_primary[comp.key] = p_two

    df_out = pd.DataFrame(rows)
    holm = holm_bonferroni(pvals_primary)
    df_out["p_holm_family_primary"] = df_out["comparison"].map(holm).fillna("")
    df_out.to_csv(OUT_CSV, index=False)

    # Minimal report
    primary_rows = [r for r in rows if r["grid"] == "" and r["comparison"] in pvals_primary]
    lines = [
        "# F3 preregistered analysis (v11)",
        "",
        "Metrica primaria: `reward_env_total` (por run/seed; derivada de JSON `reward_env_evol`).",
        "",
        "Family primaria (Holm-Bonferroni, alpha=0.05, two-sided, M=6):",
        "- F1: simbiosis(m=0.0) vs control",
        "- F1: simbiosis(m=0.0) vs dqn_control",
        "- F2: simbiosis(m=0.0) vs control",
        "- F2: simbiosis(m=0.0) vs dqn_control",
        "- F1: simbiosis(m=0.2) vs simbiosis(m=0.0)",
        "- F2: simbiosis(m=0.2) vs simbiosis(m=0.0)",
        "",
        f"Bootstrap: B={B}, seed={RANDOM_SEED}.",
        "",
        "## Resultados (pooled grids 8+16)",
        "",
        "| comparacion | nA | nB | delta media (A-B) | IC95% | p (2-sided) | p Holm (family) |",
        "| --- | ---:| ---:| ---:| --- | ---:| ---:|",
    ]
    for r in primary_rows:
        p_holm = holm.get(r["comparison"], float("nan"))
        lines.append(
            f"| {r['comparison']} | {r['n_a']} | {r['n_b']} | {r['mean_diff']:.6g} | [{r['ci95_lo']:.6g}, {r['ci95_hi']:.6g}] | {r['p_bootstrap_two_sided']:.6g} | {p_holm:.6g} |"
        )
    lines.append("")
    lines.append("## Sensibilidad por grid")
    lines.append("Ver `results/v11/data/f3_preregistered_stats_v11.csv` (incluye filas por grid8 y grid16).")
    lines.append("")
    lines.append("## Sanity check (ablacion pgf_mix)")
    lines.append("")
    lines.append("Este bloque verifica la preocupacion clasica de peer review: si el delta=0 en la ablacion es un artefacto.")
    lines.append("Se calcula por pares (condicion, grid, seed) en `simbiosis`, comparando `pgf_mix=0.2` vs `pgf_mix=0.0`:")
    lines.append("")
    lines.append(
        f"- Pares esperados (condicion x grid x seed): {sanity['pairs_total']} (missing={sanity['pairs_missing']})"
    )
    lines.append(
        f"- reward_env_total diff (m0.2 - m0.0): min={sanity['env_diff_min']:.6g}, max={sanity['env_diff_max']:.6g}, mean={sanity['env_diff_mean']:.6g}, unique_diffs~={sanity['env_diff_unique_rounded_12']}"
    )
    lines.append(
        f"- reward_total diff (m0.2 - m0.0): min={sanity['total_diff_min']:.6g}, max={sanity['total_diff_max']:.6g}, mean={sanity['total_diff_mean']:.6g}"
    )
    lines.append(
        f"- JSON check (por par): reward_env_evol sha256 iguales={sanity['evol_hash_equal']}, missing/parse_fail={sanity['evol_hash_missing']}, config_pgf_mix_mismatch={sanity['config_mix_mismatch']}"
    )
    lines.append("")
    lines.append(
        "Interpretacion: en esta implementacion, `pgf_mix` cambia fuertemente `reward_total` (shaping) pero no altera `reward_env_total` para los mismos seeds/grids/condicion, por lo que la ablacion sobre `reward_env_total` produce delta=0."
    )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Escrito: {OUT_CSV}")
    print(f"[OK] Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()
