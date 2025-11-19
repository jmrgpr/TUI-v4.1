"""
CURRICULUM COMPLETO VIABLE: Progresión 4×4 → 6×6 → 8×8 con Transfer Learning
===============================================================================

Economía viable (serie 10.x):
- Balance inicial: 8.0 (autonomía 53 pasos)
- step_cost: -0.15 (fricción baja)
- penalty_low: -0.5 (exploración viable)
- goal_reward: 20.0 (incentivo fuerte)
- spawn_rate: 0.40 (40% celdas)

FASES:
1. 4×4: 500 eps, gate >80%, guarda modelo
2. 6×6: Transfer 4×4, 1000 eps, gate >20%
3. 8×8: Transfer 6×6, 1000 eps, gate >10%

Usa mapeo correcto INT→STRING (bug action mapping resuelto)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
from sim import config

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Economía viable (desde config.py - serie 10.x)
INITIAL_RESOURCES = config.ENV_INITIAL_RESOURCES  # 8.0
STEP_COST = config.ENV_STEP_COST  # -0.15
RESOURCE_SPAWN_RATE = config.ENV_RESOURCE_SPAWN_RATE  # 0.40

# Hiperparámetros DQN (calibrados para curriculum)
LEARNING_RATE = 0.001
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.995  # Más lento aún (curriculum complejo)
BATCH_SIZE = 32
MEMORY_SIZE = 10000
HIDDEN_DIM = 128  # Red profunda para escalabilidad

# Gates de validación
GATE_4X4 = 0.80  # 80% success
GATE_6X6 = 0.20  # 20% success  
GATE_8X8 = 0.10  # 10% success

# Output (estructura estándar serie 10.x)
OUTPUT_DIR = ROOT / "results" / "pgf_v10_viable" / "resultados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def state_to_vector(state):
    """Convierte tuple state a vector flat"""
    if isinstance(state, tuple):
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)


def create_env(grid_size, max_steps_multiplier):
    """Crea environment con economía viable"""
    return ResourceDensityEnv(
        size=grid_size,
        initial_resources=INITIAL_RESOURCES,
        step_cost=STEP_COST,
        resource_spawn_rate=RESOURCE_SPAWN_RATE,
        max_steps_multiplier=max_steps_multiplier
    )


def train_phase(env, agent, num_episodes, phase_name, gate_threshold):
    """
    Entrena una fase del curriculum
    
    Returns:
        dict con métricas y status (passed/failed gate)
    """
    print(f"\n{'='*70}")
    print(f"FASE: {phase_name}")
    print(f"{'='*70}")
    print(f"Grid: {env.size}×{env.size}")
    print(f"Episodios: {num_episodes}")
    print(f"max_steps: {env.max_steps}")
    print(f"Gate: Success >{gate_threshold*100:.0f}% (últimos 100 eps)")
    print(f"Epsilon: {agent.epsilon:.4f} → {agent.epsilon_end}")
    print()
    
    metrics = {
        "success": [],
        "rewards": [],
        "steps": [],
        "resources": [],
        "epsilon": [],
        "first_success": None
    }
    
    for ep in range(num_episodes):
        state = env.reset()
        state_vec = state_to_vector(state)
        done = False
        total_reward = 0
        steps = 0
        
        while not done:
            action_idx = agent.act(state_vec)
            
            # ✅ FIX: Mapeo INT → STRING
            action_str = config.AGENT_ACTIONS[action_idx]
            
            next_state, reward, done, info = env.step(action_str)
            next_state_vec = state_to_vector(next_state)
            agent.remember(state_vec, action_idx, reward, next_state_vec, done)
            agent.learn()
            
            state_vec = next_state_vec
            total_reward += reward
            steps += 1
        
        # Métricas
        success = 1 if info.get('goal_reached', False) else 0
        metrics["success"].append(success)
        metrics["rewards"].append(total_reward)
        metrics["steps"].append(steps)
        metrics["resources"].append(env.total_resources_collected)
        metrics["epsilon"].append(agent.epsilon)
        
        if success and metrics["first_success"] is None:
            metrics["first_success"] = ep + 1
        
        # Progress cada 50 eps
        if (ep + 1) % 50 == 0:
            recent_success = np.mean(metrics["success"][-50:]) * 100
            recent_reward = np.mean(metrics["rewards"][-50:])
            recent_steps = np.mean(metrics["steps"][-50:])
            
            print(f"Ep {ep+1:4d}: success={recent_success:5.1f}%, "
                  f"reward={recent_reward:+7.2f}, "
                  f"steps={recent_steps:5.1f}, "
                  f"ε={agent.epsilon:.4f}")
            
            # Checkpoint cada 100 eps
            if (ep + 1) % 100 == 0:
                checkpoint_path = OUTPUT_DIR / f"checkpoint_{phase_name}_ep{ep+1}_{TIMESTAMP}.pth"
                torch.save(agent.model.state_dict(), checkpoint_path)
                print(f"    💾 Checkpoint: {checkpoint_path.name}")
    
    # Resultados finales
    total_success = sum(metrics["success"])
    success_rate = total_success / num_episodes
    last_100_success = np.mean(metrics["success"][-100:])
    
    print(f"\n{'='*70}")
    print(f"RESULTADOS {phase_name}")
    print(f"{'='*70}")
    print(f"Success total: {success_rate*100:.1f}% ({total_success}/{num_episodes})")
    print(f"Últimos 100: {last_100_success*100:.1f}%")
    print(f"Primer éxito: Episodio {metrics['first_success'] if metrics['first_success'] else 'NUNCA'}")
    print(f"Epsilon final: {agent.epsilon:.4f}")
    
    # Gate
    gate_passed = last_100_success >= gate_threshold
    print(f"\n{'='*70}")
    print(f"GATE {phase_name}")
    print(f"{'='*70}")
    
    if gate_passed:
        print(f"✅ GATE PASADO: {last_100_success*100:.1f}% ≥ {gate_threshold*100:.0f}%")
        print(f"   → Proceder siguiente fase")
    else:
        print(f"❌ GATE FALLIDO: {last_100_success*100:.1f}% < {gate_threshold*100:.0f}%")
        print(f"   → Detener curriculum")
    
    return {
        "metrics": metrics,
        "success_rate": success_rate,
        "last_100_success": last_100_success,
        "gate_passed": gate_passed,
        "first_success": metrics["first_success"]
    }


def save_agent(agent, phase_name):
    """Guarda pesos del agente"""
    model_path = OUTPUT_DIR / f"model_{phase_name}_{TIMESTAMP}.pth"
    torch.save(agent.model.state_dict(), model_path)
    print(f"\n💾 Modelo guardado: {model_path.relative_to(ROOT)}")
    return model_path


def load_agent(agent, model_path):
    """Carga pesos en agente (transfer learning)"""
    agent.model.load_state_dict(torch.load(model_path))
    agent.target_model.load_state_dict(agent.model.state_dict())
    print(f"📥 Pesos cargados desde: {model_path.relative_to(ROOT)}")


# ============================================================================
# MAIN CURRICULUM
# ============================================================================

def main():
    print("="*70)
    print("CURRICULUM COMPLETO VIABLE: 4×4 → 6×6 → 8×8")
    print("="*70)
    print(f"\nEconomía viable (serie 10.x):")
    print(f"  initial_resources: {INITIAL_RESOURCES}")
    print(f"  step_cost: {STEP_COST}")
    print(f"  spawn_rate: {RESOURCE_SPAWN_RATE}")
    print(f"\nHiperparámetros:")
    print(f"  learning_rate: {LEARNING_RATE}")
    print(f"  epsilon_decay: {EPSILON_DECAY}")
    print(f"  epsilon_min: {EPSILON_MIN}")
    print(f"  hidden_dim: {HIDDEN_DIM}")
    
    results_summary = []
    
    # ========================================================================
    # FASE 1: 4×4 (Baseline)
    # ========================================================================
    
    env_4x4 = create_env(grid_size=4, max_steps_multiplier=4.0)
    state = env_4x4.reset()
    state_dim = len(state_to_vector(state))  # 11 features (independiente de grid size)
    action_dim = 5  # up, down, left, right, noop
    
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
        phase_name="4x4",
        gate_threshold=GATE_4X4
    )
    
    results_summary.append({
        "phase": "4x4",
        "success_rate": result_4x4["success_rate"],
        "last_100": result_4x4["last_100_success"],
        "gate_passed": result_4x4["gate_passed"],
        "first_success": result_4x4["first_success"]
    })
    
    # Guardar métricas
    df_4x4 = pd.DataFrame(result_4x4["metrics"])
    df_4x4.to_csv(OUTPUT_DIR / f"phase1_4x4_{TIMESTAMP}.csv", index=False)
    
    if not result_4x4["gate_passed"]:
        print("\n" + "="*70)
        print("⛔ CURRICULUM ABORTADO: Fase 1 (4×4) falló gate")
        print("="*70)
        return
    
    # Guardar modelo 4×4
    model_4x4_path = save_agent(agent_4x4, "4x4")
    
    # ========================================================================
    # FASE 2: 6×6 (Transfer Learning)
    # ========================================================================
    
    env_6x6 = create_env(grid_size=6, max_steps_multiplier=5.0)  # 50 steps (más margen)
    
    # Nuevo agente 6×6 con MISMA arquitectura (state_dim=11 es universal)
    agent_6x6 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=0.9,  # Alta exploración (grid más complejo, transfer learning)
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
        hidden_dim=HIDDEN_DIM
    )
    
    # Transfer learning: cargar pesos 4×4
    load_agent(agent_6x6, model_4x4_path)
    
    result_6x6 = train_phase(
        env_6x6,
        agent_6x6,
        num_episodes=1000,
        phase_name="6x6",
        gate_threshold=GATE_6X6
    )
    
    results_summary.append({
        "phase": "6x6",
        "success_rate": result_6x6["success_rate"],
        "last_100": result_6x6["last_100_success"],
        "gate_passed": result_6x6["gate_passed"],
        "first_success": result_6x6["first_success"]
    })
    
    df_6x6 = pd.DataFrame(result_6x6["metrics"])
    df_6x6.to_csv(OUTPUT_DIR / f"phase2_6x6_{TIMESTAMP}.csv", index=False)
    
    if not result_6x6["gate_passed"]:
        print("\n" + "="*70)
        print("⛔ CURRICULUM ABORTADO: Fase 2 (6×6) falló gate")
        print("="*70)
        return
    
    model_6x6_path = save_agent(agent_6x6, "6x6")
    
    # ========================================================================
    # FASE 3: 8×8 (Transfer Learning)
    # ========================================================================
    
    env_8x8 = create_env(grid_size=8, max_steps_multiplier=3.0)
    
    # Nuevo agente 8×8 con MISMA arquitectura (state_dim=11 es universal)
    agent_8x8 = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=0.3,  # Aún menos exploración (transfer learning)
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=MEMORY_SIZE,
        hidden_dim=HIDDEN_DIM
    )
    
    # Transfer learning: cargar pesos 6×6
    load_agent(agent_8x8, model_6x6_path)
    
    result_8x8 = train_phase(
        env_8x8,
        agent_8x8,
        num_episodes=1000,
        phase_name="8x8",
        gate_threshold=GATE_8X8
    )
    
    results_summary.append({
        "phase": "8x8",
        "success_rate": result_8x8["success_rate"],
        "last_100": result_8x8["last_100_success"],
        "gate_passed": result_8x8["gate_passed"],
        "first_success": result_8x8["first_success"]
    })
    
    df_8x8 = pd.DataFrame(result_8x8["metrics"])
    df_8x8.to_csv(OUTPUT_DIR / f"phase3_8x8_{TIMESTAMP}.csv", index=False)
    
    if result_8x8["gate_passed"]:
        save_agent(agent_8x8, "8x8")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    
    print("\n" + "="*70)
    print("RESUMEN CURRICULUM COMPLETO")
    print("="*70)
    
    df_summary = pd.DataFrame(results_summary)
    print(f"\n{df_summary.to_string(index=False)}")
    
    df_summary.to_csv(OUTPUT_DIR / f"curriculum_summary_{TIMESTAMP}.csv", index=False)
    
    all_passed = all(r["gate_passed"] for r in results_summary)
    
    print(f"\n{'='*70}")
    if all_passed:
        print("🎉 CURRICULUM COMPLETO EXITOSO")
        print("   ✅ Todas las fases pasaron gates")
        print("   ✅ Transfer learning funcional")
        print("   ✅ Economía viable escalable (serie 10.x)")
        print(f"   → Considerar Fase 4: 16×16 (opcional)")
    else:
        failed_phases = [r["phase"] for r in results_summary if not r["gate_passed"]]
        print(f"⚠️  CURRICULUM PARCIAL")
        print(f"   Fases fallidas: {', '.join(failed_phases)}")
        print(f"   → Ajustar gates o hiperparámetros")
    print("="*70)
    
    print(f"\nResultados guardados en: {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
