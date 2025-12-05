"""
RUNNER ABLATION D: Entrenamiento solo en 6×6 (sin curriculum ni transfer)
=======================================================================

Corre 6×6 desde cero para cada seed, sin transfer ni curriculum.
Guarda resultados en results/pgf_v10_ablation/config_D_only_6x6/seeds/seed_xxxx
"""

import sys
import os
from pathlib import Path
import time
import numpy as np
import pandas as pd
import torch
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from run_curriculum_complete_viable import (
    create_env, state_to_vector, train_phase,
    LEARNING_RATE, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    BATCH_SIZE, MEMORY_SIZE, HIDDEN_DIM,
    GATE_6X6
)
from sim.dqn_agent import DQNAgent

SEEDS = [13, 42, 101, 2025, 9999]
OUTPUT_DIR = ROOT / "results" / "pgf_v10_ablation" / "config_D_only_6x6" / "seeds"


def run_only_6x6(seed, output_dir):
    print("\n" + "="*70)
    print(f"SEED {seed}: Solo 6x6")
    print("="*70)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_summary = []

    env_6x6 = create_env(grid_size=6, max_steps_multiplier=5.0)
    torch.manual_seed(seed)
    np.random.seed(seed)
    state = env_6x6.reset()
    state_dim = len(state_to_vector(state))
    action_dim = 5
    agent_6x6 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
    epsilon=EPSILON_START,
    epsilon_end=EPSILON_MIN,
    epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
        hidden_dim=HIDDEN_DIM
    )
    result_6x6 = train_phase(
        env_6x6,
        agent_6x6,
        num_episodes=1000,
        phase_name=f"6x6_seed{seed}",
        gate_threshold=GATE_6X6
    )
    results_summary.append({
        "seed": seed,
        "phase": "6x6",
        "grid_size": 6,
        "episodes": 1000,
        "success_rate_total": result_6x6["success_rate"],
        "success_last_100": result_6x6["last_100_success"],
        "gate": GATE_6X6 * 100,
        "gate_passed": result_6x6["gate_passed"],
        "first_success_episode": result_6x6["first_success"],
        "convergence_episode": result_6x6.get("convergence_episode", -1)
    })
    df_6x6 = pd.DataFrame(result_6x6["metrics"])
    df_6x6.to_csv(output_dir / f"phase_6x6_{timestamp}.csv", index=False)
    if result_6x6["gate_passed"]:
        model_6x6_path = output_dir / f"model_6x6_{timestamp}.pth"
        torch.save(agent_6x6.model.state_dict(), model_6x6_path)
    df_summary = pd.DataFrame(results_summary)
    df_summary.to_csv(output_dir / f"only_6x6_summary_{timestamp}.csv", index=False)
    return results_summary


def main():
    print("="*70)
<<<<<<< HEAD
<<<<<<< HEAD
    print("ABLATION D: Solo 6x6")
=======
    print("ABLATION D: Solo 6×6")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
=======
    print("ABLATION D: Solo 6x6")
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
    print("="*70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} × 1000 episodes = {len(SEEDS) * 1000} episodes")
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_results = []
    start_time = time.time()
    for i, seed in enumerate(SEEDS, 1):
        seed_dir = OUTPUT_DIR / f"seed_{seed:04d}"
<<<<<<< HEAD
<<<<<<< HEAD
        print("\n" + "#"*50)
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print("#"*50)
=======
        print("\n" + "#"*70)
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print("#"*70)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
=======
        print("\n" + "#"*50)
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print("#"*50)
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
        seed_start = time.time()
        try:
            summary = run_only_6x6(seed, seed_dir)
            all_results.extend(summary)
            seed_duration = (time.time() - seed_start) / 60
<<<<<<< HEAD
<<<<<<< HEAD
            print(f"\n✔️ Seed {seed} completado en {seed_duration:.1f} minutos")
            for res in summary:
                success = res['success_last_100']
                gate = res['gate']
                passed = "✔️" if res['gate_passed'] else "✖️"
                print(f"   6x6: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
            print(f"\n✖️ ERROR en seed {seed}: {e}")
=======
            print(f"\n✅ Seed {seed} completado en {seed_duration:.1f} minutos")
=======
            print(f"\n✔️ Seed {seed} completado en {seed_duration:.1f} minutos")
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
            for res in summary:
                success = res['success_last_100']
                gate = res['gate']
                passed = "✔️" if res['gate_passed'] else "✖️"
                print(f"   6x6: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
<<<<<<< HEAD
            print(f"\n❌ ERROR en seed {seed}: {e}")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
=======
            print(f"\n✖️ ERROR en seed {seed}: {e}")
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
            import traceback
            traceback.print_exc()
    total_duration = (time.time() - start_time) / 3600
    print("\n" + "="*70)
    print("ABLATION D COMPLETADA")
    print("="*70)
    print(f"Duración total: {total_duration:.2f} horas")
<<<<<<< HEAD
<<<<<<< HEAD
    print(f"\n📁 Resultados guardados en: {OUTPUT_DIR}")
=======
    print(f"\n📂 Resultados guardados en: {OUTPUT_DIR}")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
=======
    print(f"\n📁 Resultados guardados en: {OUTPUT_DIR}")
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)

if __name__ == "__main__":
    main()
