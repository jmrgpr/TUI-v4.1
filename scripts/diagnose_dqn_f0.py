"""
diagnose_dqn_f0.py - Diagnóstico rápido de DQN-Control en F0 (v11)

Analiza el CSV por episodios para detectar fallos sistemáticos del baseline DQN-Control.
Uso:
    python scripts/diagnose_dqn_f0.py --csv results/v11/F0_baseline/raw/grid8_risklow_seed42_v11_episodes.csv

Limitaciones:
- El CSV de episodios no contiene logs de acciones ni longitud exacta de cada episodio.
- Se centra en reward medio y dispersión por agente; si hay columnas extras se usan.
"""

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def diagnose(csv_path: Path, out_dir: Path) -> dict:
    df = pd.read_csv(csv_path)
    result = {}

    for agent in ["control", "simbiosis", "dqn_control"]:
        agent_df = df[df["Agente"] == agent]
        if agent_df.empty:
            print(f"[WARN] No hay filas para {agent}")
            continue

        mean_reward = agent_df["Recompensa"].mean()
        std_reward = agent_df["Recompensa"].std()
        result[agent] = {
            "n": len(agent_df),
            "mean_reward": mean_reward,
            "std_reward": std_reward,
        }
        print(f"[{agent}] n={len(agent_df)}, reward={mean_reward:.2f} ± {std_reward:.2f}")

    # Comparación DQN-Control vs Control
    if "dqn_control" in result and "control" in result:
        diff = result["dqn_control"]["mean_reward"] - result["control"]["mean_reward"]
        print(f"\nΔ reward (DQN-Control - Control): {diff:.2f}")
        result["delta_dqn_minus_control"] = diff

    # Gráfico simple de reward por episodio por agente
    plt.figure(figsize=(10, 5))
    for agent in ["control", "simbiosis", "dqn_control"]:
        agent_df = df[df["Agente"] == agent]
        if agent_df.empty:
            continue
        plt.plot(agent_df.index, agent_df["Recompensa"], label=agent, alpha=0.7)
    plt.legend()
    plt.title("Evolución de recompensa por agente")
    plt.xlabel("Episodio (orden en CSV)")
    plt.ylabel("Recompensa")
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_path = out_dir / "dqn_reward_evolution.png"
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Gráfico guardado en {plot_path}")

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        type=str,
        required=True,
        help="Ruta al CSV de episodios (F0).",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default="results/v11/F0_baseline/analysis",
        help="Directorio de salida para gráficos/resultados.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)

    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el CSV: {csv_path}")

    diagnose(csv_path, out_dir)


if __name__ == "__main__":
    main()
