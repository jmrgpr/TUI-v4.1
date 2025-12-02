"""
Test rápido de environment_v2.py con recursos dinámicos

Ejecuta 1 configuración con pocos episodios para verificar que funciona.

Uso:
    python scripts/test_density_env.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
import numpy as np

print("\n" + "="*80)
print("🧪 TEST RÁPIDO: environment_v2.py con recursos dinámicos")
print("="*80 + "\n")

# Configuración de test
np.random.seed(42)
env = ResourceDensityEnv(
    size=4,
    resource_spawn_rate=0.5,
    resource_reward=5.0,
    risk_scale=1.5
)

print(f"✓ Entorno creado: {env.size}x{env.size}, spawn_rate={env.resource_spawn_rate}")

# Crear agentes (DQNAgent solo necesita dimensiones)
state = env.reset()
state_dim = len([v for _, v in state])
action_dim = 4  # up, down, left, right

agent_pgf = DQNAgent(state_dim, action_dim)
agent_control = DQNAgent(state_dim, action_dim)

print(f"✓ Agentes creados: PGF + Control\n")

# Ejecutar 10 episodios de prueba
print("Ejecutando 10 episodios de prueba...\n")

actions_map = ['up', 'down', 'left', 'right']

for ep in range(10):
    agent = agent_pgf if ep % 2 == 0 else agent_control
    agent_name = "PGF" if ep % 2 == 0 else "Control"
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    resources_collected = 0
    
    while not done:
        # Convertir estado a vector
        state_vec = np.array([v for _, v in state], dtype=np.float32)
        action_idx = agent.act(state_vec)
        action = actions_map[action_idx]
        
        next_state, reward, done, info = env.step(action)
        
        # Remember transition
        state_vec = np.array([v for _, v in state], dtype=np.float32)
        next_state_vec = np.array([v for _, v in next_state], dtype=np.float32)
        agent.remember(state_vec, action_idx, reward, next_state_vec, done)
        agent.learn()  # Usar learn() en lugar de replay()
        
        state = next_state
        total_reward += reward
        steps += 1
        
        if info.get('resource_collected', False):
            resources_collected += 1
    
    # Métricas de densidad
    density = env.compute_D_effective()
    
    print(f"Episode {ep+1}: {agent_name:8} | Reward: {total_reward:6.2f} | Steps: {steps:3} | "
          f"Resources: {resources_collected} | D_eff: {density['D_effective']:.3f}")

print("\n" + "="*80)
print("✅ TEST COMPLETADO - environment_v2.py funciona correctamente")
print("="*80)
print("\nPróximo paso: Ejecutar batch completo")
print("  python scripts/run_experiment_2_density.py")
print("="*80 + "\n")
