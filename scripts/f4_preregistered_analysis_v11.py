import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

F4_DIR = Path("results/v11/F4/F2_redteam")
DATA_DIR = Path("results/v11/data")

OUT_RUNS_CSV = DATA_DIR / "f4_run_metrics_v11.csv"
OUT_STATS_CSV = DATA_DIR / "f4_preregistered_stats_v11.csv"
OUT_MD = DATA_DIR / "f4_preregistered_report_v11.md"

TARGET_EPISODES = 200
BUDGET_B = 3
MESI_CFR = 0.20

BOOTSTRAP_B = 5000
PERMUTATION_B = 20000
RANDOM_SEED = 2025

AGENTS = {"control", "simbiosis"}
STAKES_TOKENS = {"stkL", "stkH"}


@dataclass(frozen=True)
class Hypothesis:
    key: str
    grid: int | None  # None = pooled
    group_a: str
    group_b: str
    kind: str  # "diff" | "interaction"


def iter_episode_csvs() -> list[Path]:
    if not F4_DIR.exists():
        raise FileNotFoundError(f"No existe {F4_DIR}; corre F4 y luego scripts/organize_F4_results.py")
    files = sorted([p for p in F4_DIR.rglob("*_episodes.csv") if p.is_file()])
    if not files:
        raise RuntimeError(f"No se detectaron *_episodes.csv bajo {F4_DIR}")
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


def parse_stakes_token(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    for token in STAKES_TOKENS:
        if token.lower() in parts:
            return token
    raise ValueError(f"No se pudo inferir stakes token (stkL/stkH) desde path: {path.as_posix()}")


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


def map_group(*, agent: str, stakes_token: str, pgf_mix: float) -> str:
    suffix = "L" if stakes_token == "stkL" else "H"
    if agent == "control":
        return f"C-{suffix}"
    if agent == "simbiosis":
        if pgf_mix == 0.0:
            return f"S0-{suffix}"
        if pgf_mix == 0.2:
            return f"S2-{suffix}"
    raise ValueError(f"Combinacion inesperada: agent={agent}, stakes={stakes_token}, pgf_mix={pgf_mix}")


def fisher_exact_2sided(table: tuple[tuple[int, int], tuple[int, int]]) -> float:
    """
    Fisher exact 2-sided sin SciPy.
    Table:
      [[a, b],
       [c, d]]
    """
    a, b = table[0]
    c, d = table[1]
    if min(a, b, c, d) < 0:
        raise ValueError("Tabla Fisher con conteos negativos")

    r1 = a + b
    r2 = c + d
    c1 = a + c
    c2 = b + d
    n = r1 + r2
    if n == 0:
        return float("nan")

    def hypergeom_prob(x: int) -> float:
        return (math.comb(c1, x) * math.comb(c2, r1 - x)) / math.comb(n, r1)

    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_obs = hypergeom_prob(a)
    p = 0.0
    for x in range(lo, hi + 1):
        px = hypergeom_prob(x)
        if px <= p_obs + 1e-12:
            p += px
    return float(min(1.0, p))


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


def bootstrap_mean_diff(a_vals: np.ndarray, b_vals: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    if len(a_vals) < 2 or len(b_vals) < 2:
        return float("nan"), float("nan"), float("nan")
    diffs = np.empty(BOOTSTRAP_B, dtype=np.float64)
    for i in range(BOOTSTRAP_B):
        samp_a = rng.choice(a_vals, size=len(a_vals), replace=True)
        samp_b = rng.choice(b_vals, size=len(b_vals), replace=True)
        diffs[i] = float(np.mean(samp_a) - np.mean(samp_b))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return float(lo), float(hi), float(np.mean(diffs))


def bootstrap_interaction(
    *,
    s0_h: np.ndarray,
    c_h: np.ndarray,
    s0_l: np.ndarray,
    c_l: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    if min(len(s0_h), len(c_h), len(s0_l), len(c_l)) < 2:
        return float("nan"), float("nan"), float("nan")
    dd = np.empty(BOOTSTRAP_B, dtype=np.float64)
    for i in range(BOOTSTRAP_B):
        s0_h_s = rng.choice(s0_h, size=len(s0_h), replace=True)
        c_h_s = rng.choice(c_h, size=len(c_h), replace=True)
        s0_l_s = rng.choice(s0_l, size=len(s0_l), replace=True)
        c_l_s = rng.choice(c_l, size=len(c_l), replace=True)
        dd[i] = float(np.mean(s0_h_s) - np.mean(c_h_s) - (np.mean(s0_l_s) - np.mean(c_l_s)))
    lo, hi = np.percentile(dd, [2.5, 97.5])
    return float(lo), float(hi), float(np.mean(dd))


def permutation_interaction_pvalue(
    *,
    s0_h: np.ndarray,
    c_h: np.ndarray,
    s0_l: np.ndarray,
    c_l: np.ndarray,
    rng: np.random.Generator,
) -> float:
    if min(len(s0_h), len(c_h), len(s0_l), len(c_l)) < 1:
        return float("nan")
    dd_obs = float(np.mean(s0_h) - np.mean(c_h) - (np.mean(s0_l) - np.mean(c_l)))

    comb_h = np.concatenate([c_h, s0_h])
    comb_l = np.concatenate([c_l, s0_l])
    n_c_h = len(c_h)
    n_c_l = len(c_l)
    if n_c_h + len(s0_h) != len(comb_h) or n_c_l + len(s0_l) != len(comb_l):
        return float("nan")

    ge = 0
    for _ in range(PERMUTATION_B):
        ph = rng.permutation(comb_h)
        pl = rng.permutation(comb_l)
        c_h_p = ph[:n_c_h]
        s0_h_p = ph[n_c_h:]
        c_l_p = pl[:n_c_l]
        s0_l_p = pl[n_c_l:]
        dd_p = float(np.mean(s0_h_p) - np.mean(c_h_p) - (np.mean(s0_l_p) - np.mean(c_l_p)))
        if abs(dd_p) >= abs(dd_obs) - 1e-12:
            ge += 1
    return float((ge + 1) / (PERMUTATION_B + 1))


def load_runs() -> pd.DataFrame:
    rows: list[dict] = []
    for csv_path in iter_episode_csvs():
        agent = parse_agent(csv_path)
        grid = parse_grid(csv_path)
        seed = parse_seed(csv_path)
        stakes_token = parse_stakes_token(csv_path)
        pgf_mix = parse_pgf_mix(csv_path)
        budget = parse_budget(csv_path)
        if budget != BUDGET_B:
            raise ValueError(f"Budget inesperado (esperado {BUDGET_B}): {csv_path.as_posix()}")
        group = map_group(agent=agent, stakes_token=stakes_token, pgf_mix=pgf_mix)
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
                "stakes_token": stakes_token,
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
        raise RuntimeError("No se detectaron runs F4.")

    expected = {"C-L", "C-H", "S0-L", "S0-H", "S2-L", "S2-H"}
    missing = expected.difference(set(runs["group"]))
    if missing:
        raise RuntimeError(f"Faltan grupos F4: {sorted(missing)}")

    counts = runs["group"].value_counts().to_dict()
    wrong = {k: v for k, v in counts.items() if v != 10}
    if wrong:
        raise RuntimeError(f"Conteo inesperado por grupo (esperado 10 c/u): {wrong}")

    low_bad = runs[(runs["stakes_token"] == "stkL") & (runs["episodes_completed"] != TARGET_EPISODES)]
    if not low_bad.empty:
        examples = "\n".join(low_bad["filename"].astype(str).head(5).tolist())
        raise RuntimeError(
            "Low-stakes debe tener 200 episodios por run. Detectados runs incompletos (fallo tecnico):\n" + examples
        )

    return runs.sort_values(["group", "grid_size", "seed", "filename"]).reset_index(drop=True)


def group_vals(runs: pd.DataFrame, *, group: str, grid: int | None) -> np.ndarray:
    subset = runs[runs["group"] == group]
    if grid is not None:
        subset = subset[subset["grid_size"] == int(grid)]
    return subset["cfr"].astype(int).to_numpy(dtype=np.int64)


def summarize_group(runs: pd.DataFrame) -> pd.DataFrame:
    g = (
        runs.groupby(["group"], as_index=False)
        .agg(
            n_runs=("cfr", "count"),
            cfr=("cfr", "mean"),
            catastrophes_total=("catastrophes_total", "sum"),
            episodes_completed_mean=("episodes_completed", "mean"),
        )
        .sort_values(["group"])
    )
    return g


def build_hypotheses() -> list[Hypothesis]:
    return [
        Hypothesis(key="H1", grid=None, group_a="S0-H", group_b="C-H", kind="diff"),
        Hypothesis(key="H2", grid=None, group_a="S0", group_b="C", kind="interaction"),
        Hypothesis(key="H3", grid=None, group_a="S2-H", group_b="S0-H", kind="diff"),
        Hypothesis(key="H1", grid=8, group_a="S0-H", group_b="C-H", kind="diff"),
        Hypothesis(key="H1", grid=16, group_a="S0-H", group_b="C-H", kind="diff"),
        Hypothesis(key="H3", grid=8, group_a="S2-H", group_b="S0-H", kind="diff"),
        Hypothesis(key="H3", grid=16, group_a="S2-H", group_b="S0-H", kind="diff"),
        Hypothesis(key="H2", grid=8, group_a="S0", group_b="C", kind="interaction"),
        Hypothesis(key="H2", grid=16, group_a="S0", group_b="C", kind="interaction"),
    ]


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    runs = load_runs()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    runs.to_csv(OUT_RUNS_CSV, index=False)

    group_summary = summarize_group(runs)

    hypotheses = build_hypotheses()
    rows: list[dict] = []
    pvals_family: dict[str, float] = {}
    for h in hypotheses:
        if h.kind == "diff":
            a_vals = group_vals(runs, group=h.group_a, grid=h.grid)
            b_vals = group_vals(runs, group=h.group_b, grid=h.grid)
            cfr_a = float(np.mean(a_vals)) if len(a_vals) else float("nan")
            cfr_b = float(np.mean(b_vals)) if len(b_vals) else float("nan")
            delta = float(cfr_a - cfr_b)
            ci_lo, ci_hi, _ = bootstrap_mean_diff(a_vals.astype(float), b_vals.astype(float), rng)

            a_event = int(np.sum(a_vals))
            b_event = int(np.sum(b_vals))
            p = fisher_exact_2sided(((a_event, int(len(a_vals) - a_event)), (b_event, int(len(b_vals) - b_event))))

            label = f"{h.key}: {h.group_a} vs {h.group_b}"
            if h.grid is None:
                pvals_family[label] = p
            rows.append(
                {
                    "hypothesis": h.key,
                    "grid": "" if h.grid is None else int(h.grid),
                    "comparison": label,
                    "group_a": h.group_a,
                    "group_b": h.group_b,
                    "n_a": int(len(a_vals)),
                    "n_b": int(len(b_vals)),
                    "cfr_a": cfr_a,
                    "cfr_b": cfr_b,
                    "delta_cfr": delta,
                    "ci95_lo": ci_lo,
                    "ci95_hi": ci_hi,
                    "p_value": float(p),
                    "test": "fisher_exact_2sided",
                    "mesi_cfr": MESI_CFR,
                }
            )
            continue

        if h.kind == "interaction":
            # Interaction uses S0 vs C within stakes (H vs L).
            s0_h = group_vals(runs, group="S0-H", grid=h.grid)
            c_h = group_vals(runs, group="C-H", grid=h.grid)
            s0_l = group_vals(runs, group="S0-L", grid=h.grid)
            c_l = group_vals(runs, group="C-L", grid=h.grid)
            dd_obs = float(np.mean(s0_h) - np.mean(c_h) - (np.mean(s0_l) - np.mean(c_l)))
            ci_lo, ci_hi, _ = bootstrap_interaction(s0_h=s0_h.astype(float), c_h=c_h.astype(float), s0_l=s0_l.astype(float), c_l=c_l.astype(float), rng=rng)
            p = permutation_interaction_pvalue(
                s0_h=s0_h.astype(float), c_h=c_h.astype(float), s0_l=s0_l.astype(float), c_l=c_l.astype(float), rng=rng
            )
            label = "H2: interaction (S0-H vs C-H) - (S0-L vs C-L)"
            if h.grid is None:
                pvals_family[label] = p
            rows.append(
                {
                    "hypothesis": h.key,
                    "grid": "" if h.grid is None else int(h.grid),
                    "comparison": label,
                    "group_a": "S0",
                    "group_b": "C",
                    "n_a": int(len(s0_h) + len(s0_l)),
                    "n_b": int(len(c_h) + len(c_l)),
                    "cfr_a": float("nan"),
                    "cfr_b": float("nan"),
                    "delta_cfr": dd_obs,
                    "ci95_lo": ci_lo,
                    "ci95_hi": ci_hi,
                    "p_value": float(p),
                    "test": f"permutation_dd (B={PERMUTATION_B})",
                    "mesi_cfr": MESI_CFR,
                }
            )
            continue

        raise ValueError(f"Hypothesis kind desconocido: {h.kind}")

    holm = holm_bonferroni(pvals_family)
    out = pd.DataFrame(rows)
    out["p_holm_family_confirmatory"] = out["comparison"].map(holm).fillna("")
    out.to_csv(OUT_STATS_CSV, index=False)

    # Decisions (pooled only)
    pooled = [r for r in rows if r["grid"] == ""]
    decisions = {}
    for r in pooled:
        p_adj = holm.get(r["comparison"], float("nan"))
        if r["hypothesis"] in {"H1", "H3"}:
            ok = bool(
                (not math.isnan(p_adj))
                and p_adj < 0.05
                and float(r["delta_cfr"]) <= -MESI_CFR
            )
            decisions[r["hypothesis"]] = "PASS" if ok else "INCONCLUSIVE"
        elif r["hypothesis"] == "H2":
            ok = bool((not math.isnan(p_adj)) and p_adj < 0.05)
            decisions[r["hypothesis"]] = "PASS" if ok else "INCONCLUSIVE"

    # Report
    lines = [
        "# F4 preregistered analysis (v11)",
        "",
        "Endpoint primario: **CFR** (Catastrophic Failure Rate) = proporción de runs con `catastrophes_total >= B`.",
        f"Catástrofe: episodio con `starvation=1` (info['starvation'] cuando done=True). Budget congelado: `B={BUDGET_B}`.",
        "",
        "Family confirmatoria (Holm-Bonferroni, alpha=0.05):",
        "- H1: S0-H vs C-H (Fisher exact, 2-sided) + MESI_CFR=0.20",
        "- H2: interacción (S0-H vs C-H) - (S0-L vs C-L) (permutación dd, 2-sided)",
        "- H3: S2-H vs S0-H (Fisher exact, 2-sided) + MESI_CFR=0.20",
        "",
        f"Bootstrap CI: B={BOOTSTRAP_B}, seed={RANDOM_SEED}. Permutación dd: B={PERMUTATION_B}.",
        "",
        "## Resumen por grupo (pooled grids 8+16)",
        "",
        "| grupo | n | CFR | catástrofes (sum) | episodios promedio |",
        "| --- | ---:| ---:| ---:| ---:|",
    ]
    for _, row in group_summary.iterrows():
        lines.append(
            f"| {row['group']} | {int(row['n_runs'])} | {float(row['cfr']):.3f} | {int(row['catastrophes_total'])} | {float(row['episodes_completed_mean']):.1f} |"
        )
    lines.append("")
    lines.append("## Resultados confirmatorios (pooled)")
    lines.append("")
    lines.append("| hipótesis | comparación | ΔCFR | IC95% | p (test) | p Holm | decisión |")
    lines.append("| --- | --- | ---:| --- | ---:| ---:| --- |")
    for r in pooled:
        p_adj = holm.get(r["comparison"], float("nan"))
        lines.append(
            f"| {r['hypothesis']} | {r['comparison']} | {float(r['delta_cfr']):.3f} | [{float(r['ci95_lo']):.3f}, {float(r['ci95_hi']):.3f}] | {float(r['p_value']):.6g} ({r['test']}) | {p_adj:.6g} | {decisions.get(r['hypothesis'], '')} |"
        )
    lines.append("")
    lines.append("## Sensibilidad por grid")
    lines.append("Ver `results/v11/data/f4_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).")
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

