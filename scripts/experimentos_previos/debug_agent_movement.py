"""
Debug: Verificar si agent se mueve correctamente en curriculum 4x4
============================================================================
Problema: 0% success con max_steps=24 (holgura 300%)
         Reward -27.60 constante, resources 0.00, steps 24.0 exacto

Hipótesis:
1. Agent NO se mueve (acciones inválidas)
2. Agent se mueve pero NO recolecta recursos
3. Goal detection roto en ResourceDensityEnv
4. State encoding incorrecto (DQN ciego)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from sim.environment_v2 import ResourceDensityEnv
from sim import config

print("=" * 70)
print("TEST MOVIMIENTO AGENT EN 4x4")
print("=" * 70)

# Config economía v11
env = ResourceDensityEnv(
    size=4,
    initial_resources=config.ENV_INITIAL_RESOURCES,
    step_cost=config.ENV_STEP_COST,
    resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,
    max_steps_multiplier=4.0  # 24 steps para 4x4
)

print(f"\nGrid: {env.size}x{env.size}")
print(f"max_steps: {env.max_steps}")
print(f"initial_resources: {env.initial_resources}")
print(f"step_cost: {env.step_cost}")
print(f"resource_spawn_rate: {env.resource_spawn_rate}")

# Reset
state = env.reset()
print(f"\nState inicial:")
print(f"  agent_pos: {env.agent_pos}")
print(f"  goal_pos: {env.goal_pos}")
print(f"  resources: {env.resources:.2f}")
print(f"  Manhattan distance: {abs(env.agent_pos[0] - env.goal_pos[0]) + abs(env.agent_pos[1] - env.goal_pos[1])}")

# Test 1: Mover hacia abajo
print(f"\n{'=' * 70}")
print("TEST 1: Secuencia movimientos hacia goal")
print("=" * 70)

actions_sequence = [3, 1, 3, 1, 3, 1]  # Down, Right alternado hacia (3,3) desde (0,0)
total_reward = 0
step_count = 0

for i, action in enumerate(actions_sequence):
    action_name = ['Stay', 'Right', 'Up', 'Down', 'Left'][action]
    pos_before = env.agent_pos
    resources_before = env.resources
    
    state, reward, done, info = env.step(action)
    total_reward += reward
    step_count += 1
    
    pos_after = env.agent_pos
    resources_after = env.resources
    
    print(f"Step {step_count}: {action_name}")
    print(f"  Pos: {pos_before} → {pos_after} (moved: {pos_before != pos_after})")
    print(f"  Resources: {resources_before:.2f} → {resources_after:.2f}")
    print(f"  Reward: {reward:.2f}, Total: {total_reward:.2f}")
    print(f"  Done: {done}, Info: {info}")
    
    if done:
        print(f"\n  ⚠️ Episodio terminó en step {step_count}")
        if info.get('starvation'):
            print(f"     Razón: STARVATION")
        if info.get('success'):
            print(f"     Razón: SUCCESS (alcanzó goal)")
        if env.current_step >= env.max_steps:
            print(f"     Razón: TIMEOUT (max_steps {env.max_steps})")
        break

# Test 2: Random walk largo
print(f"\n{'=' * 70}")
print("TEST 2: Random walk 24 steps")
print("=" * 70)

env.reset()
print(f"Start: agent={env.agent_pos}, goal={env.goal_pos}")

total_reward = 0
positions_visited = [env.agent_pos]
resources_collected = 0

for step in range(24):
    action = np.random.randint(0, 5)
    action_name = ['Stay', 'Right', 'Up', 'Down', 'Left'][action]
    resources_before = env.resources
    
    state, reward, done, info = env.step(action)
    total_reward += reward
    positions_visited.append(env.agent_pos)
    
    if env.resources > resources_before:
        resources_collected += 1
    
    if (step + 1) % 6 == 0 or done:
        print(f"Step {step+1}: pos={env.agent_pos}, resources={env.resources:.2f}, reward={reward:.2f}")
    
    if done:
        print(f"\nDone en step {step+1}: {info}")
        break

print(f"\nResultado random walk:")
print(f"  Total reward: {total_reward:.2f}")
print(f"  Posiciones únicas: {len(set(positions_visited))}")
print(f"  Veces recolectó recursos: {resources_collected}")
print(f"  Success: {info.get('success', False)}")

# Test 3: Camino óptimo directo
print(f"\n{'=' * 70}")
print("TEST 3: Camino óptimo (0,0) → (3,3)")
print("=" * 70)

env.reset()
# Forzar posiciones conocidas
env.agent_pos = (0, 0)
env.goal_pos = (3, 3)
print(f"Forzado: agent=(0,0), goal=(3,3)")
print(f"Manhattan: 6 pasos")

# Camino: Down x3, Right x3
optimal_path = [3, 3, 3, 1, 1, 1]  # Down x3, Right x3
total_reward = 0

for i, action in enumerate(optimal_path):
    action_name = ['Stay', 'Right', 'Up', 'Down', 'Left'][action]
    pos_before = env.agent_pos
    
    state, reward, done, info = env.step(action)
    total_reward += reward
    
    print(f"Step {i+1}: {action_name}, pos={pos_before}→{env.agent_pos}, reward={reward:.2f}")
    
    if done:
        print(f"\n✅ Alcanzó goal! Total reward: {total_reward:.2f}")
        print(f"   Info: {info}")
        break

if not done:
    print(f"\n❌ NO alcanzó goal después 6 steps óptimos")
    print(f"   Pos final: {env.agent_pos}, Goal: {env.goal_pos}")
    print(f"   Total reward: {total_reward:.2f}")

print("\n" + "=" * 70)
