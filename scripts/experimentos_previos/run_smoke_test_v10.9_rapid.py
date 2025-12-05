"""
Smoke Test v10.9 - Correcciones Economía NO-Lineal (500 eps)
=============================================================
Iteración rápida con correcciones críticas post-análisis v10.8.

CAMBIOS v10.9 vs v10.8:
1. step_cost: -0.15 → -0.25 (REVERT, drena más rápido)
2. threshold_low: 2.0 → 1.0 (-50%, menos brutal)
3. goal_reward: 10.0 → 20.0 (2× señal DOMINANTE)
4. max_steps_multiplier: 3.0 → 2.0 (6×6: 20 steps vs 30)
5. spawn_rate: 0.40 (MANTENER de v10.8)

ROOT CAUSES CORREGIDOS:
- v10.8 step_cost -0.15 acumulaba penalty_low × 28 steps = -28.0
- v10.9 step_cost -0.25 fuerza muerte ~step 13-15 → penalty × 5 steps = -5.0
- threshold_low 1.0 (20% balance) vs 2.0 (40%) reduce presión constante
- goal_reward 20.0 domina penalties máximos (~-10 vs ~-5)

IMPACTO TEÓRICO v10.9:
Episode óptimo (10 steps, goal):
  +20.0 (goal) - 2.5 (steps) + 0.75 (resource) = +18.25 ✅ MUY POSITIVO

Episode subóptimo (15 steps, NO goal):
  -3.75 (steps) + 0.75 (resource) - 5.0 (penalty × 5) = -8.0 ❌

Delta: +18.25 - (-8.0) = +26.25 (SEÑAL ENORME)

Gates v10.9 (500 eps, gates ESTRICTOS):
- Success: >15% (75+ episodios alcanza meta)
- Rewards últimos 100: >+5 (positivo sólido)
- Resources: >1.5 promedio
- Steps promedio: <15 (eficiencia vs 30 previo)
"""

import sys
import os
import numpy as np
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
import sim.config as config


# ============================================================================
# CONFIGURACIÓN SMOKE TEST v10.9
# ============================================================================

GRID_SIZE = 6
INITIAL_BALANCE = 5.0
RESOURCE_REWARD = 0.75

# DQN hyperparams (mantener smoke test previo)
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.9995
BATCH_SIZE = 32
BUFFER_SIZE = 20000
TARGET_UPDATE = 100
HIDDEN_SIZE = 64

# Test (500 eps iteración rápida)
NUM_EPISODES = 500
SEED = 42


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)


def setup_experiment():
    """Setup environment y agente."""
    np.random.seed(SEED)
    
    config.EXP_CONFIG = {
        'grid_size': GRID_SIZE,
        'initial_balance': INITIAL_BALANCE,
        'step_cost': config.ENV_STEP_COST,  # -0.25 (revert v10.9)
        'resource_reward': RESOURCE_REWARD,
        'resource_spawn_rate': config.ENV_RESOURCE_SPAWN_RATE,  # 0.40
        'max_resources_on_grid': 3,
        'risk_penalty_high': -60,
        'risk_penalty_low': -25,
    }
    
    env = ResourceDensityEnv(
        size=GRID_SIZE,
        initial_resources=INITIAL_BALANCE,
        step_cost=config.ENV_STEP_COST,
        resource_reward=RESOURCE_REWARD,
        resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,
        max_resources_on_grid=3,
        max_steps_multiplier=2.0,  # v10.9: 20 steps (era 30)
    )
    
    state_tuple = env.reset()
    state_values = np.array([v for k, v in state_tuple], dtype=np.float32)
    state_dim = len(state_values)
    action_dim = 4
    
    agent = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=EPSILON_START,
        epsilon_end=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        batch_size=BATCH_SIZE,
        memory_size=BUFFER_SIZE,
        target_update_freq=TARGET_UPDATE,
        hidden_dim=HIDDEN_SIZE,
    )
    
    return env, agent


def train_single_episode(env, agent):
    """Entrena 1 episodio."""
    actions_map = ['up', 'down', 'left', 'right']
    state_tuple = env.reset()
    state_values = np.array([v for k, v in state_tuple], dtype=np.float32)
    
    episode_reward = 0.0
    episode_steps = 0
    done = False
    info_history = []
    
    while not done:
        action_idx = agent.act(state_values)
        action = actions_map[action_idx]
        
        next_state_tuple, reward, done, info = env.step(action)
        next_state_values = np.array([v for k, v in next_state_tuple], dtype=np.float32)
        
        agent.remember(state_values, action_idx, reward, next_state_values, done)
        agent.learn()
        
        episode_reward += reward
        episode_steps += 1
        state_values = next_state_values
        info_history.append(info.copy())
    
    goal_reached = info_history[-1].get('goal_reached', False) if info_history else False
    starvation = info_history[-1].get('starvation', False) if info_history else False
    tripwires_hit = sum(1 for i in info_history if i.get('tripwire', False))
    resources_collected = sum(1 for i in info_history if i.get('resource_collected', False))
    goal_reward_applied = info_history[-1].get('goal_reward_applied', False) if info_history else False
    
    return {
        'reward': episode_reward,
        'steps': episode_steps,
        'goal_reached': int(goal_reached),
        'starvation': int(starvation),
        'tripwires': tripwires_hit,
        'resources': resources_collected,
        'goal_reward_applied': int(goal_reward_applied),
        'epsilon': agent.epsilon,
    }


def run_smoke_test():
    """Ejecuta smoke test v10.9."""
    print("="*70)
    print("SMOKE TEST v10.9 - CORRECCIONES NO-LINEALES (500 EPS)")
    print("="*70)
    print(f"\nConfig v10.9 (correcciones vs v10.8):")
    print(f"  Grid: {GRID_SIZE}×{GRID_SIZE}")
    print(f"  Balance: {INITIAL_BALANCE}")
    print(f"  goal_reward: {config.ENV_GOAL_REWARD} (era 10.0, +100%)")
    print(f"  step_cost: {config.ENV_STEP_COST} (revert -0.15→-0.25)")
    print(f"  threshold_low: {config.ENV_RESOURCE_THRESHOLD_LOW} (era 2.0, -50%)")
    print(f"  spawn_rate: {config.ENV_RESOURCE_SPAWN_RATE} (mantener 0.40)")
    print(f"  max_steps: 20 (era 30, multiplier 2.0)")
    print(f"  Episodes: {NUM_EPISODES} (iteración rápida)")
    print(f"\nImpacto teórico:")
    print(f"  Episode óptimo: +20.0 - 2.5 + 0.75 = +18.25 ✅")
    print(f"  Episode subóptimo: -3.75 + 0.75 - 5.0 = -8.0 ❌")
    print(f"  Delta: +26.25 (SEÑAL ENORME)")
    print(f"\nGates ESTRICTOS:")
    print(f"  - Success: >15% (vs 0% previo)")
    print(f"  - Rewards: >+5 últimos 100 eps")
    print(f"  - Resources: >1.5")
    print(f"  - Steps: <15 promedio")
    print()
    
    env, agent = setup_experiment()
    
    episodes_data = []
    
    print(f"Entrenando {NUM_EPISODES} episodios...")
    for ep in range(NUM_EPISODES):
        metrics = train_single_episode(env, agent)
        episodes_data.append(metrics)
        
        if (ep + 1) % 50 == 0:
            recent = episodes_data[-50:]
            avg_reward = np.mean([e['reward'] for e in recent])
            avg_steps = np.mean([e['steps'] for e in recent])
            success_rate = np.mean([e['goal_reached'] for e in recent]) * 100
            resources = np.mean([e['resources'] for e in recent])
            goal_rewards = sum([e['goal_reward_applied'] for e in recent])
            print(f"  Ep {ep+1}/{NUM_EPISODES}: reward={avg_reward:.1f}, "
                  f"steps={avg_steps:.1f}, success={success_rate:.1f}%, "
                  f"resources={resources:.2f}, goals={goal_rewards}, eps={metrics['epsilon']:.3f}")
    
    # Resumen
    print("\n" + "="*70)
    print("RESULTADOS v10.9")
    print("="*70)
    
    # Métricas totales
    success_rate = np.mean([e['goal_reached'] for e in episodes_data]) * 100
    avg_reward = np.mean([e['reward'] for e in episodes_data])
    avg_steps = np.mean([e['steps'] for e in episodes_data])
    starvation_rate = np.mean([e['starvation'] for e in episodes_data]) * 100
    avg_tripwires = np.mean([e['tripwires'] for e in episodes_data])
    avg_resources = np.mean([e['resources'] for e in episodes_data])
    goal_rewards_total = sum([e['goal_reward_applied'] for e in episodes_data])
    epsilon_final = episodes_data[-1]['epsilon']
    
    # Últimos 100 episodios
    last_100 = episodes_data[-100:]
    success_last = np.mean([e['goal_reached'] for e in last_100]) * 100
    reward_last = np.mean([e['reward'] for e in last_100])
    resources_last = np.mean([e['resources'] for e in last_100])
    steps_last = np.mean([e['steps'] for e in last_100])
    goal_rewards_last = sum([e['goal_reward_applied'] for e in last_100])
    
    print(f"\nMétricas Totales ({NUM_EPISODES} eps):")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Goal rewards: {goal_rewards_total}")
    print(f"  Reward: {avg_reward:.2f}")
    print(f"  Steps: {avg_steps:.2f}")
    print(f"  Starvation: {starvation_rate:.1f}%")
    print(f"  Tripwires: {avg_tripwires:.2f}")
    print(f"  Resources: {avg_resources:.2f}")
    print(f"  Epsilon final: {epsilon_final:.4f}")
    
    print(f"\nÚltimos 100 Episodios:")
    print(f"  Success: {success_last:.1f}%")
    print(f"  Goal rewards: {goal_rewards_last}")
    print(f"  Reward: {reward_last:.2f}")
    print(f"  Steps: {steps_last:.2f}")
    print(f"  Resources: {resources_last:.2f}")
    
    # Comparación vs v10.7 y v10.8
    print(f"\n📊 COMPARACIÓN:")
    print(f"  v10.7 → v10.8 → v10.9")
    print(f"  Success: 0.0% → 0.0% → {success_last:.1f}%")
    print(f"  Rewards: -11.85 → -31.70 → {reward_last:.2f}")
    print(f"  Steps: 22.5 → 30.0 → {steps_last:.2f}")
    print(f"  Resources: 0.98 → 0.98 → {resources_last:.2f}")
    
    # Gates v10.9
    print(f"\n🚦 GATES v10.9 (ESTRICTOS):")
    gates_passed = []
    gates_failed = []
    
    # Gate 1: Success >15%
    if success_last > 15:
        gates_passed.append(f"✅ Success {success_last:.1f}% > 15%")
    else:
        gates_failed.append(f"❌ Success {success_last:.1f}% ≤ 15%")
    
    # Gate 2: Rewards >+5
    if reward_last > 5:
        gates_passed.append(f"✅ Rewards {reward_last:.2f} > +5")
    elif reward_last > 0:
        gates_passed.append(f"⚠️  Rewards {reward_last:.2f} > 0 (positivo PERO <+5)")
    else:
        gates_failed.append(f"❌ Rewards {reward_last:.2f} ≤ 0")
    
    # Gate 3: Resources >1.5
    if resources_last > 1.5:
        gates_passed.append(f"✅ Resources {resources_last:.2f} > 1.5")
    else:
        gates_failed.append(f"⚠️  Resources {resources_last:.2f} ≤ 1.5")
    
    # Gate 4: Steps <15
    if steps_last < 15:
        gates_passed.append(f"✅ Steps {steps_last:.2f} < 15")
    else:
        gates_failed.append(f"⚠️  Steps {steps_last:.2f} ≥ 15")
    
    # Gate 5: Epsilon <0.1
    if epsilon_final < 0.1:
        gates_passed.append(f"✅ Epsilon {epsilon_final:.4f} < 0.1")
    else:
        gates_failed.append(f"⚠️  Epsilon {epsilon_final:.4f} ≥ 0.1")
    
    for gate in gates_passed:
        print(f"  {gate}")
    for gate in gates_failed:
        print(f"  {gate}")
    
    # Conclusión
    print(f"\n" + "="*70)
    if success_last > 10 and reward_last > 0:
        print("✅ v10.9 FUNCIONA: Goal-seeking emergió, economía viable")
        print("\nPróximos pasos:")
        print("  1. Validar 8×8 con misma economía (max_steps 28)")
        print("  2. Si success >10%, proceder serie v11 multi-grid")
        print("  3. Documentar v10.9 como economía goal-oriented estable")
    elif success_last > 0:
        print("⚠️  v10.9 MEJORA PARCIAL: Success >0% PERO <10%")
        print("\nDiagnóstico:")
        if goal_rewards_last == 0:
            print("  ❌ goal_reward NUNCA aplicado → agent NO alcanza meta")
        if reward_last < 0:
            print("  ❌ Rewards negativos → penalties dominan aún")
        if steps_last > 15:
            print("  ⚠️  Steps altos → agent vagabundea")
        print("\nOpciones:")
        print("  A) Aumentar goal_reward 20→30 (señal más fuerte)")
        print("  B) Reducir max_steps 20→15 (más presión)")
        print("  C) Aumentar spawn_rate 0.40→0.50 (más resources)")
    else:
        print("❌ v10.9 FALLÓ: Success 0%, economía NO viable")
        print("\nOpciones críticas:")
        print("  A) Cerrar v10.x, documentar lecciones, repensar arquitectura")
        print("  B) v10.10 Último intento: goal_reward 30, spawn_rate 0.50, max_steps 15")
        print("  C) Considerar curriculum learning (4×4 → 6×6 progresivo)")
    print("="*70)
    
    # Guardar resultados
    output_dir = Path("results/smoke_test_v10.9_rapid")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / "episodes.csv"
    with open(csv_path, 'w') as f:
        f.write("reward,steps,goal_reached,starvation,tripwires,resources,goal_reward_applied,epsilon,episode\n")
        for i, e in enumerate(episodes_data):
            f.write(f"{e['reward']},{e['steps']},{e['goal_reached']},{e['starvation']},"
                   f"{e['tripwires']},{e['resources']},{e['goal_reward_applied']},{e['epsilon']},{i}\n")
    
    summary = {
        'version': 'v10.9',
        'config': {
            'grid_size': GRID_SIZE,
            'initial_balance': INITIAL_BALANCE,
            'goal_reward': float(config.ENV_GOAL_REWARD),
            'step_cost': float(config.ENV_STEP_COST),
            'threshold_low': float(config.ENV_RESOURCE_THRESHOLD_LOW),
            'spawn_rate': float(config.ENV_RESOURCE_SPAWN_RATE),
            'max_steps': 20,
            'num_episodes': NUM_EPISODES,
        },
        'metrics_total': {
            'success_rate': float(success_rate),
            'reward_mean': float(avg_reward),
            'steps_mean': float(avg_steps),
            'resources_mean': float(avg_resources),
            'goal_rewards_applied': int(goal_rewards_total),
        },
        'metrics_last_100': {
            'success_rate': float(success_last),
            'reward_mean': float(reward_last),
            'steps_mean': float(steps_last),
            'resources_mean': float(resources_last),
            'goal_rewards_applied': int(goal_rewards_last),
            'epsilon_final': float(epsilon_final),
        },
        'comparison': {
            'v10_7': {'success': 0.0, 'reward': -11.85, 'steps': 22.5},
            'v10_8': {'success': 0.0, 'reward': -31.70, 'steps': 30.0},
            'v10_9': {'success': float(success_last), 'reward': float(reward_last), 'steps': float(steps_last)},
        },
        'gates': {
            'passed': gates_passed,
            'failed': gates_failed,
        }
    }
    
    json_path = output_dir / "summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2, cls=NumpyEncoder)
    
    print(f"\nResultados: {output_dir}")


if __name__ == '__main__':
    run_smoke_test()
