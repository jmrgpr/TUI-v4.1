"""
FASE 4 – Escalabilidad v10
===========================

Runner de stress-test para el stack v10 en 16×16, con dos configuraciones
pre-registradas:

- F4a / config_E_16x16_noreg:   sin regularización (weight_decay=0, dropout=0)
- F4b / config_F_16x16_reg:     con regularización suave (1e-5, 0.10)

Opcionalmente permite 8×8 directo para comparación, pero el foco de la fase
son los grids 16×16 (frontera de v10 antes de v11).

Objetivo científico (ver PREREGISTRO_FASE4_SCALABILITY_v10.md):
- Evaluar hasta dónde escala el stack v10 sin cambiar arquitectura.
- Usar exactamente la economía v10 viable (config.py) y el wiring de
  `run_curriculum_complete_viable.py`, pero sin curriculum ni shaping.
"""

import argparse
import random
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch

import sys
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.run_curriculum_complete_viable import (  # type: ignore
    create_env,
    state_to_vector,
    train_phase,
    LEARNING_RATE,
    GAMMA,
    EPSILON_START,
    EPSILON_MIN,
    EPSILON_DECAY,
    BATCH_SIZE,
    MEMORY_SIZE,
    HIDDEN_DIM,
    GATE_8X8,
)
from sim.dqn_agent import DQNAgent  # type: ignore



# Gate exploratorio para 16×16 (ver preregistro F4)
GATE_16X16 = 0.20  # 20% success en últimos 100 episodios


def make_agent(
    state_dim: int,
    action_dim: int,
    regularization: bool,
) -> DQNAgent:
    """
    Crea un agente DQN configurado según la serie v10.

    - Si regularization=False → F4a / config_E_16x16_noreg
    - Si regularization=True  → F4b / config_F_16x16_reg
    """
    if regularization:
        weight_decay = 1e-5
        dropout = 0.10
    else:
        weight_decay = 0.0
        dropout = 0.0

    return DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=EPSILON_START,
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
        hidden_dim=HIDDEN_DIM,
        weight_decay=weight_decay,
        dropout=dropout,
    )


def run_scalability(
    grid: str,
    seed: int,
    episodes: int,
    output_dir: Path,
    regularization: bool,
    config_name: str,
) -> Path:
    """
    Entrena un solo run (grid, seed) y guarda:
    - CSV episodios completos
    - CSV resumen con métricas finales
    """
    assert grid in ("8x8", "16x16")
    grid_size = 8 if grid == "8x8" else 16

    print("\n" + "=" * 70)
    print(f"FASE 4 – SCALABILITY v10 | {config_name} | Grid {grid} | Seed {seed}")
    print("=" * 70)

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Fijar seeds
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    # Crear entorno con economía v10
    # Usamos el mismo max_steps_multiplier que en B_direct_8x8 (5.0)
    env = create_env(grid_size=grid_size, max_steps_multiplier=5.0)

    # Estado / dimensiones
    state = env.reset()
    state_dim = len(state_to_vector(state))
    action_dim = 5  # up, down, left, right, noop

    # Agente DQN con o sin regularización según la configuración
    agent = make_agent(state_dim=state_dim, action_dim=action_dim, regularization=regularization)

    gate = GATE_8X8 if grid_size == 8 else GATE_16X16
    phase_name = f"{grid}_seed{seed}"

    start = time.time()
    result = train_phase(
        env,
        agent,
        num_episodes=episodes,
        phase_name=phase_name,
        gate_threshold=gate,
    )
    duration_min = (time.time() - start) / 60.0

    # Guardar episodios completos
    metrics = result["metrics"]
    df_episodes = pd.DataFrame(metrics)
    episodes_path = output_dir / f"scalability_{grid}_seed{seed:04d}_episodes_{timestamp}.csv"
    df_episodes.to_csv(episodes_path, index=False)

    # Guardar resumen
    summary = {
        "config": config_name,
        "grid": grid,
        "grid_size": grid_size,
        "seed": seed,
        "episodes": episodes,
        "success_rate_total": result["success_rate"],
        "success_last_100": result["last_100_success"],
        "gate": gate,
        "gate_passed": result["gate_passed"],
        "first_success_episode": result["first_success"],
        "duration_min": duration_min,
    }
    df_summary = pd.DataFrame([summary])
    summary_path = output_dir / f"scalability_{grid}_seed{seed:04d}_summary_{timestamp}.csv"
    df_summary.to_csv(summary_path, index=False)

    # Guardar modelo si pasa gate
    if result["gate_passed"]:
        model_path = output_dir / f"model_{grid}_seed{seed:04d}_{timestamp}.pth"
        agent.save(str(model_path))
        print(f"\n[INFO] Modelo guardado en {model_path}")

    print("\n--- RESUMEN RUN ---")
    print(f"Config: {config_name} | Grid: {grid} | Seed: {seed}")
    print(f"Episodios: {episodes}")
    print(f"Success total: {result['success_rate']*100:.1f}%")
    print(f"Últimos 100: {result['last_100_success']*100:.1f}%")
    print(f"Gate: {gate*100:.0f}% -> {'PASADO' if result['gate_passed'] else 'FALLADO'}")
    print(f"Duración: {duration_min:.2f} min")
    print(f"Episodios CSV: {episodes_path.name}")
    print(f"Resumen CSV:  {summary_path.name}")

    return summary_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fase 4: Escalabilidad v10")
    parser.add_argument(
        "--config",
        type=str,
        choices=["E_16x16_noreg", "F_16x16_reg"],
        help=(
            "Configuración F4a/F4b:\n"
            "  E_16x16_noreg → sin regularización (config_E_16x16_noreg)\n"
            "  F_16x16_reg   → con regularización (config_F_16x16_reg)"
        ),
        required=True,
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=200,
        help="Número de episodios a correr (p.ej. 200–500 para 16x16)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed de entrenamiento",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/pgf_v10_scalability/",
        help="Carpeta base de salida",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Mapear config F4a/F4b -> grid y regularización
    if args.config == "E_16x16_noreg":
        grid = "16x16"
        regularization = False
        config_name = "config_E_16x16_noreg"
        subdir = "config_E_16x16_noreg"
    elif args.config == "F_16x16_reg":
        grid = "16x16"
        regularization = True
        config_name = "config_F_16x16_reg"
        subdir = "config_F_16x16_reg"
    else:
        raise ValueError(f"Configuración desconocida: {args.config}")

    base_output = Path(args.output)
    # Subcarpeta por configuración (como define el README de Fase 4)
    output_dir = base_output / subdir / "seeds" / f"seed_{args.seed:04d}"

    run_scalability(
        grid=grid,
        seed=args.seed,
        episodes=args.episodes,
        output_dir=output_dir,
        regularization=regularization,
        config_name=config_name,
    )


if __name__ == "__main__":
    main()
