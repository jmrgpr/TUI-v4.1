"""
Smoke Test Convergencia 6×6 - 1000 Episodios
=============================================
Test definitivo para validar que DQN PUEDE aprender antes de v10.7.

AJUSTES vs validación 200 eps:
- Episodes: 200 → 1000 (5× más experiencia)
- spawn_rate: 0.15 → 0.30 (2× más resources)
- balance: 4.0 → 5.0 (+25% margen)
- epsilon_decay: 0.995 → 0.9995 (más lento, mejor exploración)

Gates CRÍTICOS:
- Success rate: >5% (mínimo 50/1000 episodios)
- Resources collected: >1.0 promedio
- Rewards: >-5 últimos 100 eps
- Epsilon final: <0.1 (convergencia policy)
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
# CONFIGURACIÓN SMOKE TEST CONVERGENCIA
# ============================================================================

GRID_SIZE = 6
INITIAL_BALANCE = 5.0  # +25% vs 4.0 (más margen)
STEP_COST = -0.25
RESOURCE_REWARD = 0.75
SPAWN_RATE = 0.30  # 2× vs 0.15 (más resources)

# Balance post-viaje = 5.0 + 0.75 - 10×0.25 = 3.25 (162% margen)
# Manhattan óptimo: 10, max_steps: 30 (3× margen)

# DQN hyperparams
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.9995  # Más lento que 0.995 (mejor exploración)
BATCH_SIZE = 32
BUFFER_SIZE = 20000  # 2× buffer (más memoria)
TARGET_UPDATE = 100
HIDDEN_SIZE = 64

# Test
NUM_EPISODES = 1000  # 5× más que validación
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
        'step_cost': STEP_COST,
        'resource_reward': RESOURCE_REWARD,
        'resource_spawn_rate': SPAWN_RATE,
        'max_resources_on_grid': 3,
        'risk_penalty_high': -60,
        'risk_penalty_low': -25,
    }
    
    env = ResourceDensityEnv(
        size=GRID_SIZE,
        initial_resources=INITIAL_BALANCE,
        step_cost=STEP_COST,
        resource_reward=RESOURCE_REWARD,
        resource_spawn_rate=SPAWN_RATE,
        max_resources_on_grid=3,
        max_steps_multiplier=3.0,
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
    """Ejecuta smoke test convergencia."""
    print("="*70)
    print("SMOKE TEST CONVERGENCIA 6×6 - 1000 EPISODIOS")
    print("="*70)
    print(f"\nConfiguración AJUSTADA:")
    print(f"  Grid: {GRID_SIZE}×{GRID_SIZE}")
    print(f"  Balance: {INITIAL_BALANCE} (+25% vs 4.0)")
    print(f"  Spawn rate: {SPAWN_RATE} (2× vs 0.15)")
    print(f"  Episodes: {NUM_EPISODES} (5× vs 200)")
    print(f"  Epsilon decay: {EPSILON_DECAY} (más lento)")
    print(f"\nBalance post-viaje: 5.0 + 0.75 - 10×0.25 = 3.25 (162% margen)")
    print(f"\nGates CRÍTICOS:")
    print(f"  - Success rate: >5%")
    print(f"  - Resources: >1.0 promedio")
    print(f"  - Rewards últimos 100: >-5")
    print(f"  - Epsilon final: <0.1")
    print()
    
    env, agent = setup_experiment()
    
    episodes_data = []
    
    print(f"Entrenando {NUM_EPISODES} episodios...")
    for ep in range(NUM_EPISODES):
        metrics = train_single_episode(env, agent)
        episodes_data.append(metrics)
        
        if (ep + 1) % 100 == 0:
            recent = episodes_data[-100:]
            avg_reward = np.mean([e['reward'] for e in recent])
            avg_steps = np.mean([e['steps'] for e in recent])
            success_rate = np.mean([e['goal_reached'] for e in recent]) * 100
            resources = np.mean([e['resources'] for e in recent])
            print(f"  Ep {ep+1}/{NUM_EPISODES}: reward={avg_reward:.1f}, "
                  f"steps={avg_steps:.1f}, success={success_rate:.1f}%, "
                  f"resources={resources:.2f}, eps={metrics['epsilon']:.3f}")
    
    # Resumen
    print("\n" + "="*70)
    print("RESULTADOS SMOKE TEST CONVERGENCIA")
    print("="*70)
    
    # Métricas totales
    success_rate = np.mean([e['goal_reached'] for e in episodes_data]) * 100
    avg_reward = np.mean([e['reward'] for e in episodes_data])
    avg_steps = np.mean([e['steps'] for e in episodes_data])
    starvation_rate = np.mean([e['starvation'] for e in episodes_data]) * 100
    avg_tripwires = np.mean([e['tripwires'] for e in episodes_data])
    avg_resources = np.mean([e['resources'] for e in episodes_data])
    epsilon_final = episodes_data[-1]['epsilon']
    
    # Últimos 100 episodios
    last_100 = episodes_data[-100:]
    success_last = np.mean([e['goal_reached'] for e in last_100]) * 100
    reward_last = np.mean([e['reward'] for e in last_100])
    resources_last = np.mean([e['resources'] for e in last_100])
    
    print(f"\nMétricas Totales (1000 eps):")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Reward: {avg_reward:.2f}")
    print(f"  Steps: {avg_steps:.2f}")
    print(f"  Starvation: {starvation_rate:.1f}%")
    print(f"  Tripwires: {avg_tripwires:.2f}")
    print(f"  Resources: {avg_resources:.2f}")
    print(f"  Epsilon final: {epsilon_final:.4f}")
    
    print(f"\nÚltimos 100 Episodios:")
    print(f"  Success rate: {success_last:.1f}%")
    print(f"  Reward: {reward_last:.2f}")
    print(f"  Resources: {resources_last:.2f}")
    
    # Gates CRÍTICOS
    print(f"\n🚦 GATES CONVERGENCIA:")
    gates_passed = []
    gates_failed = []
    
    # Gate 1: Success >5%
    if success_last > 5:
        gates_passed.append(f"✅ Success {success_last:.1f}% > 5% (DQN aprende)")
    else:
        gates_failed.append(f"❌ Success {success_last:.1f}% ≤ 5% (no converge)")
    
    # Gate 2: Resources >1.0
    if resources_last > 1.0:
        gates_passed.append(f"✅ Resources {resources_last:.2f} > 1.0 (recolecta)")
    else:
        gates_failed.append(f"❌ Resources {resources_last:.2f} ≤ 1.0 (no recolecta)")
    
    # Gate 3: Rewards >-5 últimos 100
    if reward_last > -5:
        gates_passed.append(f"✅ Rewards {reward_last:.2f} > -5 (mejora)")
    else:
        gates_failed.append(f"❌ Rewards {reward_last:.2f} ≤ -5 (estancado)")
    
    # Gate 4: Epsilon <0.1
    if epsilon_final < 0.1:
        gates_passed.append(f"✅ Epsilon {epsilon_final:.4f} < 0.1 (policy converge)")
    else:
        gates_failed.append(f"⚠️  Epsilon {epsilon_final:.4f} ≥ 0.1 (aún explorando)")
    
    for gate in gates_passed:
        print(f"  {gate}")
    for gate in gates_failed:
        print(f"  {gate}")
    
    # Conclusión
    print(f"\n" + "="*70)
    if len(gates_passed) >= 3:
        print("✅ CONVERGENCIA CONFIRMADA: DQN aprende, listo para v10.7")
    else:
        print("❌ CONVERGENCIA FALLIDA: Ajustar economía antes de v10.7")
        print("\nSugerencias:")
        if success_last < 5:
            print("  - Aumentar spawn_rate 0.30 → 0.40")
            print("  - Reducir step_cost -0.25 → -0.15")
        if resources_last < 1:
            print("  - Aumentar spawn_rate (más resources)")
            print("  - Aumentar balance inicial")
        if epsilon_final > 0.1:
            print("  - Aumentar episodios 1000 → 2000")
            print("  - Ajustar epsilon_decay")
    print("="*70)
    
    # Guardar resultados
    output_dir = Path("results/smoke_test_convergencia_1000eps")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / "episodes.csv"
    with open(csv_path, 'w') as f:
        f.write("reward,steps,goal_reached,starvation,tripwires,resources,epsilon,episode\n")
        for i, e in enumerate(episodes_data):
            f.write(f"{e['reward']},{e['steps']},{e['goal_reached']},{e['starvation']},"
                   f"{e['tripwires']},{e['resources']},{e['epsilon']},{i}\n")
    
    summary = {
        'config': {
            'grid_size': GRID_SIZE,
            'initial_balance': INITIAL_BALANCE,
            'spawn_rate': SPAWN_RATE,
            'num_episodes': NUM_EPISODES,
            'epsilon_decay': EPSILON_DECAY,
        },
        'metrics_total': {
            'success_rate': float(success_rate),
            'reward_mean': float(avg_reward),
            'resources_mean': float(avg_resources),
        },
        'metrics_last_100': {
            'success_rate': float(success_last),
            'reward_mean': float(reward_last),
            'resources_mean': float(resources_last),
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
    
    print(f"\nResultados: {output_dir}")


if __name__ == '__main__':
    run_smoke_test()
