import math
import re
from pathlib import Path
from statistics import NormalDist

import pandas as pd

MASTER_CSV = Path("results/master_results_clean.csv")
OUT_CSV = Path("results/v11/data/f3_power_analysis_v11.csv")
OUT_MD = Path("results/v11/data/f3_power_analysis_v11.md")

ALPHA = 0.05
M_FAMILY = 6
MESI_FRAC = 0.05  # 5% del baseline (según prereg)


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
    m = re.search(r"_m(\d+)p(\d+)_v11_episodes\.csv$", path.lower().replace("\\", "/"))
    if not m:
        raise ValueError(f"No se pudo inferir pgf_mix desde filename: {path}")
    a = int(m.group(1))
    b = int(m.group(2))
    return float(f"{a}.{b}")


def power_two_sample_z(effect: float, se: float, alpha: float) -> float:
    if se <= 0 or not math.isfinite(se) or not math.isfinite(effect):
        return float("nan")
    nd = NormalDist()
    z = nd.inv_cdf(1 - alpha / 2)
    mu = effect / se
    # P(|Z| > z) for Z ~ N(mu,1)
    return (1 - nd.cdf(z - mu)) + nd.cdf(-z - mu)


def main() -> None:
    if not MASTER_CSV.exists():
        raise FileNotFoundError(f"No existe {MASTER_CSV}; ejecuta scripts/rebuild_master_from_episodes.py")

    master = pd.read_csv(MASTER_CSV)
    master["filename_norm"] = master["filename"].astype(str).str.replace("\\\\", "/", regex=True)
    f3 = master[master["filename_norm"].str.contains("results/v11/F3/", case=False, na=False)].copy()
    if f3.empty:
        raise RuntimeError("No se detectaron filas F3 en results/master_results_clean.csv")

    f3["condition"] = f3["filename_norm"].apply(parse_condition)
    f3["grid_size"] = f3["filename_norm"].apply(parse_grid)
    f3["pgf_mix"] = f3["filename_norm"].apply(parse_pgf_mix)
    f3["reward_env_total"] = pd.to_numeric(f3["reward_env_total"], errors="coerce")
    f3 = f3[f3["reward_env_total"].notna()].copy()

    # Baseline control por condición (pooled grids, pgf_mix=0.0)
    baselines = {}
    for cond in ("F1_highrisk", "F2_redteam"):
        ctrl = f3[(f3["condition"] == cond) & (f3["agent"] == "control") & (f3["pgf_mix"] == 0.0)]
        baselines[cond] = float(ctrl["reward_env_total"].mean())

    comparisons = [
        ("F1:m0p0_simbiosis_vs_control", "F1_highrisk", ("simbiosis", 0.0), ("control", 0.0)),
        ("F1:m0p0_simbiosis_vs_dqn_control", "F1_highrisk", ("simbiosis", 0.0), ("dqn_control", 0.0)),
        ("F2:m0p0_simbiosis_vs_control", "F2_redteam", ("simbiosis", 0.0), ("control", 0.0)),
        ("F2:m0p0_simbiosis_vs_dqn_control", "F2_redteam", ("simbiosis", 0.0), ("dqn_control", 0.0)),
        ("F1:pgf_ablation_m0p2_vs_m0p0", "F1_highrisk", ("simbiosis", 0.2), ("simbiosis", 0.0)),
        ("F2:pgf_ablation_m0p2_vs_m0p0", "F2_redteam", ("simbiosis", 0.2), ("simbiosis", 0.0)),
    ]

    rows = []
    for key, cond, (a_agent, a_mix), (b_agent, b_mix) in comparisons:
        a = f3[(f3["condition"] == cond) & (f3["agent"] == a_agent) & (f3["pgf_mix"] == a_mix)]["reward_env_total"]
        b = f3[(f3["condition"] == cond) & (f3["agent"] == b_agent) & (f3["pgf_mix"] == b_mix)]["reward_env_total"]
        n_a = int(a.shape[0])
        n_b = int(b.shape[0])
        mean_a = float(a.mean())
        mean_b = float(b.mean())
        sd_a = float(a.std(ddof=1)) if n_a > 1 else 0.0
        sd_b = float(b.std(ddof=1)) if n_b > 1 else 0.0
        se = math.sqrt((sd_a * sd_a) / max(1, n_a) + (sd_b * sd_b) / max(1, n_b))

        baseline = baselines[cond]
        mesi = MESI_FRAC * abs(baseline)
        power_alpha = power_two_sample_z(effect=mesi, se=se, alpha=ALPHA)
        power_bonf = power_two_sample_z(effect=mesi, se=se, alpha=ALPHA / M_FAMILY)

        rows.append(
            {
                "comparison": key,
                "condition": cond,
                "baseline_control_mean": baseline,
                "mesi_abs_5pct_baseline": mesi,
                "n_a": n_a,
                "n_b": n_b,
                "mean_a": mean_a,
                "mean_b": mean_b,
                "sd_a": sd_a,
                "sd_b": sd_b,
                "se": se,
                "power_alpha_0p05": power_alpha,
                "power_bonf_0p05_div_6": power_bonf,
            }
        )

    df = pd.DataFrame(rows)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)

    lines = [
        "# F3 power analysis (v11)",
        "",
        "Nota: este análisis es **prospectivo/diagnóstico basado en la varianza observada** (no es preregistrado y no cambia los resultados).",
        "",
        f"- MESI usado: {MESI_FRAC:.0%} del baseline `control` (por condición), sobre `reward_env_total`.",
        f"- alpha nominal: {ALPHA}",
        f"- alpha conservador (Bonferroni, lower bound vs Holm M={M_FAMILY}): {ALPHA / M_FAMILY:.6g}",
        "",
        "Power aproximado usando aproximación Normal para diferencia de medias (two-sided), con SE estimado desde SD observada por grupo.",
        "",
        f"Salida tabular: `{OUT_CSV.as_posix()}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Escrito: {OUT_CSV}")
    print(f"[OK] Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()

