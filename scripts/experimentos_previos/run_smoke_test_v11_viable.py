"""
Smoke Test v11 - Economía VIABLE validada por oráculo
======================================================

Config v11 (VIABLE):
- Balance inicial: 8.0 (autonomía 53 pasos)
- step_cost: -0.15 (menor fricción)
- penalty_low: -0.5 (menos brutal)
- threshold_low: 1.0 (12.5% balance)
- goal_reward: 20.0 (incentivo fuerte)
- spawn_rate: 0.40 (40% celdas)
- max_steps_multiplier: 2.0 (2× Manhattan)

Oráculo: 100% success en 6×6, 8×8, 16×16
DQN Test: 500 eps por grid (6×6, 8×8)

Gates:
- Success >10% (vs 0% v10.x)
- Reward promedio >0 (vs -28 v10.9)
- Resources recolectados >1.5
- Agent alcanza meta ≥1 vez en 500 eps

Si falla: problema es exploración/curriculum, NO economía.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
from sim import config

# Verificar config v11
print("="*70)
print("SMOKE TEST v11 - Economía VIABLE (Oráculo validado)")
print("="*70)
print(f"\nConfig v11:")
print(f"  initial_resources: {config.ENV_INITIAL_RESOURCES} (autonomía {config.ENV_INITIAL_RESOURCES/abs(config.ENV_STEP_COST):.1f} pasos)")
print(f"  step_cost: {config.ENV_STEP_COST}")
print(f"  penalty_low: {config.ENV_PENALTY_LOW_RESOURCES}")
print(f"  threshold_low: {config.ENV_RESOURCE_THRESHOLD_LOW}")
print(f"  goal_reward: {config.ENV_GOAL_REWARD}")
print(f"  spawn_rate: {config.ENV_RESOURCE_SPAWN_RATE}")
print()

# Hiperparámetros DQN estándar
NUM_EPISODES = 500
GRIDS = [6, 8]  # Test 6×6 y 8×8
MAX_STEPS_MULTIPLIER = 2.0  # 2× Manhattan (validado oráculo)

# Gates v11 (más estrictos que v10.x porque economía ES viable)
GATES = {
    "success_rate": 0.10,      # >10% (vs 0% v10.x)
    "reward_mean": 0.0,        # >0 (vs -28 v10.9)
    "resources_mean": 1.5,     # >1.5 (vs 0.67 v10.9)
    "goal_reached_once": True, # Al menos 1 vez en 500 eps
}

def state_to_vector(state):
    """Convertir estado abstracto (tupla de pares) a vector numérico"""
    if isinstance(state, tuple):
        # state es [(key1, val1), (key2, val2), ...]
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)

def run_smoke_test(grid_size):
    """Smoke test DQN en grid específico"""
    manhattan = (grid_size - 1) * 2
    max_steps = int(manhattan * MAX_STEPS_MULTIPLIER)
    
    print(f"\n{'='*70}")
    print(f"Grid {grid_size}×{grid_size} (Manhattan={manhattan}, max_steps={max_steps})")
    print(f"{'='*70}")
    
    # Environment
    env = ResourceDensityEnv(
        size=grid_size,
        initial_resources=config.ENV_INITIAL_RESOURCES,
        step_cost=config.ENV_STEP_COST,
        resource_reward=0.75,
        resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,
        max_steps_multiplier=MAX_STEPS_MULTIPLIER,
    )
    
    # DQN Agent con hiperparámetros estándar
    # State size: features abstractos (coord_x, coord_y, recursos_altos, recursos_bajos, etc.)
    state = env.reset()
    state_size = len(state) if isinstance(state, tuple) else 1
    action_size = 5  # up, down, left, right, noop
    
    agent = DQNAgent(
        state_dim=state_size,
        action_dim=action_size,
        lr=config.DQN_LEARNING_RATE,
        gamma=config.DQN_GAMMA,
        epsilon=1.0,  # Start con exploración máxima
        epsilon_decay=config.DQN_EPSILON_DECAY,
        epsilon_end=config.DQN_EPSILON_END,
        batch_size=32,  # Batch size estándar
        memory_size=10000,  # Memory size estándar
    )
    
    # Métricas
    metrics = {
        "success": [],
        "rewards": [],
        "steps": [],
        "resources": [],
        "starvation": [],
        "tripwires": [],
        "epsilon": [],
        "goal_reached_count": 0,
    }
    
    # Training loop
    for ep in range(NUM_EPISODES):
        state = env.reset()
        state_vec = state_to_vector(state)
        done = False
        total_reward = 0
        steps = 0
        
        while not done:
            action = agent.act(state_vec)
            next_state, reward, done, info = env.step(action)
            next_state_vec = state_to_vector(next_state)
            agent.remember(state_vec, action, reward, next_state_vec, done)
            agent.learn()  # DQNAgent usa learn() no replay()
            
            state = next_state
            state_vec = next_state_vec
            total_reward += reward
            steps += 1
        
        # Registrar métricas
        metrics["success"].append(1 if info.get('goal_reached', False) else 0)
        metrics["rewards"].append(total_reward)
        metrics["steps"].append(steps)
        metrics["resources"].append(env.total_resources_collected)
        metrics["starvation"].append(1 if info.get('starvation', False) else 0)
        metrics["tripwires"].append(1 if info.get('tripwire', False) else 0)
        metrics["epsilon"].append(agent.epsilon)
        
        if info.get('goal_reached', False):
            metrics["goal_reached_count"] += 1
        
        # Progress cada 50 eps
        if (ep + 1) % 50 == 0:
            recent_success = np.mean(metrics["success"][-50:]) * 100
            recent_reward = np.mean(metrics["rewards"][-50:])
            recent_resources = np.mean(metrics["resources"][-50:])
            print(f"  Ep {ep+1:3d}: success={recent_success:5.1f}%, reward={recent_reward:+7.2f}, resources={recent_resources:.2f}, ε={agent.epsilon:.4f}")
    
    # Resultados finales
    last_100 = min(100, NUM_EPISODES)
    success_rate = np.mean(metrics["success"][-last_100:]) * 100
    reward_mean = np.mean(metrics["rewards"][-last_100:])
    resources_mean = np.mean(metrics["resources"][-last_100:])
    steps_mean = np.mean(metrics["steps"][-last_100:])
    starvation_rate = np.mean(metrics["starvation"][-last_100:]) * 100
    
    print(f"\n{'='*70}")
    print(f"RESULTADOS {grid_size}×{grid_size} (últimos {last_100} eps)")
    print(f"{'='*70}")
    print(f"Success: {success_rate:.1f}% (total: {metrics['goal_reached_count']}/{NUM_EPISODES})")
    print(f"Reward: {reward_mean:.2f}")
    print(f"Resources: {resources_mean:.2f}")
    print(f"Steps: {steps_mean:.1f} / {max_steps}")
    print(f"Starvation: {starvation_rate:.1f}%")
    print(f"Epsilon final: {agent.epsilon:.4f}")
    
    # Evaluación gates
    print(f"\n{'='*70}")
    print(f"GATES v11 (Economía VIABLE)")
    print(f"{'='*70}")
    
    gates_passed = 0
    gates_total = len(GATES)
    
    if success_rate > GATES["success_rate"] * 100:
        print(f"✅ Success {success_rate:.1f}% > {GATES['success_rate']*100:.1f}%")
        gates_passed += 1
    else:
        print(f"❌ Success {success_rate:.1f}% ≤ {GATES['success_rate']*100:.1f}%")
    
    if reward_mean > GATES["reward_mean"]:
        print(f"✅ Reward {reward_mean:.2f} > {GATES['reward_mean']:.2f}")
        gates_passed += 1
    else:
        print(f"❌ Reward {reward_mean:.2f} ≤ {GATES['reward_mean']:.2f}")
    
    if resources_mean > GATES["resources_mean"]:
        print(f"✅ Resources {resources_mean:.2f} > {GATES['resources_mean']:.2f}")
        gates_passed += 1
    else:
        print(f"❌ Resources {resources_mean:.2f} ≤ {GATES['resources_mean']:.2f}")
    
    if metrics["goal_reached_count"] > 0:
        print(f"✅ Goal alcanzado {metrics['goal_reached_count']} veces (≥1)")
        gates_passed += 1
    else:
        print(f"❌ Goal NUNCA alcanzado (0/{NUM_EPISODES})")
    
    print(f"\nGates: {gates_passed}/{gates_total} ({'✅ APROBADO' if gates_passed == gates_total else '❌ FALLIDO'})")
    
    return {
        "grid": grid_size,
        "success_rate": success_rate,
        "reward_mean": reward_mean,
        "resources_mean": resources_mean,
        "steps_mean": steps_mean,
        "starvation_rate": starvation_rate,
        "epsilon_final": agent.epsilon,
        "goal_reached_total": metrics["goal_reached_count"],
        "gates_passed": gates_passed,
        "gates_total": gates_total,
    }

if __name__ == "__main__":
    results = []
    
    for grid_size in GRIDS:
        result = run_smoke_test(grid_size)
        results.append(result)
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"RESUMEN SMOKE TEST v11 - Economía VIABLE")
    print(f"{'='*70}")
    
    df = pd.DataFrame(results)
    print(f"\n{df.to_string(index=False)}")
    
    # Veredicto
    all_passed = all(r["gates_passed"] == r["gates_total"] for r in results)
    
    print(f"\n{'='*70}")
    print(f"VEREDICTO FINAL")
    print(f"{'='*70}")
    
    if all_passed:
        print(f"✅ ECONOMÍA v11 VIABLE + DQN APRENDE")
        print(f"   → Oráculo 100% + DQN >10% success")
        print(f"   → Problema v10.x ERA bug threshold_high + economía tight")
        print(f"   → v11 es baseline funcional para curriculum/shaping")
    else:
        print(f"❌ ECONOMÍA v11 VIABLE PERO DQN NO APRENDE")
        print(f"   → Oráculo 100% success PERO DQN ≤10%")
        print(f"   → Problema es EXPLORACIÓN/ARQUITECTURA:")
        print(f"     - Sparse rewards (solo goal_reward, no shaping)")
        print(f"     - Random exploration insuficiente (ε-greedy)")
        print(f"     - DQN converge a mínimo local (camping)")
        print(f"\n   → Soluciones:")
        print(f"     A) Curriculum learning (4×4 → 6×6 → 8×8)")
        print(f"     B) Shaped rewards (distance-based bonus)")
        print(f"     C) Exploration bonus (count-based novelty)")
        print(f"     D) Behavioral cloning (pretrain con demos oráculo)")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = ROOT / "results" / f"smoke_test_v11_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_dir / "summary.csv", index=False)
    print(f"\nResultados guardados: {output_dir}")
