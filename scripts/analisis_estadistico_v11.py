import json
import math
from pathlib import Path

import pandas as pd

MASTER_CSV = Path("results/master_results_clean.csv")
DATA_DIR = Path("results/v11/data")
BOOTSTRAP_CSV = DATA_DIR / "bootstrap_stats_v11.csv"
SUMMARY_CSV = DATA_DIR / "stats_summary_v11.csv"
REPORT_MD = DATA_DIR / "stats_report_v11.md"

METRICS = [
    ("reward_total", "reward_total"),
    ("reward_env_total", "reward_env_total"),
]

PHASE_HINTS = {
    "f0_baseline": "F0_baseline",
    "f1_highrisk": "F1_highrisk",
    "f2_redteam": "F2_redteam",
    "f6/": "F6",
    "f6_": "F6",
    "/f6_": "F6",
    "f5/": "F5",
    "f5_": "F5",
    "/f5_": "F5",
    "f4/": "F4",
    "f4_": "F4",
    "/f4_": "F4",
    "f3/": "F3",
    "f3_": "F3",
    "/f3_": "F3",
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
    if "results/v11/f6/" in lowered:
        return "F6"
    if "results/v11/f5/" in lowered:
        return "F5"
    if "results/v11/f4/" in lowered:
        return "F4"
    # Prioridad: si el archivo vive bajo results/v11/F3/, debe contarse como F3
    # incluso si contiene subcarpetas llamadas F1_highrisk / F2_redteam.
    if "results/v11/f3/" in lowered:
        return "F3"
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
    master["phase"] = master["filename"].astype(str).apply(detect_phase)
    master["risk_key"] = master["risk_scale"].apply(normalize_risk)

    attack_cache: dict[str, tuple[bool, str, str]] = {}
    rows = []
    for metric_name, col in METRICS:
        if col not in master.columns:
            continue
        subset = master[master[col].notna()].copy()
        if subset.empty:
            continue
        for (phase, agent, risk_key), group in subset.groupby(["phase", "agent", "risk_key"]):
            values = pd.to_numeric(group[col], errors="coerce").dropna()
            if values.empty:
                continue
            n = len(values)
            mean = float(values.mean())
            std = float(values.std(ddof=1)) if n > 1 else 0.0
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
                    "metric": metric_name,
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
        if "metric" not in bootstrap.columns:
            bootstrap["metric"] = "reward_total"
        summary = summary.merge(
            bootstrap[["phase", "agent", "risk_key", "metric", "p_boot", "p_boot_holm"]],
            left_on=["phase", "agent", "risk_scale", "metric"],
            right_on=["phase", "agent", "risk_key", "metric"],
            how="left",
        ).drop(columns=["risk_key"])
    else:
        summary["p_boot"] = float("nan")
        summary["p_boot_holm"] = float("nan")

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
        "- Este reporte incluye dos metricas de recompensa:",
        "  - `reward_total`: promedio por run del campo `Recompensa` en `*_episodes.csv` (recompensa total exportada por episodio).",
        "  - `reward_env_total`: promedio por run de la recompensa ambiental por episodio (sumatoria por step), estimada desde `reward_env_evol` en el JSON del run.",
        "- Para `simbiosis`, `reward_total` puede incluir mezcla con PGF cuando `pgf_mix>0` (reward shaping). Ver `results/v11/ANEXO_TECNICO_v11.md`.",
        "- `n` es el numero de runs/archivos (no episodios).",
        "",
    ]

    for metric in summary["metric"].dropna().unique():
        metric_section = summary[summary["metric"] == metric]
        if metric_section.empty:
            continue
        lines.append(f"## Metrica `{metric}`")
        lines.append("")
        for phase in sorted(metric_section["phase"].unique()):
            section = metric_section[metric_section["phase"] == phase]
            if section.empty:
                continue
            lines.append(f"### Fase `{phase}`")
            lines.append("")
            if phase == "F3":
                lines.append("Nota: F3 se reporta aqui solo como descriptivo agregado. Para el analisis preregistrado (por condicion F1/F2 y pgf_mix, con Holm M=6), ver `results/v11/data/f3_preregistered_report_v11.md`.")
                lines.append("")
            if phase == "F4":
                lines.append("Nota: F4 fija `F2_redteam` y redefine el endpoint primario como CFR (catastrofes por budget run-level). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado de CFR (Fisher + Holm) ver `results/v11/data/f4_preregistered_report_v11.md`.")
                lines.append("")
            if phase == "F5":
                lines.append("Nota: F5 mantiene high-stakes `B=3` y cambia el endpoint primario a `episodes_completed` (tiempo-hasta-agotar-budget). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f5_preregistered_report_v11.md`.")
                lines.append("")
            if phase == "F6":
                lines.append("Nota: F6 mantiene high-stakes `B=3` y vuelve a CFR como endpoint primario, pero calibra `red_team_prob` via un piloto preregistrado (seleccion de p*). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f6_preregistered_report_v11.md` y el piloto en `results/v11/data/f6_pilot_selection_v11.md`.")
                lines.append("")
            cols = ["agent", "risk_scale", "n", "mean", "std", "ci95_lo", "ci95_hi", "p_boot", "p_boot_holm", "attack_enabled", "attack_type", "attack_params"]
            lines.append(section[cols].to_string(index=False))
            lines.append("")

    lines.append("## Notas rapidas")
    lines.append("")
    lines.append("- Los p-values (`p_boot`) provienen del bootstrap no parametrico con unidad `run_mean_by_file` (media por seed/run) y se reportan solo para F2 vs control.")
    lines.append("- `p_boot_holm` aplica correccion Holm (por metrica) a las comparaciones de F2 vs control.")
    lines.append("- `attack_enabled` esta activo para `F2_redteam`, `F4` y `F5` (F4/F5 fijan F2_redteam); `attack_params` resume los parametros del entorno que habilitan el ataque.")
    lines.append("- Para F3, el reporte preregistrado (family primaria Holm M=6) esta en `results/v11/data/f3_preregistered_report_v11.md`.")
    lines.append("- Para F4, el reporte preregistrado (endpoint CFR + Holm) esta en `results/v11/data/f4_preregistered_report_v11.md`.")
    lines.append("- Para F5, el reporte preregistrado (endpoint episodes_completed + Holm) esta en `results/v11/data/f5_preregistered_report_v11.md`.")
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
