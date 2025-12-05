"""
RUNNER ABLATION B: Entrenamiento directo en 8x8 (sin curriculum)
================================================================

Corre 8x8 desde cero para cada seed, sin transfer ni curriculum.
Guarda resultados en results/pgf_v10_ablation/config_B_direct_8x8/seeds/seed_xxxx
"""

import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from run_curriculum_complete_viable import (
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
from sim.dqn_agent import DQNAgent

SEEDS = [13, 42, 101, 2025, 9999]
<<<<<<< HEAD
OUTPUT_DIR = Path(__file__).parent.parent / "results" / "pgf_v10_ablation" / "config_B_direct_8x8" / "seeds"


def run_direct_8x8(seed: int, output_dir: Path):
    print("\n" + "=" * 70)
    print(f"SEED {seed}: Directo 8x8")
    print("=" * 70)
=======
OUTPUT_DIR = ROOT / "results" / "pgf_v10_ablation" / "config_B_direct_8x8" / "seeds"


def run_direct_8x8(seed, output_dir):
    print("\n" + "="*70)
    print(f"SEED {seed}: Directo 8x8")
    print("="*70)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_summary = []

<<<<<<< HEAD
    env_8x8 = create_env(grid_size=8, max_steps_multiplier=5.0)
=======
    env_8x8 = create_env(grid_size=8, max_steps_multiplier=3.0)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    torch.manual_seed(seed)
    np.random.seed(seed)
    state = env_8x8.reset()
    state_dim = len(state_to_vector(state))
    action_dim = 5
    agent_8x8 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=EPSILON_START,
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
<<<<<<< HEAD
        hidden_dim=HIDDEN_DIM,
=======
        hidden_dim=HIDDEN_DIM
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    )
    result_8x8 = train_phase(
        env_8x8,
        agent_8x8,
<<<<<<< HEAD
        num_episodes=1500,
        phase_name=f"8x8_seed{seed}",
        gate_threshold=GATE_8X8,
    )
    results_summary.append(
        {
            "seed": seed,
            "phase": "8x8",
            "grid_size": 8,
            "episodes": 1500,
            "success_rate_total": result_8x8["success_rate"],
            "success_last_100": result_8x8["last_100_success"],
            "gate": GATE_8X8 * 100,
            "gate_passed": result_8x8["gate_passed"],
            "first_success_episode": result_8x8["first_success"],
            "convergence_episode": result_8x8.get("convergence_episode", -1),
        }
    )
    pd.DataFrame(result_8x8["metrics"]).to_csv(output_dir / f"phase_8x8_{timestamp}.csv", index=False)
    if result_8x8["gate_passed"]:
        torch.save(agent_8x8.model.state_dict(), output_dir / f"model_8x8_{timestamp}.pth")
    pd.DataFrame(results_summary).to_csv(output_dir / f"direct_8x8_summary_{timestamp}.csv", index=False)
=======
        num_episodes=1000,
        phase_name=f"8x8_seed{seed}",
        gate_threshold=GATE_8X8
    )
    results_summary.append({
        "seed": seed,
        "phase": "8x8",
        "grid_size": 8,
        "episodes": 1000,
        "success_rate_total": result_8x8["success_rate"],
        "success_last_100": result_8x8["last_100_success"],
        "gate": GATE_8X8 * 100,
        "gate_passed": result_8x8["gate_passed"],
        "first_success_episode": result_8x8["first_success"],
        "convergence_episode": result_8x8.get("convergence_episode", -1)
    })
    df_8x8 = pd.DataFrame(result_8x8["metrics"])
    df_8x8.to_csv(output_dir / f"phase_8x8_{timestamp}.csv", index=False)
    if result_8x8["gate_passed"]:
        model_8x8_path = output_dir / f"model_8x8_{timestamp}.pth"
        torch.save(agent_8x8.model.state_dict(), model_8x8_path)
    df_summary = pd.DataFrame(results_summary)
    df_summary.to_csv(output_dir / f"direct_8x8_summary_{timestamp}.csv", index=False)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    return results_summary


def main():
<<<<<<< HEAD
    print("=" * 70)
    print("ABLATION B: Directo 8x8")
    print("=" * 70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} x 1500 episodes = {len(SEEDS) * 1500} episodes")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
=======
    print("="*70)
    print("ABLATION B: Directo 8×8")
    print("="*70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} × 1000 episodes = {len(SEEDS) * 1000} episodes")
    OUTPUT_DIR.mkdir(exist_ok=True)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    all_results = []
    start_time = time.time()
    for i, seed in enumerate(SEEDS, 1):
        seed_dir = OUTPUT_DIR / f"seed_{seed:04d}"
<<<<<<< HEAD
        print("\n" + "#" * 50)
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print("#" * 50)
=======
        print("\n" + "#"*70)
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print("#"*70)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
        seed_start = time.time()
        try:
            summary = run_direct_8x8(seed, seed_dir)
            all_results.extend(summary)
            seed_duration = (time.time() - seed_start) / 60
<<<<<<< HEAD
            print(f"\nOK. Seed {seed} completado en {seed_duration:.1f} minutos")
            for res in summary:
                success = res["success_last_100"]
                gate = res["gate"]
                passed = "OK" if res["gate_passed"] else "FAIL"
                print(f"   8x8: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
            print(f"\nERROR en seed {seed}: {e}")
            import traceback
            traceback.print_exc()
    total_duration = (time.time() - start_time) / 3600
    print("\n" + "=" * 70)
    print("ABLATION B COMPLETADA")
    print("=" * 70)
    print(f"Duración total: {total_duration:.2f} horas")
    print(f"\nResultados guardados en: {OUTPUT_DIR}")

=======
            print(f"\n✅ Seed {seed} completado en {seed_duration:.1f} minutos")
            for res in summary:
                success = res['success_last_100']
                gate = res['gate']
                passed = "✅" if res['gate_passed'] else "❌"
                print(f"   8x8: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
            print(f"\n❌ ERROR en seed {seed}: {e}")
            import traceback
            traceback.print_exc()
    total_duration = (time.time() - start_time) / 3600
    print("\n" + "="*70)
    print("ABLATION B COMPLETADA")
    print("="*70)
    print(f"Duración total: {total_duration:.2f} horas")
    print(f"\n📂 Resultados guardados en: {OUTPUT_DIR}")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)

if __name__ == "__main__":
    main()
