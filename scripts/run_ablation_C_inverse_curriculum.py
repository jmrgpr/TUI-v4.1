"""
RUNNER ABLATION C: Curriculum inverso (8x8 -> 6x6 -> 4x4)
==========================================================
"""

import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

<<<<<<< HEAD
from run_curriculum_complete_viable import (
    create_env,
    state_to_vector,
    train_phase,
    save_agent,
    load_agent,
    LEARNING_RATE,
    GAMMA,
    EPSILON_START,
    EPSILON_MIN,
    EPSILON_DECAY,
    BATCH_SIZE,
    MEMORY_SIZE,
    HIDDEN_DIM,
    GATE_8X8,
    GATE_6X6,
    GATE_4X4,
=======
from scripts.run_curriculum_complete_viable import (
    create_env, state_to_vector, train_phase, save_agent, load_agent,
    LEARNING_RATE, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    BATCH_SIZE, MEMORY_SIZE, HIDDEN_DIM,
    GATE_8X8, GATE_6X6, GATE_4X4
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
)
from sim.dqn_agent import DQNAgent

SEEDS = [13, 42, 101, 2025, 9999]
<<<<<<< HEAD
OUTPUT_DIR = Path(__file__).parent.parent / "results" / "pgf_v10_ablation" / "config_C_inverse" / "seeds"


def run_inverse_curriculum(seed: int, output_dir: Path):
    print("\n" + "=" * 70)
    print(f"SEED {seed}: Curriculum inverso 8x8 -> 6x6 -> 4x4")
    print("=" * 70)
=======
OUTPUT_DIR = ROOT / "results" / "pgf_v10_ablation" / "config_C_inverse" / "seeds"


def run_inverse_curriculum(seed, output_dir):
    print("\n" + "="*70)
    print(f"SEED {seed}: Curriculum inverso 8x8 -> 6x6 -> 4x4")
    print("="*70)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_summary = []

<<<<<<< HEAD
    # Fase 1: 8x8
=======
    # Fase 1: 8×8
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    env_8x8 = create_env(grid_size=8, max_steps_multiplier=3.0)
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
        num_episodes=1000,
        phase_name=f"8x8_seed{seed}",
<<<<<<< HEAD
        gate_threshold=GATE_8X8,
    )
    results_summary.append(
        {
            "seed": seed,
            "phase": "8x8",
            "grid_size": 8,
            "episodes": 1000,
            "success_rate_total": result_8x8["success_rate"],
            "success_last_100": result_8x8["last_100_success"],
            "gate": GATE_8X8 * 100,
            "gate_passed": result_8x8["gate_passed"],
            "first_success_episode": result_8x8["first_success"],
            "convergence_episode": result_8x8.get("convergence_episode", -1),
        }
    )
    pd.DataFrame(result_8x8["metrics"]).to_csv(output_dir / f"phase1_8x8_{timestamp}.csv", index=False)
    if not result_8x8["gate_passed"]:
        print(f"\nFAIL Seed {seed}: Fase 1 (8x8) falló gate")
=======
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
    df_8x8.to_csv(output_dir / f"phase1_8x8_{timestamp}.csv", index=False)
    if not result_8x8["gate_passed"]:
        print(f"\n⛔ Seed {seed}: Fase 1 (8×8) falló gate")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
        return results_summary
    model_8x8_path = output_dir / f"model_8x8_{timestamp}.pth"
    torch.save(agent_8x8.model.state_dict(), model_8x8_path)

<<<<<<< HEAD
    # Fase 2: 6x6
=======
    # Fase 2: 6×6
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    env_6x6 = create_env(grid_size=6, max_steps_multiplier=5.0)
    agent_6x6 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=0.9,
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
    load_agent(agent_6x6, model_8x8_path)
    result_6x6 = train_phase(
        env_6x6,
        agent_6x6,
        num_episodes=1000,
        phase_name=f"6x6_seed{seed}",
<<<<<<< HEAD
        gate_threshold=GATE_6X6,
    )
    results_summary.append(
        {
            "seed": seed,
            "phase": "6x6",
            "grid_size": 6,
            "episodes": 1000,
            "success_rate_total": result_6x6["success_rate"],
            "success_last_100": result_6x6["last_100_success"],
            "gate": GATE_6X6 * 100,
            "gate_passed": result_6x6["gate_passed"],
            "first_success_episode": result_6x6["first_success"],
            "convergence_episode": result_6x6.get("convergence_episode", -1),
        }
    )
    pd.DataFrame(result_6x6["metrics"]).to_csv(output_dir / f"phase2_6x6_{timestamp}.csv", index=False)
    if not result_6x6["gate_passed"]:
        print(f"\nFAIL Seed {seed}: Fase 2 (6x6) falló gate")
=======
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
    df_6x6.to_csv(output_dir / f"phase2_6x6_{timestamp}.csv", index=False)
    if not result_6x6["gate_passed"]:
        print(f"\n⛔ Seed {seed}: Fase 2 (6×6) falló gate")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
        return results_summary
    model_6x6_path = output_dir / f"model_6x6_{timestamp}.pth"
    torch.save(agent_6x6.model.state_dict(), model_6x6_path)

<<<<<<< HEAD
    # Fase 3: 4x4
=======
    # Fase 3: 4×4
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    env_4x4 = create_env(grid_size=4, max_steps_multiplier=4.0)
    agent_4x4 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=0.3,
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
    load_agent(agent_4x4, model_6x6_path)
    result_4x4 = train_phase(
        env_4x4,
        agent_4x4,
        num_episodes=500,
        phase_name=f"4x4_seed{seed}",
<<<<<<< HEAD
        gate_threshold=GATE_4X4,
    )
    results_summary.append(
        {
            "seed": seed,
            "phase": "4x4",
            "grid_size": 4,
            "episodes": 500,
            "success_rate_total": result_4x4["success_rate"],
            "success_last_100": result_4x4["last_100_success"],
            "gate": GATE_4X4 * 100,
            "gate_passed": result_4x4["gate_passed"],
            "first_success_episode": result_4x4["first_success"],
            "convergence_episode": result_4x4.get("convergence_episode", -1),
        }
    )
    pd.DataFrame(result_4x4["metrics"]).to_csv(output_dir / f"phase3_4x4_{timestamp}.csv", index=False)
    torch.save(agent_4x4.model.state_dict(), output_dir / f"model_4x4_{timestamp}.pth")
    pd.DataFrame(results_summary).to_csv(output_dir / f"inverse_curriculum_summary_{timestamp}.csv", index=False)
=======
        gate_threshold=GATE_4X4
    )
    results_summary.append({
        "seed": seed,
        "phase": "4x4",
        "grid_size": 4,
        "episodes": 500,
        "success_rate_total": result_4x4["success_rate"],
        "success_last_100": result_4x4["last_100_success"],
        "gate": GATE_4X4 * 100,
        "gate_passed": result_4x4["gate_passed"],
        "first_success_episode": result_4x4["first_success"],
        "convergence_episode": result_4x4.get("convergence_episode", -1)
    })
    df_4x4 = pd.DataFrame(result_4x4["metrics"])
    df_4x4.to_csv(output_dir / f"phase3_4x4_{timestamp}.csv", index=False)
    model_4x4_path = output_dir / f"model_4x4_{timestamp}.pth"
    torch.save(agent_4x4.model.state_dict(), model_4x4_path)
    df_summary = pd.DataFrame(results_summary)
    df_summary.to_csv(output_dir / f"inverse_curriculum_summary_{timestamp}.csv", index=False)
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)
    return results_summary


def main():
<<<<<<< HEAD
    print("=" * 70)
    print("ABLATION C: Curriculum inverso")
    print("=" * 70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} x 2500 episodes = {len(SEEDS) * 2500} episodes")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
=======
    print("="*70)
    print("ABLATION C: Curriculum inverso")
    print("="*70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} × 2500 episodes = {len(SEEDS) * 2500} episodes")
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
            summary = run_inverse_curriculum(seed, seed_dir)
            all_results.extend(summary)
            seed_duration = (time.time() - seed_start) / 60
<<<<<<< HEAD
            print(f"\nOK. Seed {seed} completado en {seed_duration:.1f} minutos")
            for res in summary:
                phase = res["phase"]
                success = res["success_last_100"]
                gate = res["gate"]
                passed = "OK" if res["gate_passed"] else "FAIL"
                print(f"   {phase}: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
            print(f"\nERROR en seed {seed}: {e}")
            import traceback
            traceback.print_exc()
    total_duration = (time.time() - start_time) / 3600
    print("\n" + "=" * 70)
    print("ABLATION C COMPLETADA")
    print("=" * 70)
    print(f"Duración total: {total_duration:.2f} horas")
    print(f"\nResultados guardados en: {OUTPUT_DIR}")

=======
            print(f"\n✅ Seed {seed} completado en {seed_duration:.1f} minutos")
            for res in summary:
                phase = res['phase']
                success = res['success_last_100']
                gate = res['gate']
                passed = "✅" if res['gate_passed'] else "❌"
                print(f"   {phase}: {success:.1f}% (gate {gate:.0f}%) {passed}")
        except Exception as e:
            print(f"\n❌ ERROR en seed {seed}: {e}")
            import traceback
            traceback.print_exc()
    total_duration = (time.time() - start_time) / 3600
    print("\n" + "="*70)
    print("ABLATION C COMPLETADA")
    print("="*70)
    print(f"Duración total: {total_duration:.2f} horas")
    print(f"\n📂 Resultados guardados en: {OUTPUT_DIR}")
>>>>>>> 7de8f43 (Ablation v10 Fase 1: runners corregidos, carpetas y documentación listas. Listo para ejecutar experimentos núcleo (A/B/C/D).)

if __name__ == "__main__":
    main()
