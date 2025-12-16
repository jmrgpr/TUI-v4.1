import csv
from pathlib import Path
from statistics import mean, stdev


RAW_DIR = Path("results/v11/F1_highrisk/raw")
ANALYSIS_DIR = Path("results/v11/F1_highrisk/analysis")


def load_stat_tests():
    path = ANALYSIS_DIR / "stat_tests_F1_v11.csv"
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def metric_to_column(metric: str) -> str | None:
    mapping = {
        "Recompensa": "Recompensa",
        "Flexibilidad": "Flexibilidad",
        "Robustez": "Robustez",
        "RiskEffective_Avg": "RiskEffective_Avg",
        "Surprise_Avg": "Surprise_Avg",
        "PGF_Bruto_Avg": "PGF_Bruto_Avg",
        "PGF_Costo_Avg": "PGF_Costo_Avg",
        "Q-optimal": "Q-optimal",
    }
    return mapping.get(metric)


def load_episodes(grid: int, seed: int):
    path = RAW_DIR / f"grid{grid}_riskhigh_r1p2_seed{seed}_v11_episodes.csv"
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def float_or_none(x: str) -> float | None:
    if x is None or x == "":
        return None
    return float(x)


def main() -> None:
    issues: list[str] = []
    stat_rows = load_stat_tests()

    for row in stat_rows:
        grid = int(row["Grid"])
        seed = int(row["Seed"])
        metric = row["Metric"]
        col = metric_to_column(metric)
        if col is None:
            continue

        mean_simb = float_or_none(row.get("mean_simbiosis"))
        std_simb = float_or_none(row.get("std_simbiosis"))
        mean_ctrl = float_or_none(row.get("mean_control"))
        std_ctrl = float_or_none(row.get("std_control"))

        # Si no hay medias registradas, no comprobamos (caso degenerate)
        if mean_simb is None or mean_ctrl is None:
            continue

        episodes = load_episodes(grid, seed)

        def values_for(agent: str):
            vals = [float(r[col]) for r in episodes if r.get("Agente") == agent]
            return vals

        vals_simb = values_for("simbiosis")
        vals_ctrl = values_for("control")

        if not vals_simb or not vals_ctrl:
            issues.append(f"[EPISODES-MISSING] Grid={grid} Seed={seed} Metric={metric}: faltan filas para algun agente")
            continue

        # Medias
        m_simb = mean(vals_simb)
        m_ctrl = mean(vals_ctrl)

        if abs(m_simb - mean_simb) > 1e-6:
            issues.append(
                f"[MEAN-MISMATCH] Grid={grid} Seed={seed} Metric={metric} simbiosis: "
                f"csv={m_simb:.12f} stat={mean_simb:.12f}"
            )
        if abs(m_ctrl - mean_ctrl) > 1e-6:
            issues.append(
                f"[MEAN-MISMATCH] Grid={grid} Seed={seed} Metric={metric} control: "
                f"csv={m_ctrl:.12f} stat={mean_ctrl:.12f}"
            )

        # Desviaciones estándar muestrales (si están informadas)
        if std_simb is not None:
            s_simb = stdev(vals_simb)
            if abs(s_simb - std_simb) > 1e-6:
                issues.append(
                    f"[STD-MISMATCH] Grid={grid} Seed={seed} Metric={metric} simbiosis: "
                    f"csv={s_simb:.12f} stat={std_simb:.12f}"
                )

        if std_ctrl is not None:
            s_ctrl = stdev(vals_ctrl)
            if abs(s_ctrl - std_ctrl) > 1e-6:
                issues.append(
                    f"[STD-MISMATCH] Grid={grid} Seed={seed} Metric={metric} control: "
                    f"csv={s_ctrl:.12f} stat={std_ctrl:.12f}"
                )

    if issues:
        print("=== FSCK F1 STATS CONSISTENCY: PROBLEMAS DETECTADOS ===")
        for issue in issues:
            print(issue)
    else:
        print("=== FSCK F1 STATS CONSISTENCY: TODO OK ===")


if __name__ == "__main__":
    main()
