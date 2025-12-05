"""
RUNNER MULTI-SEED: Validación v10_viable con N=5 seeds
========================================================

Corre curriculum 4×4→6×6→8×8 con 5 seeds independientes:
- Seeds: [13, 42, 101, 2025, 9999]
- Seed 42: crea symlink a v10_viable (baseline)
- Resto: ejecuta curriculum completo

Guarda resultados en estructura separada para no contaminar baseline.
"""

import sys
import os
from pathlib import Path
import time
<<<<<<< HEAD
<<<<<<< HEAD
import numpy as np
=======
>>>>>>> 61e07a7 (Fase 0: Roadmap v10 completo - Estructura multi-seed/ablation/PGF offline)
=======
import numpy as np
>>>>>>> 8324c5b (Fix: Eliminar parámetro seed de DQNAgent (no existe))

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# Import después de sys.path
from scripts.run_curriculum_complete_viable import (
    create_env, state_to_vector, train_phase, save_agent, load_agent,
    INITIAL_RESOURCES, STEP_COST, RESOURCE_SPAWN_RATE,
    LEARNING_RATE, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    BATCH_SIZE, MEMORY_SIZE, HIDDEN_DIM,
    GATE_4X4, GATE_6X6, GATE_8X8
)
from sim.dqn_agent import DQNAgent
import pandas as pd
import torch
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

SEEDS = [13, 42, 101, 2025, 9999]

MULTISEED_DIR = ROOT / "results" / "pgf_v10_multiseed"
VIABLE_DIR = ROOT / "results" / "pgf_v10_viable" / "resultados"

# ============================================================================
# RUNNER
# ============================================================================

def run_curriculum_seed(seed, output_dir):
    """
    Corre curriculum completo para una seed.
    
    Returns:
        dict con resultados summary
    """
    print(f"\n{'='*70}")
    print(f"🎲 SEED {seed}: Curriculum 4×4 → 6×6 → 8×8")
    print(f"{'='*70}")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results_summary = []
    
    # Fase 1: 4×4
    env_4x4 = create_env(grid_size=4, max_steps_multiplier=4.0)
    state = env_4x4.reset(seed=seed)
    state_dim = len(state_to_vector(state))
    action_dim = 5
    
    # Establecer seed global para reproducibilidad
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    agent_4x4 = DQNAgent(
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
    
    result_4x4 = train_phase(
        env_4x4,
        agent_4x4,
        num_episodes=500,
        phase_name=f"4x4_seed{seed}",
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
    df_4x4.to_csv(output_dir / f"phase1_4x4_{timestamp}.csv", index=False)
    
    if not result_4x4["gate_passed"]:
        print(f"\n⛔ Seed {seed}: Fase 1 (4×4) falló gate")
        return results_summary
    
    model_4x4_path = output_dir / f"model_4x4_{timestamp}.pth"
    torch.save(agent_4x4.model.state_dict(), model_4x4_path)
    
    # Fase 2: 6×6
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
    hidden_dim=HIDDEN_DIM
    )
    
    load_agent(agent_6x6, model_4x4_path)
    
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
    df_6x6.to_csv(output_dir / f"phase2_6x6_{timestamp}.csv", index=False)
    
    if not result_6x6["gate_passed"]:
        print(f"\n⛔ Seed {seed}: Fase 2 (6×6) falló gate")
        return results_summary
    
    model_6x6_path = output_dir / f"model_6x6_{timestamp}.pth"
    torch.save(agent_6x6.model.state_dict(), model_6x6_path)
    
    # Fase 3: 8×8
    env_8x8 = create_env(grid_size=8, max_steps_multiplier=3.0)
    
    agent_8x8 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=0.3,
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
    hidden_dim=HIDDEN_DIM
    )
    
    load_agent(agent_8x8, model_6x6_path)
    
    result_8x8 = train_phase(
        env_8x8,
        agent_8x8,
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
    df_8x8.to_csv(output_dir / f"phase3_8x8_{timestamp}.csv", index=False)
    
    if result_8x8["gate_passed"]:
        model_8x8_path = output_dir / f"model_8x8_{timestamp}.pth"
        torch.save(agent_8x8.model.state_dict(), model_8x8_path)
    
    # Guardar summary
    df_summary = pd.DataFrame(results_summary)
    df_summary.to_csv(output_dir / f"curriculum_summary_{timestamp}.csv", index=False)
    
    return results_summary


def main():
    print("="*70)
    print("MULTI-SEED VALIDATION: v10_viable Curriculum")
    print("="*70)
    print(f"\nSeeds: {SEEDS}")
    print(f"Total runs: {len(SEEDS)} × 2500 episodes = {len(SEEDS) * 2500} episodes")
    print(f"Duración estimada: ~8-10 horas\n")
    
    MULTISEED_DIR.mkdir(exist_ok=True)
    seeds_dir = MULTISEED_DIR / "seeds"
    seeds_dir.mkdir(exist_ok=True)
    
    all_results = []
    start_time = time.time()
    
    for i, seed in enumerate(SEEDS, 1):
        seed_dir = seeds_dir / f"seed_{seed:04d}"
        
        print(f"\n{'#'*70}")
        print(f"# SEED {seed} ({i}/{len(SEEDS)})")
        print(f"{'#'*70}")
        
        # Seed 42: crear symlink a v10_viable
        if seed == 42:
            if not seed_dir.exists():
                try:
                    # Windows: crear junction (más compatible que symlink)
                    if os.name == 'nt':
                        import subprocess
                        subprocess.run([
                            'mklink', '/J',
                            str(seed_dir.resolve()),
                            str(VIABLE_DIR.resolve())
                        ], shell=True, check=True)
                    else:
                        seed_dir.symlink_to(VIABLE_DIR.resolve(), target_is_directory=True)
                    
                    print(f"✅ Seed 42: Junction/symlink creado → v10_viable")
                except Exception as e:
                    print(f"⚠️ No se pudo crear symlink: {e}")
                    print(f"   Copiando manualmente archivos de v10_viable...")
                    import shutil
                    shutil.copytree(VIABLE_DIR, seed_dir, dirs_exist_ok=True)
            else:
                print(f"✅ Seed 42: Ya existe (baseline v10_viable)")
            
            # Cargar summary de v10_viable
            viable_summary = list(VIABLE_DIR.glob("curriculum_summary_*.csv"))
            if viable_summary:
                df_42 = pd.read_csv(viable_summary[0])
                df_42['seed'] = 42
                all_results.append(df_42)
            
            continue
        
        # Otras seeds: ejecutar curriculum
        seed_start = time.time()
        
        try:
            summary = run_curriculum_seed(seed, seed_dir)
            all_results.extend(summary)
            
            seed_duration = (time.time() - seed_start) / 60
            print(f"\n✅ Seed {seed} completado en {seed_duration:.1f} minutos")
            
            # Mostrar resultados
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
    
    # Resumen final
    total_duration = (time.time() - start_time) / 3600
    
    print("\n" + "="*70)
    print("MULTI-SEED VALIDATION COMPLETADA")
    print("="*70)
    print(f"Duración total: {total_duration:.2f} horas")
    print(f"\n📂 Resultados guardados en: {MULTISEED_DIR}")
    print(f"\n✅ Próximo paso: Ejecutar análisis agregado")
    print(f"   python scripts/analisis_multiseed_v10.py")


if __name__ == "__main__":
    main()
