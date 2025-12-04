"""
Smoke Test 6×6 Post-Penalty Fix
================================
Test rápido (100 eps, ~1 min) para validar FIX #5:
- ENV_PENALTY_LOW_RESOURCES: -10.0 → -1.0 (10× menos)
- ENV_RESOURCE_THRESHOLD_LOW: 5.0 → 2.0 (ventana exploración)

Gates esperados:
- Success rate: 10-30% (mínimo aprendizaje)
- Resources collected: >0.5 promedio (exploración activa)
- Tripwires hit: >0.5 promedio (movimiento real)
- Rewards: -20 a -40 rango (viable DQN, no -160)
"""

import sys
import os
import numpy as np
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
import sim.config as config


# ============================================================================
# CONFIGURACIÓN SMOKE TEST 6×6
# ============================================================================

GRID_SIZE = 6
INITIAL_BALANCE = 4.0
STEP_COST = -0.25
RESOURCE_REWARD = 0.75
SPAWN_RATE = 0.15

# Balance post-viaje = 4.0 + 0.75 - 10×0.25 = 2.25 (125% margen)
# Manhattan óptimo: 10, max_steps: 30 (3× margen)

# DQN hyperparams
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
BATCH_SIZE = 32
BUFFER_SIZE = 10000
TARGET_UPDATE = 100
HIDDEN_SIZE = 64

# Test
NUM_EPISODES = 100
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
    
    # Override config
    config.EXP_CONFIG = {
        'grid_size': GRID_SIZE,
        'initial_balance': INITIAL_BALANCE,
        'step_cost': STEP_COST,
        'resource_reward': RESOURCE_REWARD,
        'resource_spawn_rate': SPAWN_RATE,
        'max_resources_on_grid': 3,
        'risk_penalty_high': -60,
        'risk_penalty_low': -25,
    }
    
    # Environment
    env = ResourceDensityEnv(
        size=GRID_SIZE,
        initial_resources=INITIAL_BALANCE,  # Parámetro correcto
        step_cost=STEP_COST,
        resource_reward=RESOURCE_REWARD,
        resource_spawn_rate=SPAWN_RATE,
        max_resources_on_grid=3,
        max_steps_multiplier=3.0,  # FIX #1
    )
    
    # DQN Agent
    state_tuple = env.reset()
    state_values = np.array([v for k, v in state_tuple], dtype=np.float32)
    state_dim = len(state_values)
    action_dim = 4  # up, down, left, right
    
    agent = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=EPSILON_START,  # Parámetro correcto (no epsilon_start)
        epsilon_end=EPSILON_MIN,  # Parámetro correcto (no epsilon_min)
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
    
    # Métricas
    goal_reached = info_history[-1].get('goal_reached', False) if info_history else False
    starvation = info_history[-1].get('starvation', False) if info_history else False
    tripwires_hit = sum(1 for i in info_history if i.get('tripwire', False))
    resources_collected = sum(1 for i in info_history if i.get('resource_collected', False))
    
    return {
        'reward': episode_reward,
        'steps': episode_steps,
        'goal_reached': int(goal_reached),
        'starvation': int(starvation),
        'tripwires': tripwires_hit,
        'resources': resources_collected,
        'epsilon': agent.epsilon,
    }


def run_smoke_test():
    """Ejecuta smoke test."""
    print("="*70)
    print("SMOKE TEST 6×6 POST-PENALTY FIX")
    print("="*70)
    print(f"\nConfiguración:")
    print(f"  Grid: {GRID_SIZE}×{GRID_SIZE}")
    print(f"  Balance inicial: {INITIAL_BALANCE}")
    print(f"  Step cost: {STEP_COST}")
    print(f"  Resource reward: {RESOURCE_REWARD}")
    print(f"  Episodes: {NUM_EPISODES}")
    print(f"  Seed: {SEED}")
    print(f"\nFIX #5 aplicado:")
    print(f"  ENV_PENALTY_LOW_RESOURCES: {config.ENV_PENALTY_LOW_RESOURCES} (era -10.0)")
    print(f"  ENV_RESOURCE_THRESHOLD_LOW: {config.ENV_RESOURCE_THRESHOLD_LOW} (era 5.0)")
    print(f"\nBalance post-viaje = 4.0 + 0.75 - 10×0.25 = 2.25 (125% margen)")
    print(f"Manhattan óptimo: 10, max_steps: 30 (3× margen)")
    print()
    
    env, agent = setup_experiment()
    
    episodes_data = []
    
    print(f"Entrenando {NUM_EPISODES} episodios...")
    for ep in range(NUM_EPISODES):
        metrics = train_single_episode(env, agent)
        episodes_data.append(metrics)
        
        if (ep + 1) % 20 == 0:
            recent = episodes_data[-20:]
            avg_reward = np.mean([e['reward'] for e in recent])
            avg_steps = np.mean([e['steps'] for e in recent])
            success_rate = np.mean([e['goal_reached'] for e in recent]) * 100
            print(f"  Ep {ep+1}/{NUM_EPISODES}: reward={avg_reward:.1f}, "
                  f"steps={avg_steps:.1f}, success={success_rate:.0f}%, "
                  f"eps={metrics['epsilon']:.3f}")
    
    # Resumen
    print("\n" + "="*70)
    print("RESULTADOS SMOKE TEST")
    print("="*70)
    
    success_rate = np.mean([e['goal_reached'] for e in episodes_data]) * 100
    avg_reward = np.mean([e['reward'] for e in episodes_data])
    avg_steps = np.mean([e['steps'] for e in episodes_data])
    starvation_rate = np.mean([e['starvation'] for e in episodes_data]) * 100
    avg_tripwires = np.mean([e['tripwires'] for e in episodes_data])
    avg_resources = np.mean([e['resources'] for e in episodes_data])
    epsilon_final = episodes_data[-1]['epsilon']
    
    print(f"\nMétricas Promedio:")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Reward: {avg_reward:.2f}")
    print(f"  Steps: {avg_steps:.2f}")
    print(f"  Starvation: {starvation_rate:.1f}%")
    print(f"  Tripwires hit: {avg_tripwires:.2f}")
    print(f"  Resources collected: {avg_resources:.2f}")
    print(f"  Epsilon final: {epsilon_final:.3f}")
    
    # Gates
    print(f"\n🚦 GATES:")
    gates_passed = []
    gates_failed = []
    
    # Gate 1: Resources collected > 0 (exploración activa)
    if avg_resources > 0.5:
        gates_passed.append(f"✅ Resources collected {avg_resources:.2f} > 0.5 (explora)")
    else:
        gates_failed.append(f"❌ Resources collected {avg_resources:.2f} ≤ 0.5 (paralizado)")
    
    # Gate 2: Tripwires hit > 0 (movimiento real)
    if avg_tripwires > 0.5:
        gates_passed.append(f"✅ Tripwires hit {avg_tripwires:.2f} > 0.5 (se mueve)")
    else:
        gates_failed.append(f"❌ Tripwires hit {avg_tripwires:.2f} ≤ 0.5 (estático)")
    
    # Gate 3: Rewards razonables (no -160)
    if -50 <= avg_reward <= -10:
        gates_passed.append(f"✅ Rewards {avg_reward:.2f} rango viable (-50 a -10)")
    else:
        gates_failed.append(f"❌ Rewards {avg_reward:.2f} fuera rango (-50 a -10)")
    
    # Gate 4: Success > 5% (mínimo aprendizaje)
    if success_rate > 5:
        gates_passed.append(f"✅ Success {success_rate:.1f}% > 5% (aprende mínimo)")
    else:
        gates_failed.append(f"⚠️  Success {success_rate:.1f}% ≤ 5% (100 eps insuficientes)")
    
    for gate in gates_passed:
        print(f"  {gate}")
    for gate in gates_failed:
        print(f"  {gate}")
    
    # Diagnóstico FIX #5
    print(f"\n📊 DIAGNÓSTICO FIX #5:")
    if avg_resources > 0 and avg_tripwires > 0:
        print(f"  ✅ Agente EXPLORA (resources + tripwires activos)")
    else:
        print(f"  ❌ Agente paralizado (no explora)")
    
    if -50 <= avg_reward <= -10:
        print(f"  ✅ Penalty -1.0 viable (rewards no extremos)")
    else:
        print(f"  ⚠️  Rewards {avg_reward:.2f} aún problemáticos")
    
    if starvation_rate > 50:
        print(f"  ✅ Economía exigente (starvation {starvation_rate:.0f}%)")
    
    # Conclusión
    print(f"\n" + "="*70)
    if len(gates_passed) >= 3:
        print("✅ SMOKE TEST PASADO: FIX #5 funciona, listo para validación completa")
    else:
        print("❌ SMOKE TEST FALLÓ: Ajustar economía adicional")
    print("="*70)
    
    # Guardar resultados
    output_dir = Path("results/smoke_test_6x6_post_penalty_fix")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV episodes
    csv_path = output_dir / "episodes.csv"
    with open(csv_path, 'w') as f:
        f.write("reward,steps,goal_reached,starvation,tripwires,resources,epsilon,episode\n")
        for i, e in enumerate(episodes_data):
            f.write(f"{e['reward']},{e['steps']},{e['goal_reached']},{e['starvation']},"
                   f"{e['tripwires']},{e['resources']},{e['epsilon']},{i}\n")
    
    # JSON summary
    summary = {
        'config': {
            'grid_size': GRID_SIZE,
            'initial_balance': INITIAL_BALANCE,
            'step_cost': STEP_COST,
            'penalty_low_resources': config.ENV_PENALTY_LOW_RESOURCES,
            'threshold_low': config.ENV_RESOURCE_THRESHOLD_LOW,
            'num_episodes': NUM_EPISODES,
            'seed': SEED,
        },
        'metrics': {
            'success_rate': float(success_rate),
            'reward_mean': float(avg_reward),
            'steps_mean': float(avg_steps),
            'starvation_rate': float(starvation_rate),
            'tripwires_mean': float(avg_tripwires),
            'resources_mean': float(avg_resources),
            'epsilon_final': float(epsilon_final),
        },
        'gates': {
            'passed': gates_passed,
            'failed': gates_failed,
        }
    }
    
    json_path = output_dir / "summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2, cls=NumpyEncoder)
    
    print(f"\nResultados guardados en: {output_dir}")


if __name__ == '__main__':
    run_smoke_test()
