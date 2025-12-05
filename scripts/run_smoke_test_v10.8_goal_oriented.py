"""
Smoke Test v10.8 Goal-Oriented - 1000 Episodios
================================================
Test definitivo economía goal-seeking con 3 ajustes críticos.

CAMBIOS vs smoke test convergencia (v10.7):
1. goal_reward: 0.0 → 10.0 (recompensa explícita meta)
2. spawn_rate: 0.30 → 0.40 (+33% resources)
3. step_cost: -0.25 → -0.15 (-40% castigo)

IMPACTO TEÓRICO:
- Episode óptimo: +10.0 (goal) + 0.75 (resource) - 1.5 (steps) = +9.25 ✅ POSITIVO
- Episode subóptimo: +0.75 (resource) - 3.3 (steps) - 3.0 (penalty) = -5.55 ❌
- Delta: 9.25 - (-5.55) = +14.8 (señal DOMINANTE alcanzar meta)

Gates CRÍTICOS v10.8:
- Success rate: >10% (100+ episodios alcanza meta)
- Rewards últimos 100: >0 (promedio positivo)
- Resources: >1.5 promedio (spawn_rate 0.40)
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
# CONFIGURACIÓN SMOKE TEST v10.8
# ============================================================================

GRID_SIZE = 6
INITIAL_BALANCE = 5.0
# v10.8: Economía goal-oriented (config.py actualizado)
# - goal_reward: 10.0 (NUEVO)
# - step_cost: -0.15 (era -0.25)
# - spawn_rate: 0.40 (era 0.30)
RESOURCE_REWARD = 0.75

# DQN hyperparams (mantener smoke test previo)
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.9995  # Convergencia lenta (mejor exploración)
BATCH_SIZE = 32
BUFFER_SIZE = 20000
TARGET_UPDATE = 100
HIDDEN_SIZE = 64

# Test
NUM_EPISODES = 1000
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
    
    # v10.8: Config usa parámetros actualizados (goal_reward, step_cost, spawn_rate)
    config.EXP_CONFIG = {
        'grid_size': GRID_SIZE,
        'initial_balance': INITIAL_BALANCE,
        'step_cost': config.ENV_STEP_COST,  # -0.15 (config.py)
        'resource_reward': RESOURCE_REWARD,
        'resource_spawn_rate': config.ENV_RESOURCE_SPAWN_RATE,  # 0.40 (config.py)
        'max_resources_on_grid': 3,
        'risk_penalty_high': -60,
        'risk_penalty_low': -25,
    }
    
    env = ResourceDensityEnv(
        size=GRID_SIZE,
        initial_resources=INITIAL_BALANCE,
        step_cost=config.ENV_STEP_COST,  # -0.15
        resource_reward=RESOURCE_REWARD,
        resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,  # 0.40
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
    """Ejecuta smoke test v10.8."""
    print("="*70)
    print("SMOKE TEST v10.8 GOAL-ORIENTED - 1000 EPISODIOS")
    print("="*70)
    print(f"\nConfiguración v10.8:")
    print(f"  Grid: {GRID_SIZE}×{GRID_SIZE}")
    print(f"  Balance: {INITIAL_BALANCE}")
    print(f"  goal_reward: {config.ENV_GOAL_REWARD} (NUEVO)")
    print(f"  step_cost: {config.ENV_STEP_COST} (era -0.25, -40%)")
    print(f"  spawn_rate: {config.ENV_RESOURCE_SPAWN_RATE} (era 0.30, +33%)")
    print(f"  Episodes: {NUM_EPISODES}")
    print(f"  Epsilon decay: {EPSILON_DECAY}")
    print(f"\nImpacto teórico:")
    print(f"  Episode óptimo: +10.0 (goal) + 0.75 (res) - 1.5 (steps) = +9.25 ✅")
    print(f"  Episode subóptimo: +0.75 (res) - 3.3 (steps) - 3.0 (pen) = -5.55 ❌")
    print(f"  Delta: +14.8 (señal DOMINANTE)")
    print(f"\nGates v10.8:")
    print(f"  - Success rate: >10%")
    print(f"  - Rewards últimos 100: >0")
    print(f"  - Resources: >1.5 promedio")
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
            goal_rewards = sum([e['goal_reward_applied'] for e in recent])
            print(f"  Ep {ep+1}/{NUM_EPISODES}: reward={avg_reward:.1f}, "
                  f"steps={avg_steps:.1f}, success={success_rate:.1f}%, "
                  f"resources={resources:.2f}, goal_rewards={goal_rewards}, eps={metrics['epsilon']:.3f}")
    
    # Resumen
    print("\n" + "="*70)
    print("RESULTADOS SMOKE TEST v10.8")
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
    goal_rewards_last = sum([e['goal_reward_applied'] for e in last_100])
    
    print(f"\nMétricas Totales (1000 eps):")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Goal rewards aplicados: {goal_rewards_total}")
    print(f"  Reward: {avg_reward:.2f}")
    print(f"  Steps: {avg_steps:.2f}")
    print(f"  Starvation: {starvation_rate:.1f}%")
    print(f"  Tripwires: {avg_tripwires:.2f}")
    print(f"  Resources: {avg_resources:.2f}")
    print(f"  Epsilon final: {epsilon_final:.4f}")
    
    print(f"\nÚltimos 100 Episodios:")
    print(f"  Success rate: {success_last:.1f}%")
    print(f"  Goal rewards: {goal_rewards_last}")
    print(f"  Reward: {reward_last:.2f}")
    print(f"  Resources: {resources_last:.2f}")
    
    # Comparación vs v10.7
    print(f"\n📊 COMPARACIÓN vs v10.7 (smoke test convergencia):")
    print(f"  Success: 0.0% → {success_last:.1f}% (delta +{success_last:.1f}pp)")
    print(f"  Rewards: -11.85 → {reward_last:.2f} (delta {reward_last - (-11.85):+.2f})")
    print(f"  Resources: 0.98 → {resources_last:.2f} (delta {resources_last - 0.98:+.2f})")
    
    # Gates v10.8
    print(f"\n🚦 GATES v10.8:")
    gates_passed = []
    gates_failed = []
    
    # Gate 1: Success >10%
    if success_last > 10:
        gates_passed.append(f"✅ Success {success_last:.1f}% > 10% (aprende meta)")
    else:
        gates_failed.append(f"❌ Success {success_last:.1f}% ≤ 10% (aún no converge)")
    
    # Gate 2: Rewards >0 últimos 100
    if reward_last > 0:
        gates_passed.append(f"✅ Rewards {reward_last:.2f} > 0 (positivo)")
    else:
        gates_failed.append(f"⚠️  Rewards {reward_last:.2f} ≤ 0 (aún negativo)")
    
    # Gate 3: Resources >1.5
    if resources_last > 1.5:
        gates_passed.append(f"✅ Resources {resources_last:.2f} > 1.5 (recolecta)")
    else:
        gates_failed.append(f"⚠️  Resources {resources_last:.2f} ≤ 1.5 (marginal)")
    
    # Gate 4: Epsilon <0.1
    if epsilon_final < 0.1:
        gates_passed.append(f"✅ Epsilon {epsilon_final:.4f} < 0.1 (converge)")
    else:
        gates_failed.append(f"⚠️  Epsilon {epsilon_final:.4f} ≥ 0.1 (explorando)")
    
    for gate in gates_passed:
        print(f"  {gate}")
    for gate in gates_failed:
        print(f"  {gate}")
    
    # Conclusión
    print(f"\n" + "="*70)
    if len(gates_passed) >= 3:
        print("✅ v10.8 VALIDADO: Goal-seeking funciona, listo para multi-grid")
        print("\nPróximos pasos:")
        print("  1. Validar 8×8 y 16×16 con misma economía")
        print("  2. Documentar v10.8 como economía goal-oriented")
        print("  3. Planificar v11 (multi-grid experiments)")
    else:
        print("⚠️  v10.8 MEJORA PARCIAL: Ajustar economía iterativamente")
        print("\nSugerencias:")
        if success_last < 10:
            print("  - Aumentar goal_reward 10.0 → 15.0")
            print("  - Reducir step_cost -0.15 → -0.10")
        if resources_last < 1.5:
            print("  - Aumentar spawn_rate 0.40 → 0.50")
            print("  - Aumentar balance inicial 5.0 → 6.0")
        if reward_last < 0:
            print("  - Verificar balance goal_reward vs penalties")
            print("  - Aumentar episodes 1000 → 2000")
    print("="*70)
    
    # Guardar resultados
    output_dir = Path("results/smoke_test_v10.8_goal_oriented")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / "episodes.csv"
    with open(csv_path, 'w') as f:
        f.write("reward,steps,goal_reached,starvation,tripwires,resources,goal_reward_applied,epsilon,episode\n")
        for i, e in enumerate(episodes_data):
            f.write(f"{e['reward']},{e['steps']},{e['goal_reached']},{e['starvation']},"
                   f"{e['tripwires']},{e['resources']},{e['goal_reward_applied']},{e['epsilon']},{i}\n")
    
    summary = {
        'version': 'v10.8',
        'config': {
            'grid_size': GRID_SIZE,
            'initial_balance': INITIAL_BALANCE,
            'goal_reward': float(config.ENV_GOAL_REWARD),
            'step_cost': float(config.ENV_STEP_COST),
            'spawn_rate': float(config.ENV_RESOURCE_SPAWN_RATE),
            'num_episodes': NUM_EPISODES,
            'epsilon_decay': EPSILON_DECAY,
        },
        'metrics_total': {
            'success_rate': float(success_rate),
            'reward_mean': float(avg_reward),
            'resources_mean': float(avg_resources),
            'goal_rewards_applied': int(goal_rewards_total),
        },
        'metrics_last_100': {
            'success_rate': float(success_last),
            'reward_mean': float(reward_last),
            'resources_mean': float(resources_last),
            'goal_rewards_applied': int(goal_rewards_last),
            'epsilon_final': float(epsilon_final),
        },
        'comparison_v10_7': {
            'success_delta': float(success_last - 0.0),
            'reward_delta': float(reward_last - (-11.85)),
            'resources_delta': float(resources_last - 0.98),
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
