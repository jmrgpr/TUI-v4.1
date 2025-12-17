import json
from pathlib import Path

ROOT = Path("results/v11")
OUTPUT = ROOT / "data" / "f2_vs_f1_diff.md"
PHASES = ["F1_highrisk", "F2_redteam"]
AGENTS = {"control", "dqn_control", "simbiosis"}
METRICS = [
    "avg_reward",
    "avg_tripwire",
    "avg_shocks",
    "avg_gap",
    "mean_surprise",
    "mean_risk_effective",
    "gaming_hits",
    "u_proxy",
    "u_humans",
    "red_team_prob",
]


def mean_of_list(values) -> float | None:
    if not isinstance(values, list):
        return None
    vals = []
    for v in values:
        try:
            vals.append(float(v))
        except Exception:
            continue
    return (sum(vals) / len(vals)) if vals else None


def collect_phase_metrics(phase: str) -> list[dict]:
    metrics = []
    base = ROOT / phase
    if not base.exists():
        return metrics
    for json_path in base.rglob("grid*_riskhigh*.json"):
        parts = [p.lower() for p in json_path.parts]
        if "raw" in parts or "archived" in parts:
            continue
        agent = json_path.parent.name
        if agent not in AGENTS:
            continue
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        row = {"phase": phase, "agent": agent}
        config = data.get("config", {})
        row["attack_enabled"] = bool(config.get("red_team") or data.get("red_team"))
        row["mean_surprise"] = mean_of_list(data.get("surprise_avg")) or mean_of_list(data.get("surprise_evol"))
        row["mean_risk_effective"] = mean_of_list(data.get("risk_effective_avg")) or mean_of_list(data.get("risk_effective_evol"))
        row["red_team_prob"] = config.get("red_team_prob")
        for metric in METRICS:
            if metric in row:
                continue
            row[metric] = data.get(metric)
        metrics.append(row)
    return metrics


def format_table(df: list[dict], header: list[str]) -> str:
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for row in df:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in header) + " |")
    return "\n".join(lines)


def main():
    all_rows = []
    for phase in PHASES:
        all_rows.extend(collect_phase_metrics(phase))
    if not all_rows:
        raise RuntimeError("No se encontraron JSON canonicos para F1 o F2.")

    grouped = {}
    for row in all_rows:
        key = (row["phase"], row["agent"])
        grouped.setdefault(key, []).append(row)

    summary = []
    for (phase, agent), rows in grouped.items():
        avg = {"phase": phase, "agent": agent}
        for metric in METRICS:
            vals = [r[metric] for r in rows if r.get(metric) is not None]
            avg[metric] = sum(vals) / len(vals) if vals else None
        avg["attack_enabled"] = any(r["attack_enabled"] for r in rows)
        summary.append(avg)

    f1 = {row["agent"]: row for row in summary if row["phase"] == "F1_highrisk"}
    f2 = {row["agent"]: row for row in summary if row["phase"] == "F2_redteam"}

    diff_rows = []
    for agent in sorted(AGENTS):
        base = f1.get(agent)
        target = f2.get(agent)
        if not base or not target:
            continue
        diff = {"agent": agent}
        for metric in METRICS:
            val_f1 = base.get(metric) or 0.0
            val_f2 = target.get(metric) or 0.0
            diff[f"{metric}_f1"] = f1_val = round(val_f1, 4) if isinstance(val_f1, (int, float)) else ""
            diff[f"{metric}_f2"] = f2_val = round(val_f2, 4) if isinstance(val_f2, (int, float)) else ""
            diff[f"{metric}_diff"] = round(f2_val - f1_val, 4) if isinstance(f1_val, (int, float)) and isinstance(f2_val, (int, float)) else ""
        diff_rows.append(diff)

    lines = [
        "# F2_vs_F1_diff",
        "",
        "Se comparan los JSON canónicos de la fase `F1_highrisk` (sin ataque) frente a `F2_redteam` (red team activo) para demostrar que F2 introduce perturbaciones observables.",
        "",
        "## Valores promedio por fase",
    ]

    header = ["phase", "agent", "attack_enabled"] + METRICS
    lines.append(format_table(summary, header))
    lines.append("")
    lines.append("## Diferencias (F2 - F1)")
    diff_header = ["agent"] + [f"{metric}_f1" for metric in METRICS] + [f"{metric}_f2" for metric in METRICS] + [f"{metric}_diff" for metric in METRICS]
    lines.append(format_table(diff_rows, diff_header))
    lines.append("")
    lines.append("Los valores `attack_enabled` y `red_team_prob` confirman que solo F2 habilita el red team; los cambios en `avg_tripwire`, `avg_shocks`, `mean_risk_effective` y `mean_surprise` son las señales observables esperadas.")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Diferencia F2 vs F1 guardada en {OUTPUT}")


if __name__ == "__main__":
    main()
