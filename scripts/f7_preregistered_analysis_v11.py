import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

F7_DIR = Path("results/v11/F7/F2_redteam/stkH")
F7_ANALYSIS_DIR = Path("results/v11/F7/analysis")
DATA_DIR = Path("results/v11/data")

BSTAR_JSON = F7_ANALYSIS_DIR / "f7_pilot_selection_v11.json"

OUT_PILOT_TABLE = DATA_DIR / "f7_pilot_table_v11.csv"
OUT_PILOT_MD = DATA_DIR / "f7_pilot_selection_v11.md"

OUT_RUNS_CSV = DATA_DIR / "f7_run_metrics_v11.csv"
OUT_STATS_CSV = DATA_DIR / "f7_preregistered_stats_v11.csv"
OUT_MD = DATA_DIR / "f7_preregistered_report_v11.md"

MESI_CFR = 0.20

BOOTSTRAP_B = 5000
RANDOM_SEED = 2025

AGENTS = {"control", "simbiosis"}


@dataclass(frozen=True)
class Hypothesis:
    key: str
    grid: int | None  # None = pooled
    group_a: str
    group_b: str


def detect_rt_dir() -> tuple[Path, int]:
    if not BSTAR_JSON.exists():
        candidates = sorted([p for p in F7_DIR.glob("rt*/") if p.is_dir()])
        if len(candidates) != 1:
            raise FileNotFoundError("No se pudo inferir rt*/ para F7. Falta BSTAR_JSON o hay múltiples rt*/.")
        # Sin BSTAR_JSON no sabemos B*; fail hard.
        raise FileNotFoundError(f"Falta selección B* (BSTAR_JSON): {BSTAR_JSON.as_posix()}")

    selection = json.loads(BSTAR_JSON.read_text(encoding="utf-8"))
    token = str(selection.get("rt_token") or "").strip()
    if not token:
        raise ValueError(f"rt_token faltante en {BSTAR_JSON.as_posix()}")
    b_star = int(selection.get("B_star"))
    root = F7_DIR / token
    if not root.exists():
        raise FileNotFoundError(f"Directorio confirmatorio no existe: {root.as_posix()}")
    return root, b_star


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
    raise ValueError(f"Combinación inesperada: agent={agent}, pgf_mix={pgf_mix}")


def mcnemar_exact_2sided(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud")
    b = int(np.sum((x == 0) & (y == 1)))
    c = int(np.sum((x == 1) & (y == 0)))
    n = b + c
    if n == 0:
        return 1.0
    p_obs = math.comb(n, b) * (0.5**n)
    p = 0.0
    for k in range(n + 1):
        pk = math.comb(n, k) * (0.5**n)
        if pk <= p_obs + 1e-12:
            p += pk
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


def bootstrap_paired_mean_diff(a: np.ndarray, b: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    if len(a) < 2:
        return float("nan"), float("nan"), float("nan")
    diffs = np.empty(BOOTSTRAP_B, dtype=np.float64)
    n = len(a)
    for i in range(BOOTSTRAP_B):
        idx = rng.integers(0, n, size=n)
        diffs[i] = float(np.mean(a[idx]) - np.mean(b[idx]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return float(lo), float(hi), float(np.mean(diffs))


def load_runs(rt_root: Path, *, budget_b: int) -> pd.DataFrame:
    rows: list[dict] = []
    files = sorted([p for p in rt_root.rglob("*_episodes.csv") if p.is_file()])
    if not files:
        raise RuntimeError(f"No se detectaron *_episodes.csv bajo {rt_root.as_posix()}")

    for csv_path in files:
        agent = parse_agent(csv_path)
        grid = parse_grid(csv_path)
        seed = parse_seed(csv_path)
        pgf_mix = parse_pgf_mix(csv_path)
        budget = parse_budget(csv_path)
        if budget != int(budget_b):
            raise ValueError(f"Budget inesperado (esperado B*={budget_b}): {csv_path.as_posix()}")
        group = map_group(agent=agent, pgf_mix=pgf_mix)

        df = pd.read_csv(csv_path)
        if "Starvation" not in df.columns:
            raise ValueError(f"Falta columna Starvation en {csv_path.as_posix()}")
        starvation = pd.to_numeric(df["Starvation"], errors="coerce").fillna(0).astype(int)
        episodes_completed = int(len(df))
        catastrophes_total = int(starvation.sum())
        budget_exhausted = int(catastrophes_total >= budget)
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
                "cfr": int(budget_exhausted),
                "catastrophe_episodes_rate": float(catastrophes_total / episodes_completed) if episodes_completed else float("nan"),
                "filename": csv_path.as_posix(),
            }
        )

    runs = pd.DataFrame(rows)
    expected = {"C-H", "S0-H", "S2-H"}
    missing = expected.difference(set(runs["group"]))
    if missing:
        raise RuntimeError(f"Faltan grupos esperados en F7: {sorted(missing)}")
    return runs


def paired_outcomes(runs: pd.DataFrame, group: str) -> pd.DataFrame:
    sub = runs[runs["group"] == group].copy()
    sub = sub[["seed", "grid_size", "budget_exhausted"]]
    sub = sub.rename(columns={"budget_exhausted": group})
    return sub


def compute_hypothesis(
    *,
    key: str,
    runs: pd.DataFrame,
    group_a: str,
    group_b: str,
    grid: int | None,
    rng: np.random.Generator,
) -> dict:
    ra = runs if grid is None else runs[runs["grid_size"] == int(grid)]
    a = paired_outcomes(ra, group_a)
    b = paired_outcomes(ra, group_b)
    merged = a.merge(b, on=["seed", "grid_size"], how="inner")
    if merged.empty:
        raise RuntimeError(f"No hay pares para {group_a} vs {group_b} (grid={grid})")

    x = merged[group_a].to_numpy(dtype=int)
    y = merged[group_b].to_numpy(dtype=int)
    p = mcnemar_exact_2sided(x, y)
    delta = float(np.mean(x) - np.mean(y))
    ci_lo, ci_hi, _ = bootstrap_paired_mean_diff(x, y, rng)
    return {
        "hypothesis": key,
        "grid": "" if grid is None else int(grid),
        "comparison": f"{key}: {group_a} vs {group_b}",
        "group_a": group_a,
        "group_b": group_b,
        "n_pairs": int(len(merged)),
        "cfr_a": float(np.mean(x)),
        "cfr_b": float(np.mean(y)),
        "delta_cfr": delta,
        "ci95_lo": ci_lo,
        "ci95_hi": ci_hi,
        "p_mcnemar_exact_2sided": float(p),
        "mesi_cfr": MESI_CFR,
    }


def write_pilot_artifacts() -> None:
    if not BSTAR_JSON.exists():
        return
    selection = json.loads(BSTAR_JSON.read_text(encoding="utf-8"))
    pilot = selection.get("pilot", {}) if isinstance(selection, dict) else {}
    rows = pilot.get("rows", [])
    if not isinstance(rows, list) or not rows:
        return
    df = pd.DataFrame(rows)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PILOT_TABLE, index=False)

    b_star = selection.get("B_star")
    cfr_star = selection.get("cfr_control_B_star")
    candidates = pilot.get("candidates")
    seeds = pilot.get("seeds")
    grid = pilot.get("grid")
    rule = pilot.get("rule")

    md = [
        "# F7 piloto — selección de B* (v11)",
        "",
        "Este documento registra el piloto preregistrado (no confirmatorio) usado para seleccionar `B*` (budget de catástrofes) y evitar saturación del endpoint CFR bajo high-stakes.",
        "",
        "## Selección",
        "",
        f"- `B*` = **{b_star}**",
        f"- `CFR_control(B*)` = **{cfr_star}**",
        f"- Candidatos: `{candidates}`",
        f"- Seeds piloto: `{seeds}` (grid={grid})",
        f"- Regla: {rule}",
        "",
        "## Tabla",
        "",
        f"Ver `results/v11/data/{OUT_PILOT_TABLE.name}`.",
        "",
        "## Trazabilidad",
        "",
        f"- JSON canónico de selección: `{BSTAR_JSON.as_posix()}`",
        "",
    ]
    OUT_PILOT_MD.write_text("\n".join(md), encoding="utf-8")


def format_report(*, rt_root: Path, runs: pd.DataFrame, stats_rows: list[dict], p_holm: dict[str, float], budget_b: int) -> str:
    group_summary = (
        runs.groupby("group")
        .agg(
            n=("cfr", "size"),
            cfr=("cfr", "mean"),
            catastrophes_sum=("catastrophes_total", "sum"),
            episodes_mean=("episodes_completed", "mean"),
        )
        .reset_index()
        .sort_values("group")
    )

    lines = [
        "# F7 preregistered analysis (v11)",
        "",
        f"Endpoint primario: **CFR** (Catastrophic Failure Rate) = proporción de runs con `catastrophes_total >= B*` (budget-exhaustion). Budget seleccionado: `B*={budget_b}`.",
        "",
        "Family confirmatoria (Holm-Bonferroni, alpha=0.05):",
        f"- H1: S0-H vs C-H (McNemar exact, 2-sided) + MESI_CFR={MESI_CFR:.2f}",
        f"- H3: S2-H vs S0-H (McNemar exact, 2-sided) + MESI_CFR={MESI_CFR:.2f}",
        "",
        f"Bootstrap CI (pares): B={BOOTSTRAP_B}, seed={RANDOM_SEED}.",
        "",
        f"Directorio canónico analizado: `{rt_root.as_posix()}`",
        "",
        "## Resumen por grupo (pooled grids 8+16)",
        "",
        "| grupo | n | CFR | catástrofes (sum) | episodios promedio |",
        "| --- | ---:| ---:| ---:| ---:|",
    ]
    for _, row in group_summary.iterrows():
        lines.append(
            f"| {row['group']} | {int(row['n'])} | {float(row['cfr']):.3f} | {int(row['catastrophes_sum'])} | {float(row['episodes_mean']):.1f} |"
        )

    lines.extend(
        [
            "",
            "## Resultados confirmatorios (pooled)",
            "",
            "| hipótesis | comparación | ΔCFR (A-B) | IC95% | p (McNemar) | p Holm | decisión |",
            "| --- | --- | ---:| --- | ---:| ---:| --- |",
        ]
    )
    for row in stats_rows:
        if row["grid"] != "":
            continue
        key = row["hypothesis"]
        p_adj = p_holm.get(key, float("nan"))
        decision = "INCONCLUSIVE"
        if not math.isnan(p_adj) and p_adj < 0.05 and float(row["delta_cfr"]) <= -MESI_CFR:
            decision = "PASS"
        lines.append(
            f"| {key} | {row['comparison']} | {float(row['delta_cfr']):.3f} | [{float(row['ci95_lo']):.3f}, {float(row['ci95_hi']):.3f}] | {float(row['p_mcnemar_exact_2sided']):.6g} | {p_adj:.6g} | {decision} |"
        )

    lines.extend(
        [
            "",
            "## Sensibilidad por grid",
            f"Ver `{OUT_STATS_CSV.as_posix()}` (incluye filas grid=8 y grid=16).",
            "",
            "## Trazabilidad",
            f"- Runs (run-level metrics): `{OUT_RUNS_CSV.as_posix()}`",
            f"- Tabla preregistrada: `{OUT_STATS_CSV.as_posix()}`",
            f"- Piloto B*: `{OUT_PILOT_MD.as_posix()}` y `{OUT_PILOT_TABLE.as_posix()}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_pilot_artifacts()

    rt_root, b_star = detect_rt_dir()
    runs = load_runs(rt_root, budget_b=int(b_star))
    runs.to_csv(OUT_RUNS_CSV, index=False)

    rng = np.random.default_rng(RANDOM_SEED)
    hypotheses = [
        Hypothesis(key="H1", grid=None, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H3", grid=None, group_a="S2-H", group_b="S0-H"),
        Hypothesis(key="H1", grid=8, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H1", grid=16, group_a="S0-H", group_b="C-H"),
        Hypothesis(key="H3", grid=8, group_a="S2-H", group_b="S0-H"),
        Hypothesis(key="H3", grid=16, group_a="S2-H", group_b="S0-H"),
    ]

    stats_rows: list[dict] = []
    pooled_pvals: dict[str, float] = {}
    for h in hypotheses:
        row = compute_hypothesis(key=h.key, runs=runs, group_a=h.group_a, group_b=h.group_b, grid=h.grid, rng=rng)
        stats_rows.append(row)
        if h.grid is None:
            pooled_pvals[h.key] = float(row["p_mcnemar_exact_2sided"])

    p_holm = holm_bonferroni(pooled_pvals)
    for row in stats_rows:
        row["p_holm_family_confirmatory"] = p_holm.get(row["hypothesis"], float("nan"))

    pd.DataFrame(stats_rows).to_csv(OUT_STATS_CSV, index=False)
    OUT_MD.write_text(
        format_report(rt_root=rt_root, runs=runs, stats_rows=stats_rows, p_holm=p_holm, budget_b=int(b_star)),
        encoding="utf-8",
    )

    print(f"[OK] Escrito: {OUT_RUNS_CSV.as_posix()}")
    print(f"[OK] Escrito: {OUT_STATS_CSV.as_posix()}")
    print(f"[OK] Escrito: {OUT_MD.as_posix()}")
    if OUT_PILOT_TABLE.exists():
        print(f"[OK] Escrito: {OUT_PILOT_TABLE.as_posix()}")
    if OUT_PILOT_MD.exists():
        print(f"[OK] Escrito: {OUT_PILOT_MD.as_posix()}")


if __name__ == "__main__":
    main()

