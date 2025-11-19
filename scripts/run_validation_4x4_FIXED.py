"""
VALIDACIÓN 4×4 POST-FIX: Bug Action Mapping Resuelto
====================================================

BUG CRÍTICO RESUELTO:
- DQNAgent.act() devuelve INTEGER (0-4)
- environment.step() espera STRING ("up", "down", etc)
- Sin conversión: agent congelado en spawn, 0% success

FIX IMPLEMENTADO:
action_idx = agent.act(state_vec)  # 0-4
action_str = config.AGENT_ACTIONS[action_idx]  # 0→'up', 1→'down', etc
next_state, reward, done, info = env.step(action_str)

OBJETIVO:
Validar que con fix, DQN alcanza >80% success en grid 4×4 (500 eps)
con economía v11 viable (balance 8.0, step_cost -0.15, etc)
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

print("="*70)
print("VALIDACIÓN 4×4 POST-FIX: Bug Action Mapping Resuelto")
print("="*70)

# Configuración
GRID_SIZE = 4
NUM_EPISODES = 500
MAX_STEPS_MULTIPLIER = 4.0  # Holgura 300%

# Economía v11 viable
INITIAL_RESOURCES = config.ENV_INITIAL_RESOURCES  # 8.0
STEP_COST = config.ENV_STEP_COST  # -0.15
RESOURCE_SPAWN_RATE = config.ENV_RESOURCE_SPAWN_RATE  # 0.40

# Hiperparámetros DQN
EPSILON_START = 1.0
EPSILON_DECAY = 0.999  # Exploración lenta
EPSILON_MIN = 0.1  # Nunca deja explorar 10%
LEARNING_RATE = 0.001
GAMMA = 0.99

print(f"\nGrid: {GRID_SIZE}×{GRID_SIZE}")
print(f"Episodios: {NUM_EPISODES}")
print(f"max_steps_multiplier: {MAX_STEPS_MULTIPLIER}× (Manhattan × {MAX_STEPS_MULTIPLIER})")
print(f"\nEconomía v11:")
print(f"  initial_resources: {INITIAL_RESOURCES}")
print(f"  step_cost: {STEP_COST}")
print(f"  spawn_rate: {RESOURCE_SPAWN_RATE}")
print(f"\nHiperparámetros:")
print(f"  epsilon_start: {EPSILON_START}")
print(f"  epsilon_decay: {EPSILON_DECAY}")
print(f"  epsilon_min: {EPSILON_MIN}")
print(f"  learning_rate: {LEARNING_RATE}")
print(f"  gamma: {GAMMA}")

# Environment
env = ResourceDensityEnv(
    size=GRID_SIZE,
    initial_resources=INITIAL_RESOURCES,
    step_cost=STEP_COST,
    resource_spawn_rate=RESOURCE_SPAWN_RATE,
    max_steps_multiplier=MAX_STEPS_MULTIPLIER
)

# State vector
def state_to_vector(state):
    """Convierte tuple state a vector flat para DQN"""
    if isinstance(state, tuple):
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)

# Agent
state = env.reset()
state_dim = len(state_to_vector(state))
action_dim = 5  # up, down, left, right, noop

agent = DQNAgent(
    state_dim=state_dim,
    action_dim=action_dim,
    lr=LEARNING_RATE,
    gamma=GAMMA,
    epsilon=EPSILON_START,
    epsilon_end=EPSILON_MIN,
    epsilon_decay=EPSILON_DECAY,
    batch_size=32,
    memory_size=10000,
)

# Métricas
metrics = {
    "success": [],
    "rewards": [],
    "steps": [],
    "resources": [],
    "epsilon": [],
    "goal_reached_episodes": [],
}

print(f"\n{'='*70}")
print(f"ENTRENAMIENTO")
print(f"{'='*70}\n")

# Training loop con FIX action mapping
for ep in range(NUM_EPISODES):
    state = env.reset()
    state_vec = state_to_vector(state)
    done = False
    total_reward = 0
    steps = 0
    
    while not done:
        action_idx = agent.act(state_vec)  # Devuelve 0-4
        
        # ✅ FIX: Mapear índice a string action
        action_str = config.AGENT_ACTIONS[action_idx]  # 0→'up', 1→'down', etc
        
        next_state, reward, done, info = env.step(action_str)
        next_state_vec = state_to_vector(next_state)
        agent.remember(state_vec, action_idx, reward, next_state_vec, done)
        agent.learn()
        
        state = next_state
        state_vec = next_state_vec
        total_reward += reward
        steps += 1
    
    # Registrar métricas
    success = 1 if info.get('goal_reached', False) else 0
    metrics["success"].append(success)
    metrics["rewards"].append(total_reward)
    metrics["steps"].append(steps)
    metrics["resources"].append(env.total_resources_collected)
    metrics["epsilon"].append(agent.epsilon)
    
    if success:
        metrics["goal_reached_episodes"].append(ep + 1)
    
    # Progress cada 50 eps
    if (ep + 1) % 50 == 0:
        recent_success = np.mean(metrics["success"][-50:]) * 100
        recent_reward = np.mean(metrics["rewards"][-50:])
        recent_resources = np.mean(metrics["resources"][-50:])
        recent_steps = np.mean(metrics["steps"][-50:])
        
        print(f"Ep {ep+1:3d}: success={recent_success:5.1f}%, "
              f"reward={recent_reward:+7.2f}, "
              f"resources={recent_resources:.2f}, "
              f"steps={recent_steps:.1f}, "
              f"ε={agent.epsilon:.4f}")

# Resultados finales
print(f"\n{'='*70}")
print(f"RESULTADOS FINALES")
print(f"{'='*70}\n")

total_success = np.sum(metrics["success"])
success_rate = (total_success / NUM_EPISODES) * 100

print(f"Success total: {success_rate:.1f}% ({total_success}/{NUM_EPISODES})")
print(f"Epsilon final: {agent.epsilon:.4f}")

if metrics["goal_reached_episodes"]:
    print(f"Primer éxito: Episodio {metrics['goal_reached_episodes'][0]}")
else:
    print(f"Primer éxito: NUNCA")

# Últimos 100 eps
last_100_success = np.mean(metrics["success"][-100:]) * 100
last_100_reward = np.mean(metrics["rewards"][-100:])
last_100_resources = np.mean(metrics["resources"][-100:])
last_100_steps = np.mean(metrics["steps"][-100:])

print(f"\nÚltimos 100 eps:")
print(f"  Success: {last_100_success:.1f}%")
print(f"  Reward: {last_100_reward:+.2f}")
print(f"  Resources: {last_100_resources:.2f}")
print(f"  Steps: {last_100_steps:.1f} / {env.max_steps}")

# Gate
GATE_THRESHOLD = 80.0
print(f"\n{'='*70}")
print(f"GATE VALIDACIÓN")
print(f"{'='*70}")

if last_100_success >= GATE_THRESHOLD:
    print(f"✅ GATE PASADO: Success {last_100_success:.1f}% ≥ {GATE_THRESHOLD}%")
    print(f"   → DQN aprende correctamente con economía v11")
    print(f"   → Bug action mapping RESUELTO")
    print(f"   → Proceder: Fase 2 (6×6 con transfer learning)")
else:
    print(f"❌ GATE FALLIDO: Success {last_100_success:.1f}% < {GATE_THRESHOLD}%")
    print(f"   → Bug adicional o tuning necesario")

# Guardar resultados
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = ROOT / "results"
output_dir.mkdir(exist_ok=True)

df = pd.DataFrame(metrics)
output_file = output_dir / f"validation_4x4_fixed_{timestamp}.csv"
df.to_csv(output_file, index=False)

print(f"\nResultados guardados: {output_file.relative_to(ROOT)}")
print("="*70)
