"""
Script de análisis avanzado para Fase 3 PGF offline.
Genera correlaciones, tablas resumen y visualizaciones clave.


Además de PGF vs I_op, calcula:
- Correlación PGF vs success (si existe la columna).
- Correlación PGF vs steps (como proxy de overhead).
- Un CSV global `pgf_vs_success_summary.csv` con métricas agregadas
  por archivo enriquecido (fase / run).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python analyze_pgf_offline_v10.py <carpeta_enriched>")
        sys.exit(1)

    enriched_dir = Path(sys.argv[1])
    output_dir = enriched_dir.parent / "analysis"
    output_dir.mkdir(exist_ok=True)

    csvs = sorted(enriched_dir.glob("*.csv"))

    # Acumulador para resumen global PGF vs éxito / steps
    summary_rows = []

    for csv_path in csvs:
        df = pd.read_csv(csv_path)
        basename = csv_path.stem.replace("_enriched", "")

        # Fase aproximada a partir del nombre de archivo (phase1/2/3_4x4/6x6/8x8_...)
        # Ejemplos: phase1_4x4_..., phase2_6x6_..., phase3_8x8_...
        parts = basename.split("_")
        phase_id = parts[0] if parts else ""
        grid = parts[1] if len(parts) > 1 else ""

        # Correlación PGF vs I_op (como antes)
        corr_pgf_iop = float("nan")
        if {"PGF", "I_op"}.issubset(df.columns):
            corr_pgf_iop = df[["PGF", "I_op"]].corr().iloc[0, 1]
            with open(
                output_dir / f"{basename}_correlation.txt", "w", encoding="utf-8"
            ) as f:
                f.write(f"Correlación PGF vs I_op: {corr_pgf_iop:.4f}\n")

        # Histograma PGF
        if "PGF" in df.columns:
            plt.figure()
            sns.histplot(df["PGF"], kde=True)
            plt.title(f"Histograma PGF - {basename}")
            plt.savefig(output_dir / f"{basename}_hist_pgf.png")
            plt.close()

        # Histograma I_op
        if "I_op" in df.columns:
            plt.figure()
            sns.histplot(df["I_op"], kde=True)
            plt.title(f"Histograma I_op - {basename}")
            plt.savefig(output_dir / f"{basename}_hist_iop.png")
            plt.close()

        # Tabla resumen básica PGF / I_op
        cols_basic = [c for c in ["PGF", "I_op"] if c in df.columns]
        if cols_basic:
            summary = df[cols_basic].describe()
            summary.to_csv(output_dir / f"{basename}_summary.csv")

        # --- Análisis adicional PGF vs éxito / steps ---
        has_success = "success" in df.columns
        has_steps = "steps" in df.columns

        row = {
            "file": csv_path.name,
            "phase": phase_id,
            "grid": grid,
            "pgf_mean": df["PGF"].mean() if "PGF" in df.columns else float("nan"),
            "pgf_std": df["PGF"].std() if "PGF" in df.columns else float("nan"),
            "iop_mean": df["I_op"].mean() if "I_op" in df.columns else float("nan"),
            "iop_std": df["I_op"].std() if "I_op" in df.columns else float("nan"),
            "corr_pgf_iop": corr_pgf_iop,
        }

        # Correlación PGF vs success (si hay columna)
        if has_success and "PGF" in df.columns:
            try:
                corr_pgf_success = df[["PGF", "success"]].corr().iloc[0, 1]
            except Exception:
                corr_pgf_success = float("nan")
            row["corr_pgf_success"] = corr_pgf_success
            row["success_rate"] = df["success"].mean()
        else:
            row["corr_pgf_success"] = float("nan")
            row["success_rate"] = float("nan")

        # Correlación PGF vs steps (proxy overhead)
        if has_steps and "PGF" in df.columns:
            try:
                corr_pgf_steps = df[["PGF", "steps"]].corr().iloc[0, 1]
            except Exception:
                corr_pgf_steps = float("nan")
            row["corr_pgf_steps"] = corr_pgf_steps
            row["steps_mean"] = df["steps"].mean()
            row["steps_std"] = df["steps"].std()
        else:
            row["corr_pgf_steps"] = float("nan")
            row["steps_mean"] = float("nan")
            row["steps_std"] = float("nan")

        summary_rows.append(row)

    # Guardar resumen global PGF vs éxito / steps
    if summary_rows:
        df_summary = pd.DataFrame(summary_rows)
        df_summary.to_csv(output_dir / "pgf_vs_success_summary.csv", index=False)

    print("Análisis completado. Resultados en:", output_dir)


if __name__ == "__main__":
    main()

=======
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

if len(sys.argv) < 2:
    print("Uso: python analyze_pgf_offline_v10.py <carpeta_enriched>")
    sys.exit(1)

enriched_dir = Path(sys.argv[1])
output_dir = enriched_dir.parent / "analysis"
output_dir.mkdir(exist_ok=True)

csvs = list(enriched_dir.glob("*.csv"))

for csv_path in csvs:
    df = pd.read_csv(csv_path)
    basename = csv_path.stem.replace('_enriched','')
    # Correlación PGF vs I_op
    corr = df[["PGF", "I_op"]].corr().iloc[0,1]
    with open(output_dir / f"{basename}_correlation.txt", "w") as f:
        f.write(f"Correlación PGF vs I_op: {corr:.4f}\n")
    # Histograma PGF
    plt.figure()
    sns.histplot(df["PGF"], kde=True)
    plt.title(f"Histograma PGF - {basename}")
    plt.savefig(output_dir / f"{basename}_hist_pgf.png")
    plt.close()
    # Histograma I_op
    plt.figure()
    sns.histplot(df["I_op"], kde=True)
    plt.title(f"Histograma I_op - {basename}")
    plt.savefig(output_dir / f"{basename}_hist_iop.png")
    plt.close()
    # Tabla resumen
    summary = df[["PGF", "I_op"]].describe()
    summary.to_csv(output_dir / f"{basename}_summary.csv")
print("Análisis completado. Resultados en:", output_dir)
>>>>>>> 03cb0ce (Close v10 Fase 2 ablation, add v9/v10 reports, and scaffold Fase 3 PGF offline)
