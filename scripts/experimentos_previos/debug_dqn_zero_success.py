"""
DEBUG: Diagnóstico sistemático DQN - ¿Por qué 0% success?
==========================================================

Hipótesis:
1. DQNAgent.act() no selecciona acciones válidas
2. Action mapping incorrecto (índice → acción)
3. State encoding genera vectores inválidos
4. Agent no se mueve (reward -25.80 constante sugiere timeout sin movimiento)

Test: 10 episodios con logging detallado de CADA paso
"""

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
from sim import config

print("="*70)
print("DEBUG DQN: Diagnóstico 0% Success")
print("="*70)

def state_to_vector(state):
    """Convertir estado abstracto a vector numérico"""
    if isinstance(state, tuple):
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)

# Environment 4×4 simple
env = ResourceDensityEnv(
    size=4,
    initial_resources=8.0,
    step_cost=-0.15,
    resource_reward=0.75,
    resource_spawn_rate=0.40,
    max_steps_multiplier=2.0,
)

print(f"\nEnvironment 4×4:")
print(f"  goal_pos: {env.goal_pos}")
print(f"  max_steps: {env.max_steps}")
print(f"  agent_pos inicial: {env.agent_pos}")

# DQN Agent
state = env.reset()
state_vec = state_to_vector(state)
state_size = len(state_vec)
action_size = 5

print(f"\nDQN Agent:")
print(f"  state_size: {state_size}")
print(f"  action_size: {action_size}")
print(f"  state_vec ejemplo: {state_vec}")

agent = DQNAgent(
    state_dim=state_size,
    action_dim=action_size,
    lr=1e-3,
    gamma=0.95,
    epsilon=1.0,  # 100% random
    epsilon_decay=0.999,
    epsilon_end=0.1,
    batch_size=32,
    memory_size=10000,
)

# Test 1: Verificar action mapping
print(f"\n{'='*70}")
print(f"TEST 1: Action Mapping")
print(f"{'='*70}")

# Verificar qué acciones devuelve agent.act() con epsilon=1.0 (random)
print(f"\nEpsilon=1.0 (100% random), 20 samples:")
actions_sampled = []
for _ in range(20):
    action = agent.act(state_vec)
    actions_sampled.append(action)

print(f"Acciones devueltas: {actions_sampled}")
print(f"Unique actions: {set(actions_sampled)}")
print(f"Action counts: {[(a, actions_sampled.count(a)) for a in set(actions_sampled)]}")

if len(set(actions_sampled)) == 1:
    print(f"⚠️  WARNING: Agent SIEMPRE devuelve acción {actions_sampled[0]}")
    print(f"   Bug probable: act() no usa epsilon correctamente")

# Test 2: Verificar environment.step() con cada acción
print(f"\n{'='*70}")
print(f"TEST 2: Environment Step con cada acción")
print(f"{'='*70}")

ACTION_NAMES = {0: 'up', 1: 'down', 2: 'left', 3: 'right', 4: 'noop'}

for action_idx in range(5):
    env.reset()
    pos_before = tuple(env.agent_pos)
    
    # Convertir índice a string acción
    action_name = ACTION_NAMES.get(action_idx, f"action_{action_idx}")
    
    _, reward, done, info = env.step(action_name)
    pos_after = tuple(env.agent_pos)
    
    moved = pos_before != pos_after
    print(f"Action {action_idx} ({action_name}): "
          f"{pos_before} → {pos_after} | "
          f"moved={moved}, reward={reward:+.2f}, done={done}")

# Test 3: Episodio completo con logging detallado
print(f"\n{'='*70}")
print(f"TEST 3: Episodio Completo Detallado (epsilon=1.0 random)")
print(f"{'='*70}")

state = env.reset()
state_vec = state_to_vector(state)
print(f"\nEpisodio start:")
print(f"  agent_pos: {env.agent_pos}")
print(f"  goal_pos: {env.goal_pos}")
print(f"  resources: {env.resources:.2f}")
print(f"  state_vec: {state_vec}")

done = False
total_reward = 0
step = 0

while not done and step < 15:  # Max 15 steps para debug
    action_idx = agent.act(state_vec)
    action_name = ACTION_NAMES.get(action_idx, f"action_{action_idx}")
    
    pos_before = tuple(env.agent_pos)
    resources_before = env.resources
    
    try:
        next_state, reward, done, info = env.step(action_name)
    except Exception as e:
        print(f"\n❌ ERROR en step: {e}")
        print(f"   action_idx: {action_idx}")
        print(f"   action_name: {action_name}")
        break
    
    pos_after = tuple(env.agent_pos)
    resources_after = env.resources
    next_state_vec = state_to_vector(next_state)
    
    moved = pos_before != pos_after
    goal_reached = info.get('goal_reached', False)
    
    step += 1
    total_reward += reward
    
    print(f"\nStep {step}: action={action_idx} ({action_name})")
    print(f"  pos: {pos_before} → {pos_after} (moved={moved})")
    print(f"  resources: {resources_before:.2f} → {resources_after:.2f}")
    print(f"  reward: {reward:+.2f}, total: {total_reward:+.2f}")
    print(f"  done: {done}, goal_reached: {goal_reached}")
    
    if goal_reached:
        print(f"  ✅ META ALCANZADA!")
        break
    
    if done:
        death_reason = info.get('death_reason', 'unknown')
        starvation = info.get('starvation', False)
        print(f"  ❌ Episode terminó: {death_reason}, starvation={starvation}")
    
    state = next_state
    state_vec = next_state_vec

# Test 4: Verificar conversión action_idx → action_name
print(f"\n{'='*70}")
print(f"TEST 4: Verificar Action Mapping en Environment")
print(f"{'='*70}")

# Revisar config.AGENT_ACTIONS
if hasattr(config, 'AGENT_ACTIONS'):
    print(f"\nconfig.AGENT_ACTIONS: {config.AGENT_ACTIONS}")
else:
    print(f"\n⚠️  config.AGENT_ACTIONS NO existe")

# Revisar environment actions
if hasattr(env, 'actions'):
    print(f"env.actions: {env.actions}")
else:
    print(f"⚠️  env.actions NO existe")

# Test 5: Verificar si DQNAgent.act() usa índices correctos
print(f"\n{'='*70}")
print(f"TEST 5: Verificar DQNAgent.act() internals")
print(f"{'='*70}")

import torch

# Forzar epsilon=0 (exploit) y ver qué predice la red
agent.epsilon = 0.0
print(f"\nCon epsilon=0 (100% exploit):")

state_tensor = torch.FloatTensor(state_vec).unsqueeze(0)
with torch.no_grad():
    q_values = agent.q_network(state_tensor)
    action = q_values.argmax(1).item()

print(f"  Q-values: {q_values.numpy()}")
print(f"  Acción seleccionada: {action}")
print(f"  Max Q-value: {q_values.max().item():.4f}")

# Restaurar epsilon
agent.epsilon = 1.0

# VEREDICTO
print(f"\n{'='*70}")
print(f"VEREDICTO")
print(f"{'='*70}")

print(f"\nSi agent SIEMPRE devuelve misma acción:")
print(f"  → Bug en DQNAgent.act() (no usa epsilon o action_dim)")
print(f"\nSi agent NO se mueve:")
print(f"  → Bug en action mapping (índice → string)")
print(f"  → Environment espera string PERO DQN devuelve índice")
print(f"\nSi agent se mueve PERO reward constante:")
print(f"  → Bug en reward calculation o timeout prematuro")
print(f"\nSi agent se mueve BIEN:")
print(f"  → Bug en learning (no propaga gradientes)")
