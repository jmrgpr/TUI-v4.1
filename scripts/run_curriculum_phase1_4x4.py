"""
CURRICULUM LEARNING - FASE 1: Grid 4×4 "Hello World"
=====================================================

Objetivo: Validar que DQN PUEDE aprender con economía v11 viable.
Si falla aquí, hay bug implementación. Si funciona, v10.x era problema exploración.

Config v11 (VIABLE validada por oráculo):
- Balance inicial: 8.0 (autonomía 53 pasos)
- step_cost: -0.15
- penalty_low: -0.5
- threshold_low: 1.0
- goal_reward: 20.0
- spawn_rate: 0.40
- max_steps: 2× Manhattan

Grid 4×4:
- Estados: 16 (vs 36 en 6×6)
- Manhattan: 6 pasos
- max_steps: 12 pasos
- Probabilidad random: ~6.25% (vs ~2.8% en 6×6)

AJUSTES CRÍTICOS EXPLORACIÓN:
- epsilon_decay: 0.999 (MÁS LENTO que 0.995)
  → Mantiene ε>0.5 durante ~700 eps
  → ε=0.1 en ~2300 eps (vs 460 eps con 0.995)
- epsilon_min: 0.1 (NO 0.01)
  → NUNCA deja de explorar 10%

Gate Fase 1: Success >80% en 500 eps
Si falla: Bug implementación DQN
Si pasa: Proceder Fase 2 (6×6 transfer)
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
print("CURRICULUM FASE 1: Grid 4×4 Hello World")
print("="*70)
print("\nObjetivo: Validar DQN aprende con economía v11 viable")
print("Si falla: Bug DQN. Si pasa: v10.x era exploración insuficiente.\n")

# Config v11 VIABLE
print("Config v11 (Oráculo 100% success):")
print(f"  initial_resources: {config.ENV_INITIAL_RESOURCES}")
print(f"  step_cost: {config.ENV_STEP_COST}")
print(f"  penalty_low: {config.ENV_PENALTY_LOW_RESOURCES}")
print(f"  threshold_low: {config.ENV_RESOURCE_THRESHOLD_LOW}")
print(f"  goal_reward: {config.ENV_GOAL_REWARD}")
print(f"  spawn_rate: {config.ENV_RESOURCE_SPAWN_RATE}")
print()

# Hiperparámetros Fase 1
GRID_SIZE = 4
NUM_EPISODES = 500
# CRÍTICO: Multiplicador 4.0× (NO 2.0×) para APRENDIZAJE
# Oráculo necesita 2×, DQN explorando necesita 4× para tropezar con meta
MAX_STEPS_MULTIPLIER = 4.0  # 24 pasos (holgura 18 pasos para errores)
MANHATTAN = (GRID_SIZE - 1) * 2  # 6 pasos
MAX_STEPS = int(MANHATTAN * MAX_STEPS_MULTIPLIER)  # 24 pasos

# CRÍTICO: Exploración lenta
EPSILON_START = 1.0
EPSILON_DECAY = 0.999  # MÁS LENTO que 0.995 (mantiene exploración)
EPSILON_MIN = 0.1      # NUNCA deja de explorar 10%

# Gate Fase 1 (4×4 debe ser trivial)
GATE_SUCCESS = 0.80  # >80% últimos 100 eps

print(f"Grid 4×4:")
print(f"  Estados: {GRID_SIZE**2} (vs 36 en 6×6)")
print(f"  Manhattan: {MANHATTAN} pasos (óptimo)")
print(f"  max_steps: {MAX_STEPS} pasos (4× Manhattan, holgura para exploración)")
print(f"  Holgura errores: {MAX_STEPS - MANHATTAN} pasos (~{((MAX_STEPS-MANHATTAN)/MANHATTAN)*100:.0f}% margen)")
print(f"  Probabilidad random goal: ~{100/(GRID_SIZE**2):.1f}%")
print()

print(f"Hiperparámetros Exploración AJUSTADOS:")
print(f"  epsilon_start: {EPSILON_START}")
print(f"  epsilon_decay: {EPSILON_DECAY} (vs 0.995 previo)")
print(f"  epsilon_min: {EPSILON_MIN} (vs 0.01 previo)")
print(f"  Epsilon >0.5 durante: ~{int(np.log(0.5)/np.log(EPSILON_DECAY))} eps")
print(f"  Epsilon →0.1 en: ~{int(np.log(EPSILON_MIN)/np.log(EPSILON_DECAY))} eps")
print()

print(f"Gate Fase 1: Success >{GATE_SUCCESS*100:.0f}% (últimos 100 eps)")
print(f"Episodios: {NUM_EPISODES}")
print()

def state_to_vector(state):
    """Convertir estado abstracto a vector numérico"""
    if isinstance(state, tuple):
        return np.array([val for _, val in state], dtype=np.float32)
    return np.array(state, dtype=np.float32)

# Environment 4×4
env = ResourceDensityEnv(
    size=GRID_SIZE,
    initial_resources=config.ENV_INITIAL_RESOURCES,
    step_cost=config.ENV_STEP_COST,
    resource_reward=0.75,
    resource_spawn_rate=config.ENV_RESOURCE_SPAWN_RATE,
    max_steps_multiplier=MAX_STEPS_MULTIPLIER,
)

# DQN Agent con epsilon lento
state = env.reset()
state_size = len(state_to_vector(state))
action_size = 5  # up, down, left, right, noop

agent = DQNAgent(
    state_dim=state_size,
    action_dim=action_size,
    lr=config.DQN_LEARNING_RATE,
    gamma=config.DQN_GAMMA,
    epsilon=EPSILON_START,
    epsilon_decay=EPSILON_DECAY,
    epsilon_end=EPSILON_MIN,
    batch_size=32,
    memory_size=10000,
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
    "goal_reached_episodes": [],  # Episodios donde alcanzó goal
}

print(f"{'='*70}")
print(f"ENTRENAMIENTO Fase 1")
print(f"{'='*70}\n")

# Training loop
for ep in range(NUM_EPISODES):
    state = env.reset()
    state_vec = state_to_vector(state)
    done = False
    total_reward = 0
    steps = 0
    
    while not done:
        action_idx = agent.act(state_vec)  # Devuelve 0-4
        # FIX: Mapear índice a string action
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
    metrics["starvation"].append(1 if info.get('starvation', False) else 0)
    metrics["tripwires"].append(1 if info.get('tripwire', False) else 0)
    metrics["epsilon"].append(agent.epsilon)
    
    if success:
        metrics["goal_reached_episodes"].append(ep + 1)
    
    # Progress detallado (cada 50 eps)
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
        
        # CRÍTICO: Reportar PRIMER éxito
        if metrics["goal_reached_episodes"] and ep + 1 == metrics["goal_reached_episodes"][-1]:
            print(f"  ✅ PRIMER ÉXITO en episodio {ep+1}!")

# Resultados finales
print(f"\n{'='*70}")
print(f"RESULTADOS FASE 1: Grid 4×4")
print(f"{'='*70}")

last_100 = min(100, NUM_EPISODES)
success_rate = np.mean(metrics["success"][-last_100:]) * 100
success_rate_total = np.mean(metrics["success"]) * 100
reward_mean = np.mean(metrics["rewards"][-last_100:])
resources_mean = np.mean(metrics["resources"][-last_100:])
steps_mean = np.mean(metrics["steps"][-last_100:])
starvation_rate = np.mean(metrics["starvation"][-last_100:]) * 100

total_successes = sum(metrics["success"])
first_success_ep = metrics["goal_reached_episodes"][0] if metrics["goal_reached_episodes"] else None

print(f"\nMétricas Globales:")
print(f"  Success total: {success_rate_total:.1f}% ({total_successes}/{NUM_EPISODES})")
print(f"  Primer éxito: Episodio {first_success_ep if first_success_ep else 'NUNCA'}")
print(f"  Epsilon final: {agent.epsilon:.4f}")
print()

print(f"Métricas Últimos {last_100} Eps:")
print(f"  Success: {success_rate:.1f}%")
print(f"  Reward: {reward_mean:.2f}")
print(f"  Resources: {resources_mean:.2f}")
print(f"  Steps: {steps_mean:.1f} / {MAX_STEPS}")
print(f"  Starvation: {starvation_rate:.1f}%")
print()

# Gate Fase 1
print(f"{'='*70}")
print(f"GATE FASE 1")
print(f"{'='*70}")

gate_passed = success_rate > GATE_SUCCESS * 100

if gate_passed:
    print(f"✅ GATE APROBADO: Success {success_rate:.1f}% > {GATE_SUCCESS*100:.0f}%")
    print(f"   → DQN funcional con economía v11 viable")
    print(f"   → v10.x falló por exploración insuficiente (epsilon_decay 0.995)")
    print(f"   → Proceder Fase 2: 6×6 con transfer learning")
else:
    print(f"❌ GATE FALLIDO: Success {success_rate:.1f}% ≤ {GATE_SUCCESS*100:.0f}%")
    
    if first_success_ep is None:
        print(f"   → CRÍTICO: NUNCA alcanzó goal en {NUM_EPISODES} eps")
        print(f"   → Posible bug implementación DQN o state encoding")
        print(f"   → Revisar:")
        print(f"     1. state_to_vector() convierte correctamente")
        print(f"     2. DQNAgent.act() selecciona acciones válidas")
        print(f"     3. Environment.step() detecta goal correctamente")
    elif first_success_ep > 100:
        print(f"   → Primer éxito tardío (ep {first_success_ep})")
        print(f"   → Posible: epsilon decay aún rápido O reward shaping insuficiente")
        print(f"   → Sugerencia: epsilon_decay 0.9995 O shaped rewards distancia")
    else:
        print(f"   → Primer éxito temprano (ep {first_success_ep}) PERO no consolidó")
        print(f"   → Posible: learning_rate muy alto O batch_size muy pequeño")
        print(f"   → Sugerencia: lr 1e-4 O batch_size 64")

# Análisis exploración
print(f"\n{'='*70}")
print(f"ANÁLISIS EXPLORACIÓN")
print(f"{'='*70}")

# Encontrar cuándo epsilon cayó <0.5
eps_below_half = next((i for i, e in enumerate(metrics["epsilon"]) if e < 0.5), None)
eps_at_first_success = metrics["epsilon"][first_success_ep - 1] if first_success_ep else None

print(f"Epsilon <0.5 en episodio: {eps_below_half if eps_below_half else 'NUNCA'}")
if first_success_ep:
    print(f"Epsilon en primer éxito (ep {first_success_ep}): {eps_at_first_success:.4f}")
    
    if eps_at_first_success > 0.5:
        print(f"  ✅ Primer éxito con exploración alta (ε={eps_at_first_success:.4f})")
        print(f"     → Buena señal: Agent descubrió goal durante fase random")
    else:
        print(f"  ⚠️  Primer éxito con exploración baja (ε={eps_at_first_success:.4f})")
        print(f"     → Agent tardó en explorar suficiente")

# Guardar resultados
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = ROOT / "results" / f"curriculum_phase1_4x4_{timestamp}"
output_dir.mkdir(parents=True, exist_ok=True)

df_metrics = pd.DataFrame({
    "episode": range(1, NUM_EPISODES + 1),
    "success": metrics["success"],
    "reward": metrics["rewards"],
    "steps": metrics["steps"],
    "resources": metrics["resources"],
    "epsilon": metrics["epsilon"],
})
df_metrics.to_csv(output_dir / "training_metrics.csv", index=False)

# Summary
summary = {
    "grid_size": GRID_SIZE,
    "num_episodes": NUM_EPISODES,
    "epsilon_decay": EPSILON_DECAY,
    "epsilon_min": EPSILON_MIN,
    "success_rate_last100": success_rate,
    "success_rate_total": success_rate_total,
    "total_successes": total_successes,
    "first_success_episode": first_success_ep,
    "epsilon_final": agent.epsilon,
    "gate_passed": gate_passed,
    "gate_threshold": GATE_SUCCESS * 100,
}
pd.DataFrame([summary]).to_csv(output_dir / "summary.csv", index=False)

# Guardar modelo si pasó gate
if gate_passed:
    import torch
    model_path = output_dir / "dqn_phase1_4x4.pth"
    torch.save({
        'q_network': agent.q_network.state_dict(),
        'target_network': agent.target_network.state_dict(),
        'epsilon': agent.epsilon,
        'episode': NUM_EPISODES,
    }, model_path)
    print(f"\n✅ Modelo guardado: {model_path}")
    print(f"   → Usar para Fase 2 (6×6 transfer learning)")

print(f"\nResultados completos: {output_dir}")
print("="*70)
