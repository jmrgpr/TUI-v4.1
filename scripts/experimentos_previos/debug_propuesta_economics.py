"""
DEBUG: Verificar si propuesta se aplica correctamente en environment.
Simula 1 episodio con logging detallado.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv

# Config PROPUESTA
initial_resources = 8.0
step_cost = -0.15
resource_reward = 0.75
spawn_rate = 0.40
max_steps_mult = 3.0

print("="*70)
print("DEBUG: Simulación 1 episodio 6×6 con config PROPUESTA")
print("="*70)
print(f"initial_resources: {initial_resources}")
print(f"step_cost: {step_cost}")
print(f"resource_reward: {resource_reward}")
print(f"spawn_rate: {spawn_rate}")
print(f"max_steps_multiplier: {max_steps_mult}\n")

env = ResourceDensityEnv(
    size=6,
    initial_resources=initial_resources,
    step_cost=step_cost,
    resource_reward=resource_reward,
    resource_spawn_rate=spawn_rate,
    max_steps_multiplier=max_steps_mult,
)

print(f"Environment creado:")
print(f"  size: {env.size}")
print(f"  initial_resources (real): {env.initial_resources}")
print(f"  step_cost (real): {env.step_cost}")
print(f"  resource_reward (real): {env.resource_reward}")
print(f"  resource_spawn_rate (real): {env.resource_spawn_rate}")
print(f"  max_steps: {env.max_steps}")
print(f"  goal_pos: {env.goal_pos}\n")

# Simular path Manhattan
path = ["right"] * 5 + ["down"] * 5  # 6×6: (0,0) → (0,5) → (5,5)

state = env.reset()
print(f"Reset: agent_pos={env.agent_pos}, resources={env.resources:.2f}, resources_on_grid={len(env.resource_positions)}\n")

done = False
step = 0
total_reward = 0

while not done and step < env.max_steps:
    action = path[step] if step < len(path) else "right"
    
    # Estado pre-step
    resources_before = env.resources
    pos_before = tuple(env.agent_pos)
    had_resource = pos_before in env.resource_positions if step > 0 else False
    
    _, reward, done, info = env.step(action)
    total_reward += reward
    step += 1
    
    # Estado post-step
    resources_after = env.resources
    pos_after = tuple(env.agent_pos)
    collected = info.get('resource_collected', False)
    goal_reached = info.get('goal_reached', False)
    starvation = info.get('starvation', False)
    
    delta_resources = resources_after - resources_before
    
    print(f"Step {step}: {action:6s} | pos {pos_after} | resources {resources_before:.2f}→{resources_after:.2f} (Δ{delta_resources:+.2f}) | reward {reward:+.2f} | collected={collected} | done={done}")
    
    if goal_reached:
        print(f"  ✅ META ALCANZADA!")
        break
    if starvation:
        print(f"  ❌ STARVATION (resources={resources_after:.2f})")
        break
    if done:
        print(f"  ⚠️  done=True (reason={info.get('death_reason', 'unknown')})")

print(f"\n{'='*70}")
print(f"RESULTADO:")
print(f"  Success: {'SÍ' if info.get('goal_reached') else 'NO'}")
print(f"  Steps: {step}")
print(f"  Total reward: {total_reward:.2f}")
print(f"  Resources finales: {env.resources:.2f}")
print(f"  Starvation: {'SÍ' if info.get('starvation') else 'NO'}")
print(f"  Collected: {env.total_resources_collected}")
print(f"  Spawned: {env.total_resources_spawned}")
print("="*70)

# Verificación matemática
expected_cost = step * abs(step_cost)
expected_gain = env.total_resources_collected * resource_reward
net_change = -expected_cost + expected_gain
predicted_balance = initial_resources + net_change

print(f"\nVERIFICACIÓN MATEMÁTICA:")
print(f"  Initial: {initial_resources:.2f}")
print(f"  Cost ({step} steps × {abs(step_cost)}): -{expected_cost:.2f}")
print(f"  Gain ({env.total_resources_collected} resources × {resource_reward}): +{expected_gain:.2f}")
print(f"  Predicho final: {predicted_balance:.2f}")
print(f"  Real final: {env.resources:.2f}")
print(f"  Match: {'✅' if abs(predicted_balance - env.resources) < 0.01 else '❌'}")
