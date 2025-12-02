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

# Crear agentes
agent_pgf = DQNAgent(env, use_pgf=True, name="PGF")
agent_control = DQNAgent(env, use_pgf=False, name="Control")

print(f"✓ Agentes creados: PGF + Control\n")

# Ejecutar 10 episodios de prueba
print("Ejecutando 10 episodios de prueba...\n")

for ep in range(10):
    agent = agent_pgf if ep % 2 == 0 else agent_control
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    resources_collected = 0
    
    while not done:
        action = agent.act(state, explore=True)
        next_state, reward, done, info = env.step(action)
        
        agent.remember(state, action, reward, next_state, done)
        agent.replay()
        
        state = next_state
        total_reward += reward
        steps += 1
        
        if info.get('resource_collected', False):
            resources_collected += 1
    
    # Métricas de densidad
    density = env.compute_D_effective()
    
    print(f"Episode {ep+1}: {agent.name:8} | Reward: {total_reward:6.2f} | Steps: {steps:3} | "
          f"Resources: {resources_collected} | D_eff: {density['D_effective']:.3f}")

print("\n" + "="*80)
print("✅ TEST COMPLETADO - environment_v2.py funciona correctamente")
print("="*80)
print("\nPróximo paso: Ejecutar batch completo")
print("  python scripts/run_experiment_2_density.py")
print("="*80 + "\n")
