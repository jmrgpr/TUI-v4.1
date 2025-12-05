"""
Script de auditoría para verificar si los experimentos 4x4 realmente usaron grid 4x4
"""
import sys
import numpy as np

# Agregar path para importar módulos
sys.path.insert(0, 'C:/Proyectos/TUI-v4.1')

from sim.environment import SimbiosisEnv
from sim.runner import run_experiment

print("=" * 80)
print("AUDITORÍA DE GRID_SIZE")
print("=" * 80)

# Test 1: Verificar signatura de SimbiosisEnv.__init__
print("\n1. Inspeccionando SimbiosisEnv.__init__()...")
import inspect
sig = inspect.signature(SimbiosisEnv.__init__)
print(f"   Parámetros: {list(sig.parameters.keys())}")

# Test 2: Verificar si acepta 'size'
print("\n2. Test: ¿SimbiosisEnv acepta 'size'?")
try:
    env = SimbiosisEnv(size=4)
    print(f"   ✅ SÍ acepta 'size' - env.size = {env.size}")
    print(f"   Meta position: {env.goal_pos}")
except TypeError as e:
    print(f"   ❌ NO acepta 'size': {e}")

# Test 3: Verificar si acepta 'grid_size'
print("\n3. Test: ¿SimbiosisEnv acepta 'grid_size'?")
try:
    env = SimbiosisEnv(grid_size=4)
    print(f"   ✅ SÍ acepta 'grid_size' - env.size = {env.size}")
except TypeError as e:
    print(f"   ❌ NO acepta 'grid_size': {e}")

# Test 4: Verificar signatura de run_experiment
print("\n4. Inspeccionando run_experiment()...")
sig = inspect.signature(run_experiment)
print(f"   Parámetros: {list(sig.parameters.keys())}")

# Test 5: Ejecutar mini experimento con grid_size=4
print("\n5. Test: Ejecutar run_experiment(grid_size=4, episodes=2)...")
try:
    result = run_experiment(
        episodes=2,
        seed=999,
        risk_scale=1.5,
        agent_name="Test",
        use_pgf=False,
        use_dqn=False,
        grid_size=4
    )
    print(f"   ✅ run_experiment ejecutó exitosamente")
    print(f"   Recompensa media: {result['avg_reward']:.2f}")
    print(f"   Total_rewards: {result['total_rewards']}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 6: Verificar tamaño del grid inspeccionando el código de runner.py
print("\n6. Inspeccionando código de runner.py...")
with open('sim/runner.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if 'SimbiosisEnv(' in line and 'env =' in line:
            print(f"   Línea {i}: {line.strip()}")
            # Mostrar contexto
            for j in range(max(0, i-3), min(len(lines), i+2)):
                print(f"   {j+1}: {lines[j].rstrip()}")
            break

# Test 7: Verificar diferencia en recompensas promedio entre 4x4 y 5x5
print("\n7. Comparación empírica: 4x4 vs 5x5 (5 episodios cada uno)")
print("   Ejecutando grid_size=4...")
result_4x4 = run_experiment(
    episodes=5,
    seed=42,
    risk_scale=1.5,
    agent_name="Test_4x4",
    use_pgf=False,
    use_dqn=False,
    grid_size=4
)
print(f"   Grid 4x4 - Recompensa media: {result_4x4['avg_reward']:.2f}")
print(f"   Recompensas: {result_4x4['total_rewards']}")

print("\n   Ejecutando grid_size=5...")
result_5x5 = run_experiment(
    episodes=5,
    seed=42,
    risk_scale=1.5,
    agent_name="Test_5x5",
    use_pgf=False,
    use_dqn=False,
    grid_size=5
)
print(f"   Grid 5x5 - Recompensa media: {result_5x5['avg_reward']:.2f}")
print(f"   Recompensas: {result_5x5['total_rewards']}")

print("\n8. CONCLUSIONES:")
if result_4x4['total_rewards'] == result_5x5['total_rewards']:
    print("   🚨 ALERTA: Las recompensas son IDÉNTICAS - grid_size NO está funcionando")
    print("   ❌ Los experimentos 4x4 NO SON VÁLIDOS")
else:
    print("   ✅ Las recompensas son DIFERENTES - grid_size está funcionando")
    print("   ✅ Los experimentos 4x4 SON VÁLIDOS")

print("\n" + "=" * 80)
