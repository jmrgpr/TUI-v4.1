"""
Diagnóstico CRÍTICO: Verificar que tripwires se generan y detectan correctamente
"""
from sim.environment_v2 import ResourceDensityEnv
import numpy as np

# Test 1: Generación de tripwires
print("=" * 60)
print("TEST 1: Generación de tripwires en grid 4×4, spawn=0.25")
print("=" * 60)

np.random.seed(42)
env = ResourceDensityEnv(size=4, resource_spawn_rate=0.25, step_cost=-0.2, resource_reward=1.0)
env.reset()

tripwires = [(r,c) for r in range(4) for c in range(4) if env.grid[r,c] == -1]
print(f"Tripwires generados: {len(tripwires)}")
print(f"Posiciones: {tripwires}")
print(f"Esperado (promedio): ~4 tripwires (0.25 × 16 celdas)")

# Test 2: Detección de tripwires al pisar
print("\n" + "=" * 60)
print("TEST 2: Detección de tripwires al pisar")
print("=" * 60)

if len(tripwires) > 0:
    target_tripwire = tripwires[0]
    print(f"Target tripwire: {target_tripwire}")
    
    # Resetear y colocar agente adyacente al tripwire
    env.reset()
    env.agent_pos = np.array([target_tripwire[0], max(0, target_tripwire[1]-1)])
    print(f"Agente posicionado en: {env.agent_pos}")
    
    # Mover hacia el tripwire (acción derecha = 1)
    action = 1  # Right
    obs, reward, done, info = env.step(action)
    
    print(f"Después de step hacia tripwire:")
    print(f"  Nueva posición: {env.agent_pos}")
    print(f"  Reward: {reward}")
    print(f"  info['tripwire']: {info.get('tripwire', 'KEY NOT FOUND')}")
    print(f"  done: {done}")
else:
    print("⚠️ NO SE GENERARON TRIPWIRES - Seed 42 con spawn=0.25 no creó ninguno")

# Test 3: Simulación completa 100 episodios
print("\n" + "=" * 60)
print("TEST 3: Simulación 100 episodios random walk")
print("=" * 60)

tripwire_encounters = 0
total_steps = 0

for ep in range(100):
    env.reset()
    done = False
    steps = 0
    
    while not done and steps < 50:
        action = np.random.randint(0, 4)
        obs, reward, done, info = env.step(action)
        
        if info.get('tripwire', False):
            tripwire_encounters += 1
        
        steps += 1
    
    total_steps += steps

print(f"Episodios: 100")
print(f"Tripwires pisados: {tripwire_encounters}")
print(f"Tasa: {tripwire_encounters/total_steps:.4f} tripwires por step")
print(f"Esperado: ~0.0156 (1/64 celdas con movimiento random)")

if tripwire_encounters == 0:
    print("⚠️ CRÍTICO: Ningún tripwire pisado en 100 episodios")
    print("   Posibles causas:")
    print("   1. info['tripwire'] no se está setteando en environment_v2.py")
    print("   2. Tripwires no se están generando (seed específico?)")
    print("   3. Agent init position evita tripwires por diseño")
