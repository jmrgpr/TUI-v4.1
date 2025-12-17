import json
import math
from pathlib import Path

import pandas as pd

MASTER_CSV = Path("results/master_results_clean.csv")
DATA_DIR = Path("results/v11/data")
BOOTSTRAP_CSV = DATA_DIR / "bootstrap_stats_v11.csv"
SUMMARY_CSV = DATA_DIR / "stats_summary_v11.csv"
REPORT_MD = DATA_DIR / "stats_report_v11.md"

PHASE_HINTS = {
    "f0_baseline": "F0_baseline",
    "f1_highrisk": "F1_highrisk",
    "f2_redteam": "F2_redteam",
}

ATTACK_COLUMNS = [
    "grid_size",
    "risk_scale",
    "risk_level",
    "pgf_mix",
    "episodes",
    "seed",
    "red_team",
    "red_team_prob",
    "red_team_impact",
    "red_team_move_tripwire_prob",
    "red_team_add_shock_prob",
    "red_team_block_prob",
]


def detect_phase(filename: str) -> str:
    lowered = filename.replace("\\", "/").lower()
    for marker, phase in PHASE_HINTS.items():
        if marker in lowered:
            return phase
    if "archived" in lowered:
        return "archived"
    return "untracked"


def normalize_risk(value) -> str:
    try:
        if pd.isna(value):
            return "unknown"
        return format(float(value), ".6g")
    except Exception:
        return "unknown"


def describe_attack_params(config: dict) -> str:
    if not config:
        return ""
    parts = []
    for key in ATTACK_COLUMNS:
        val = config.get(key)
        if val is None:
            continue
        parts.append(f"{key}={val}")
    return ";".join(parts)


def load_attack_info(filepath: str, cache: dict) -> tuple[bool, str, str]:
    if filepath in cache:
        return cache[filepath]
    path = Path(filepath)
    if not path.exists():
        cache[filepath] = (False, "", "")
        return cache[filepath]
    if not path.name.endswith("_episodes.csv"):
        cache[filepath] = (False, "", "")
        return cache[filepath]
    json_path = path.with_name(path.name.replace("_episodes.csv", ".json"))
    if not json_path.exists():
        cache[filepath] = (False, "", "")
        return cache[filepath]
    try:
        with json_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except json.JSONDecodeError:
        cache[filepath] = (False, "", "")
        return cache[filepath]
    config = payload.get("config", {})
    attack_enabled = bool(config.get("red_team") or payload.get("red_team"))
    attack_params = describe_attack_params(config)
    cache[filepath] = (attack_enabled, attack_params, json_path.stem)
    return cache[filepath]


def compute_summary(master: pd.DataFrame) -> pd.DataFrame:
    master = master.dropna(subset=["agent"])
    master = master[master["reward_total"].notna()]
    master["phase"] = master["filename"].astype(str).apply(detect_phase)
    master["risk_key"] = master["risk_scale"].apply(normalize_risk)

    attack_cache: dict[str, tuple[bool, str, str]] = {}
    rows = []
    for (phase, agent, risk_key), group in master.groupby(["phase", "agent", "risk_key"]):
        rewards = pd.to_numeric(group["reward_total"], errors="coerce").dropna()
        if rewards.empty:
            continue
        n = len(rewards)
        mean = float(rewards.mean())
        std = float(rewards.std(ddof=1)) if n > 1 else 0.0
        se = std / math.sqrt(n) if n > 1 else 0.0
        ci_lo = mean - 1.96 * se
        ci_hi = mean + 1.96 * se

        attack_records = [load_attack_info(f, attack_cache) for f in group["filename"].astype(str)]
        attack_enabled = any(info[0] for info in attack_records)
        attack_params = next((info[1] for info in attack_records if info[1]), "")
        attack_type = "red_team_adversarial" if attack_enabled else "none"

        rows.append(
            {
                "phase": phase,
                "agent": agent,
                "risk_scale": risk_key,
                "n": n,
                "mean": mean,
                "std": std,
                "ci95_lo": ci_lo,
                "ci95_hi": ci_hi,
                "attack_enabled": attack_enabled,
                "attack_type": attack_type,
                "attack_params": attack_params,
            }
        )

    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary

    if BOOTSTRAP_CSV.exists():
        bootstrap = pd.read_csv(BOOTSTRAP_CSV)
        if "phase" not in bootstrap.columns:
            bootstrap["phase"] = "unknown"
        bootstrap["risk_key"] = bootstrap["risk_scale"].apply(normalize_risk) if "risk_scale" in bootstrap.columns else "unknown"
        summary = summary.merge(
            bootstrap[["phase", "agent", "risk_key", "p_boot"]],
            left_on=["phase", "agent", "risk_scale"],
            right_on=["phase", "agent", "risk_key"],
            how="left",
        ).drop(columns=["risk_key"])
    else:
        summary["p_boot"] = float("nan")

    return summary


def format_report(summary: pd.DataFrame) -> str:
    lines = [
        "# Estadistica descriptiva e inferencial minima - v11",
        "",
        "Fuente: `results/master_results_clean.csv` reconsolidado a partir de los CSV canonicos listados en `results/v11/CANONICAL_DATASET_v11.md`.",
        "",
        "El analisis agrupa por `phase`, `agent` y `risk_scale`. Para F2, incluye un bootstrap no parametrico (ver `results/v11/data/bootstrap_stats_v11.csv`) que usa como unidad primaria la media por archivo `*_episodes.csv` (cluster por seed/run) para evitar pseudo-replicacion por episodio.",
        "",
        "## Metrica y unidad (muy importante)",
        "",
        "- Metrica en este reporte: `reward_total` (columna `reward_total` en `results/master_results_clean.csv`).",
        "- Operacionalmente, `reward_total` es el promedio por run del campo `Recompensa` en `*_episodes.csv` (media de recompensas por episodio dentro del run).",
        "- Para `simbiosis`, `Recompensa` incluye mezcla con PGF cuando `pgf_mix>0` (reward shaping). Ver `results/v11/ANEXO_TECNICO_v11.md`.",
        "- `n` es el numero de runs/archivos (no episodios).",
        "",
    ]

    for phase in sorted(summary["phase"].unique()):
        section = summary[summary["phase"] == phase]
        if section.empty:
            continue
        lines.append(f"## Fase `{phase}`")
        lines.append("")
        lines.append(section[["agent", "risk_scale", "n", "mean", "std", "ci95_lo", "ci95_hi", "p_boot", "attack_enabled", "attack_type", "attack_params"]].to_string(index=False))
        lines.append("")

    lines.append("## Notas rapidas")
    lines.append("")
    lines.append("- Los p-values (`p_boot`) provienen del bootstrap no parametrico con unidad `run_mean_by_file` (media por seed/run).")
    lines.append("- `attack_enabled` esta activo solo para la fase `F2_redteam`; `attack_params` resume los parametros del entorno que habilitan el ataque.")
    lines.append("- Los intervalos de confianza son +/-1.96 errores estandar calculados sobre el numero de runs/archivos (`n`), donde cada archivo representa una configuracion (grid, seed).")
    lines.append("")
    lines.append("El conjunto canonico y la comparativa F1/F2 se documentan en `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/data/f2_vs_f1_diff.md`.")
    return "\n".join(lines)


def main():
    if not MASTER_CSV.exists():
        raise FileNotFoundError(f"{MASTER_CSV} no encontrado. Ejecuta `scripts/rebuild_master_from_episodes.py` primero.")
    master = pd.read_csv(MASTER_CSV)
    summary = compute_summary(master)
    if summary.empty:
        raise RuntimeError("El resumen estadístico quedó vacío.")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_CSV, index=False)
    report = format_report(summary)
    REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Generado resumen estadístico: {SUMMARY_CSV} y {REPORT_MD}")


if __name__ == "__main__":
    main()
