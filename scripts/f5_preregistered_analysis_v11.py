import itertools
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

F5_DIR = Path("results/v11/F5/F2_redteam/stkH")
DATA_DIR = Path("results/v11/data")

OUT_RUNS_CSV = DATA_DIR / "f5_run_metrics_v11.csv"
OUT_STATS_CSV = DATA_DIR / "f5_preregistered_stats_v11.csv"
OUT_MD = DATA_DIR / "f5_preregistered_report_v11.md"

TARGET_EPISODES = 200
BUDGET_B = 3
MESI_EC = 5

BOOTSTRAP_B = 5000
RANDOM_SEED = 2025

AGENTS = {"control", "simbiosis"}


@dataclass(frozen=True)
class Hypothesis:
    key: str
    grid: int | None  # None = pooled
    group_a: str
    group_b: str


def iter_episode_csvs() -> list[Path]:
    if not F5_DIR.exists():
        raise FileNotFoundError(f"No existe {F5_DIR}; corre F5 y luego scripts/organize_F5_results.py")
    files = sorted([p for p in F5_DIR.rglob("*_episodes.csv") if p.is_file()])
    if not files:
        raise RuntimeError(f"No se detectaron *_episodes.csv bajo {F5_DIR}")
    return files


def parse_grid(path: Path) -> int:
    m = re.search(r"grid(\d+)", path.as_posix().lower())
    if not m:
        raise ValueError(f"No se pudo inferir grid desde path: {path.as_posix()}")
    return int(m.group(1))


def parse_seed(path: Path) -> int:
    m = re.search(r"seed(\d+)", path.name.lower())
    if not m:
        raise ValueError(f"No se pudo inferir seed desde filename: {path.name}")
    return int(m.group(1))


def parse_agent(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    for agent in AGENTS:
        if agent.lower() in parts:
            return agent
    raise ValueError(f"No se pudo inferir agente (control/simbiosis) desde path: {path.as_posix()}")


def parse_pgf_mix(path: Path) -> float:
    # ..._m0p2_v11_episodes.csv
    m = re.search(r"_m(\d+)p(\d+)_v11_episodes\.csv$", path.name.lower())
    if not m:
        raise ValueError(f"No se pudo inferir pgf_mix desde filename: {path.name}")
    a = int(m.group(1))
    b = int(m.group(2))
    return float(f"{a}.{b}")


def parse_budget(path: Path) -> int:
    m = re.search(r"_b(\d+)_m\d+p\d+_v11_episodes\.csv$", path.name.lower())
    if not m:
        raise ValueError(f"No se pudo inferir budget B desde filename: {path.name}")
    return int(m.group(1))


def map_group(*, agent: str, pgf_mix: float) -> str:
    if agent == "control":
        return "C-H"
    if agent == "simbiosis":
        if pgf_mix == 0.0:
            return "S0-H"
        if pgf_mix == 0.2:
            return "S2-H"
    raise ValueError(f"Combinacion inesperada: agent={agent}, pgf_mix={pgf_mix}")


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


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, stat: str) -> tuple[float, float]:
    if len(values) < 2:
        return float("nan"), float("nan")
    out = np.empty(BOOTSTRAP_B, dtype=np.float64)
    for i in range(BOOTSTRAP_B):
        samp = rng.choice(values, size=len(values), replace=True)
        if stat == "mean":
            out[i] = float(np.mean(samp))
        elif stat == "median":
            out[i] = float(np.median(samp))
        else:
            raise ValueError(f"stat desconocido: {stat}")
    lo, hi = np.percentile(out, [2.5, 97.5])
    return float(lo), float(hi)


def exact_signflip_pvalue_mean(diffs: np.ndarray) -> float:
    """
    Permutación pareada exacta (sign-flip) sobre mean(diffs), 2-sided.
    Para n<=20, enumerar 2^n combinaciones es barato y evita Monte Carlo.
    """
    n = len(diffs)
    if n == 0:
        return float("nan")
    obs = float(np.mean(diffs))
    total = 0
    extreme = 0
    for signs in itertools.product([-1.0, 1.0], repeat=n):
        total += 1
        m = float(np.mean(diffs * np.array(signs, dtype=np.float64)))
        if abs(m) >= abs(obs) - 1e-12:
            extreme += 1
    return float(extreme / total) if total else float("nan")


def load_runs() -> pd.DataFrame:
    rows: list[dict] = []
    for csv_path in iter_episode_csvs():
        agent = parse_agent(csv_path)
        grid = parse_grid(csv_path)
        seed = parse_seed(csv_path)
        pgf_mix = parse_pgf_mix(csv_path)
        budget = parse_budget(csv_path)
        if budget != BUDGET_B:
            raise ValueError(f"Budget inesperado (esperado {BUDGET_B}): {csv_path.as_posix()}")
        group = map_group(agent=agent, pgf_mix=pgf_mix)
        df = pd.read_csv(csv_path)
        if "Starvation" not in df.columns:
            raise ValueError(f"Falta columna Starvation en {csv_path.as_posix()}")
        starvation = pd.to_numeric(df["Starvation"], errors="coerce").fillna(0).astype(int)
        episodes_completed = int(len(df))
        catastrophes_total = int(starvation.sum())
        budget_exhausted = bool(catastrophes_total >= budget)
        cfr = 1 if budget_exhausted else 0
        rows.append(
            {
                "group": group,
                "grid_size": int(grid),
                "seed": int(seed),
                "agent": agent,
                "pgf_mix": float(pgf_mix),
                "budget": int(budget),
                "episodes_completed": int(episodes_completed),
                "catastrophes_total": int(catastrophes_total),
                "budget_exhausted": int(budget_exhausted),
                "cfr": int(cfr),
                "catastrophe_episodes_rate": float(catastrophes_total / episodes_completed) if episodes_completed else float("nan"),
                "filename": csv_path.as_posix(),
            }
        )

    runs = pd.DataFrame(rows)
    if runs.empty:
        raise RuntimeError("No se detectaron runs F5.")

    expected = {"C-H", "S0-H", "S2-H"}
    missing = expected.difference(set(runs["group"]))
    if missing:
        raise RuntimeError(f"Faltan grupos F5: {sorted(missing)}")

    counts = runs["group"].value_counts().to_dict()
    wrong = {k: v for k, v in counts.items() if v != 10}
    if wrong:
        raise RuntimeError(f"Conteo inesperado por grupo (esperado 10 c/u): {wrong}")

    high_bad = runs[runs["episodes_completed"] > TARGET_EPISODES]
    if not high_bad.empty:
        examples = "\n".join(high_bad["filename"].astype(str).head(5).tolist())
        raise RuntimeError("episodes_completed no puede exceder 200. Ejemplos:\n" + examples)

    return runs.sort_values(["group", "grid_size", "seed", "filename"]).reset_index(drop=True)


def get_metric_by_pair(runs: pd.DataFrame, *, group: str, grid: int | None) -> dict[tuple[int, int], float]:
    subset = runs[runs["group"] == group]
    if grid is not None:
        subset = subset[subset["grid_size"] == int(grid)]
    out: dict[tuple[int, int], float] = {}
    for _, row in subset.iterrows():
        key = (int(row["seed"]), int(row["grid_size"]))
        if key in out:
            raise RuntimeError(f"Duplicado inesperado para {group} seed+grid={key}")
        out[key] = float(row["episodes_completed"])
    return out


def paired_diffs(runs: pd.DataFrame, *, a: str, b: str, grid: int | None) -> np.ndarray:
    a_map = get_metric_by_pair(runs, group=a, grid=grid)
    b_map = get_metric_by_pair(runs, group=b, grid=grid)
    keys = sorted(set(a_map).intersection(set(b_map)))
    if not keys:
        return np.array([], dtype=np.float64)
    diffs = np.array([a_map[k] - b_map[k] for k in keys], dtype=np.float64)
    return diffs


def summarize_group(runs: pd.DataFrame) -> pd.DataFrame:
    g = (
        runs.groupby(["group"], as_index=False)
        .agg(
            n_runs=("episodes_completed", "count"),
            episodes_completed_mean=("episodes_completed", "mean"),
            episodes_completed_median=("episodes_completed", "median"),
            cfr=("cfr", "mean"),
        )
        .sort_values(["group"])
    )
    return g


def build_hypotheses() -> list[Hypothesis]:
    return [
        Hypothesis(key="H1", grid=None, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H3", grid=None, group_a="S2-H", group_b="S0-H"),
        Hypothesis(key="H1", grid=8, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H1", grid=16, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H3", grid=8, group_a="S2-H", group_b="S0-H"),
        Hypothesis(key="H3", grid=16, group_a="S2-H", group_b="S0-H"),
    ]


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    runs = load_runs()
    runs.to_csv(OUT_RUNS_CSV, index=False)

    group_summary = summarize_group(runs)
    hypotheses = build_hypotheses()

    rows: list[dict] = []
    pvals_family: dict[str, float] = {}
    for h in hypotheses:
        diffs = paired_diffs(runs, a=h.group_a, b=h.group_b, grid=h.grid)
        if diffs.size == 0:
            raise RuntimeError(f"Sin pares para {h.key} {h.group_a} vs {h.group_b} (grid={h.grid})")
        mean_diff = float(np.mean(diffs))
        median_diff = float(np.median(diffs))
        ci_mean_lo, ci_mean_hi = bootstrap_ci(diffs, rng, stat="mean")
        ci_med_lo, ci_med_hi = bootstrap_ci(diffs, rng, stat="median")
        p = exact_signflip_pvalue_mean(diffs)

        label = f"{h.key}: {h.group_a} vs {h.group_b}"
        if h.grid is None:
            pvals_family[label] = p

        # Means per group (descriptivo)
        a_vals = list(get_metric_by_pair(runs, group=h.group_a, grid=h.grid).values())
        b_vals = list(get_metric_by_pair(runs, group=h.group_b, grid=h.grid).values())
        rows.append(
            {
                "hypothesis": h.key,
                "grid": "" if h.grid is None else int(h.grid),
                "comparison": label,
                "group_a": h.group_a,
                "group_b": h.group_b,
                "n_pairs": int(len(diffs)),
                "mean_a": float(np.mean(a_vals)) if a_vals else float("nan"),
                "mean_b": float(np.mean(b_vals)) if b_vals else float("nan"),
                "mean_diff": mean_diff,
                "median_diff": median_diff,
                "ci95_mean_lo": ci_mean_lo,
                "ci95_mean_hi": ci_mean_hi,
                "ci95_median_lo": ci_med_lo,
                "ci95_median_hi": ci_med_hi,
                "p_perm_signflip_mean_2sided": float(p),
                "mesi_ec": int(MESI_EC),
            }
        )

    holm = holm_bonferroni(pvals_family)
    out = pd.DataFrame(rows)
    out["p_holm_family_confirmatory"] = out["comparison"].map(holm).fillna("")
    out.to_csv(OUT_STATS_CSV, index=False)

    decisions: dict[str, str] = {}
    for r in rows:
        if r["grid"] != "":
            continue
        p_adj = holm.get(r["comparison"], float("nan"))
        ok = bool((not math.isnan(p_adj)) and p_adj < 0.05 and float(r["mean_diff"]) >= float(MESI_EC))
        decisions[r["hypothesis"]] = "PASS" if ok else "INCONCLUSIVE"

    pooled = [r for r in rows if r["grid"] == ""]
    lines = [
        "# F5 preregistered analysis (v11)",
        "",
        "Endpoint primario: **episodes_completed** (high-stakes `B=3`; mayor = mejor).",
        "Catástrofe: episodio con `starvation=1` (info['starvation'] cuando done=True).",
        "",
        "Family confirmatoria (Holm-Bonferroni, alpha=0.05):",
        "- H1: S0-H vs C-H (permutación pareada sign-flip sobre mean(d), 2-sided) + MESI_EC=5",
        "- H3: S2-H vs S0-H (permutación pareada sign-flip sobre mean(d), 2-sided) + MESI_EC=5",
        "",
        f"Bootstrap CI: B={BOOTSTRAP_B}, seed={RANDOM_SEED}.",
        "",
        "## Resumen por grupo (pooled grids 8+16)",
        "",
        "| grupo | n | episodes_completed (mean) | episodes_completed (median) | CFR (secundario) |",
        "| --- | ---:| ---:| ---:| ---:|",
    ]
    for _, row in group_summary.iterrows():
        lines.append(
            f"| {row['group']} | {int(row['n_runs'])} | {float(row['episodes_completed_mean']):.3g} | {float(row['episodes_completed_median']):.3g} | {float(row['cfr']):.3g} |"
        )
    lines.append("")
    lines.append("## Resultados confirmatorios (pooled)")
    lines.append("")
    lines.append("| hipótesis | comparación | Δmean(A-B) | IC95% mean | Δmedian(A-B) | IC95% median | p (perm) | p Holm | decisión |")
    lines.append("| --- | --- | ---:| --- | ---:| --- | ---:| ---:| --- |")
    for r in pooled:
        p_adj = holm.get(r["comparison"], float("nan"))
        lines.append(
            f"| {r['hypothesis']} | {r['comparison']} | {float(r['mean_diff']):.3g} | [{float(r['ci95_mean_lo']):.3g}, {float(r['ci95_mean_hi']):.3g}] | "
            f"{float(r['median_diff']):.3g} | [{float(r['ci95_median_lo']):.3g}, {float(r['ci95_median_hi']):.3g}] | "
            f"{float(r['p_perm_signflip_mean_2sided']):.6g} | {p_adj:.6g} | {decisions.get(r['hypothesis'], '')} |"
        )
    lines.append("")
    lines.append("## Sensibilidad por grid")
    lines.append("Ver `results/v11/data/f5_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).")
    lines.append("")
    lines.append("## Trazabilidad")
    lines.append(f"- Runs (run-level metrics): `results/v11/data/{OUT_RUNS_CSV.name}`")
    lines.append(f"- Tabla preregistrada: `results/v11/data/{OUT_STATS_CSV.name}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Escrito: {OUT_RUNS_CSV}")
    print(f"[OK] Escrito: {OUT_STATS_CSV}")
    print(f"[OK] Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()

