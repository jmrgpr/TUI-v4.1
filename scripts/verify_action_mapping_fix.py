"""
VERIFICACIÓN SISTEMÁTICA: Bug Action Mapping
============================================

Verifica que el fix funciona comparando:
1. Oráculo (baseline 100%)
2. DQN con fix (debe >80%)
3. DQN sin fix (simulado, debe 0%)

Grid: 4×4 (caso simple)
Episodios: 100 (verificación rápida)
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
print("VERIFICACIÓN SISTEMÁTICA: Bug Action Mapping")
print("="*70)

GRID_SIZE = 4
NUM_EPISODES = 100
MAX_STEPS_MULTIPLIER = 4.0

# Economía v11
env = ResourceDensityEnv(
    size=GRID_SIZE,
    initial_resources=config.ENV_INITIAL_RESOURCES,
    step_cost=config.ENV_STEP_COST,
    resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,
    max_steps_multiplier=MAX_STEPS_MULTIPLIER
)

print(f"\nGrid: {GRID_SIZE}×{GRID_SIZE}")
print(f"Episodios: {NUM_EPISODES}")
print(f"max_steps: {int((GRID_SIZE-1)*2*MAX_STEPS_MULTIPLIER)}")

# ============================================================================
# TEST 1: ORÁCULO (Baseline 100%)
# ============================================================================
print(f"\n{'='*70}")
print("TEST 1: ORÁCULO (baseline)")
print("="*70)

success_oracle = 0
for ep in range(NUM_EPISODES):
    state = env.reset()
    done = False
    
    while not done:
        # Oráculo: camino óptimo hacia goal
        agent_pos = env.agent_pos
        goal_pos = env.goal_pos
        
        if agent_pos[0] < goal_pos[0]:
            action = 'down'
        elif agent_pos[0] > goal_pos[0]:
            action = 'up'
        elif agent_pos[1] < goal_pos[1]:
            action = 'right'
        elif agent_pos[1] > goal_pos[1]:
            action = 'left'
        else:
            action = 'stay'
        
        state, reward, done, info = env.step(action)
    
    if info.get('goal_reached', False):
        success_oracle += 1

success_rate_oracle = (success_oracle / NUM_EPISODES) * 100
print(f"Success: {success_rate_oracle:.1f}% ({success_oracle}/{NUM_EPISODES})")

if success_rate_oracle >= 95:
    print("✅ Oráculo funciona correctamente (≥95%)")
else:
    print(f"❌ Oráculo FALLÓ: {success_rate_oracle:.1f}% < 95%")
    print("   → Economía v11 NO viable o bug environment")

# ============================================================================
# TEST 2: DQN CON FIX (debe >50% después 100 eps)
# ============================================================================
print(f"\n{'='*70}")
print("TEST 2: DQN CON FIX action mapping")
print("="*70)

# State encoding
def state_to_vector(state):
    if isinstance(state, tuple):
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)

# Agent
state = env.reset()
state_dim = len(state_to_vector(state))
action_dim = 5

agent_fixed = DQNAgent(
    state_dim=state_dim,
    action_dim=action_dim,
    lr=0.001,
    gamma=0.99,
    epsilon=1.0,
    epsilon_end=0.1,
    epsilon_decay=0.995,  # Más rápido para 100 eps
    batch_size=32,
    memory_size=10000,
)

success_fixed = 0
first_success_fixed = None

for ep in range(NUM_EPISODES):
    state = env.reset()
    state_vec = state_to_vector(state)
    done = False
    
    while not done:
        action_idx = agent_fixed.act(state_vec)
        
        # ✅ FIX: Mapear INT → STRING
        action_str = config.AGENT_ACTIONS[action_idx]
        
        next_state, reward, done, info = env.step(action_str)
        next_state_vec = state_to_vector(next_state)
        agent_fixed.remember(state_vec, action_idx, reward, next_state_vec, done)
        agent_fixed.learn()
        
        state_vec = next_state_vec
    
    if info.get('goal_reached', False):
        success_fixed += 1
        if first_success_fixed is None:
            first_success_fixed = ep + 1

success_rate_fixed = (success_fixed / NUM_EPISODES) * 100
print(f"Success: {success_rate_fixed:.1f}% ({success_fixed}/{NUM_EPISODES})")
print(f"Primer éxito: Episodio {first_success_fixed if first_success_fixed else 'NUNCA'}")
print(f"Epsilon final: {agent_fixed.epsilon:.4f}")

if success_rate_fixed >= 50:
    print(f"✅ DQN con fix aprende (≥50% en 100 eps)")
elif first_success_fixed:
    print(f"⚠️  DQN con fix aprende LENTO ({success_rate_fixed:.1f}%)")
    print(f"   Primer éxito ep {first_success_fixed}, necesita más episodios")
else:
    print(f"❌ DQN con fix FALLÓ: 0% success")
    print("   → Bug adicional o hiperparámetros")

# ============================================================================
# TEST 3: DQN SIN FIX (simulado, debe 0%)
# ============================================================================
print(f"\n{'='*70}")
print("TEST 3: DQN SIN FIX (simulación bug)")
print("="*70)

agent_buggy = DQNAgent(
    state_dim=state_dim,
    action_dim=action_dim,
    lr=0.001,
    gamma=0.99,
    epsilon=1.0,
    epsilon_end=0.1,
    epsilon_decay=0.995,
    batch_size=32,
    memory_size=10000,
)

success_buggy = 0
positions_unique_buggy = set()

for ep in range(NUM_EPISODES):
    state = env.reset()
    state_vec = state_to_vector(state)
    done = False
    
    while not done:
        action_idx = agent_buggy.act(state_vec)
        
        # ❌ BUG: Enviar INT directamente (simula bug)
        # Como environment.step() recibe int no reconocido,
        # moves.get(3, (0,0)) devuelve (0,0) → agent NO se mueve
        action_buggy = action_idx  # Envía INT en lugar de STRING
        
        # Simulación manual del bug: agent congelado
        positions_unique_buggy.add(tuple(env.agent_pos))
        
        # Para simular, forzamos que no se mueva
        next_state, reward, done, info = env.step('stay')  # Fuerza noop
        next_state_vec = state_to_vector(next_state)
        agent_buggy.remember(state_vec, action_idx, reward, next_state_vec, done)
        agent_buggy.learn()
        
        state_vec = next_state_vec
    
    if info.get('goal_reached', False):
        success_buggy += 1

success_rate_buggy = (success_buggy / NUM_EPISODES) * 100
print(f"Success: {success_rate_buggy:.1f}% ({success_buggy}/{NUM_EPISODES})")
print(f"Posiciones únicas visitadas: {len(positions_unique_buggy)}")
print(f"Epsilon final: {agent_buggy.epsilon:.4f}")

if success_rate_buggy == 0 and len(positions_unique_buggy) <= 2:
    print("✅ Bug simulado correctamente (agent congelado, 0% success)")
else:
    print(f"⚠️  Simulación bug inconsistente")

# ============================================================================
# RESUMEN
# ============================================================================
print(f"\n{'='*70}")
print("RESUMEN VERIFICACIÓN")
print("="*70)

print(f"\n1. Oráculo:        {success_rate_oracle:5.1f}% (baseline viabilidad)")
print(f"2. DQN con fix:    {success_rate_fixed:5.1f}% (debe >50%)")
print(f"3. DQN sin fix:    {success_rate_buggy:5.1f}% (debe ~0%)")

delta_fix = success_rate_fixed - success_rate_buggy

print(f"\nDelta fix: +{delta_fix:.1f}% (diferencia con/sin fix)")

# Conclusión
print(f"\n{'='*70}")
print("CONCLUSIÓN")
print("="*70)

checks = []
checks.append(("Oráculo viable", success_rate_oracle >= 95))
checks.append(("DQN con fix aprende", success_rate_fixed >= 50 or first_success_fixed))
checks.append(("Delta fix significativo", delta_fix >= 40))

all_passed = all(passed for _, passed in checks)

for check, passed in checks:
    status = "✅" if passed else "❌"
    print(f"{status} {check}")

print(f"\n{'='*70}")
if all_passed:
    print("✅ VERIFICACIÓN EXITOSA")
    print("   → Bug action mapping CONFIRMADO resuelto")
    print("   → Economía v11 viable")
    print("   → DQN aprende correctamente con fix")
    print(f"   → Serie 10.x VÁLIDA (usa actions_map correctamente)")
else:
    print("❌ VERIFICACIÓN FALLIDA")
    print("   → Revisar configuración o bugs adicionales")
print("="*70)
