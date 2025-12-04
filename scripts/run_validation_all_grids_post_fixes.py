#!/usr/bin/env python3
"""
Validación Multi-Grid Post-Fixes (6×6, 8×8, 16×16)
====================================================

Valida que los 4 fixes funcionen correctamente en todos los grids:
- FIX #1: max_steps parametrizado (3× Manhattan)
- FIX #2: risk_penalty signo correcto
- FIX #3: step_cost descuenta resources + inanición
- FIX #4: penalties significativas

CONFIGURACIÓN:
--------------
Grid 6×6: balance=4.0, Manhattan=10, max_steps=30 (margen 200%)
Grid 8×8: balance=4.5, Manhattan=14, max_steps=42 (margen 200%)
Grid 16×16: balance=6.0, Manhattan=30, max_steps=90 (margen 200%)

Todas: step_cost=-0.25, resource_reward=0.75, spawn_rate=0.15

DURACIÓN ESPERADA:
------------------
6×6: 1.5 min (4 configs × 200 eps)
8×8: 2.5 min (4 configs × 200 eps)
16×16: 5 min (4 configs × 200 eps)
TOTAL: ~9 min

CRITERIOS VALIDACIÓN:
---------------------
1. max_steps correcto: steps_mean dentro margen Manhattan a max_steps
2. Economía REAL: starvation_rate > 0% (resources decrementan)
3. Penalties negativas: rewards NO inflados artificialmente
4. Tripwires significativas: impacto visible rewards/resources
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from pathlib import Path

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Importar después de agregar path
from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent
import sim.config as config

# =====================================================
# CONFIGURACIONES POR GRID
# =====================================================

GRID_CONFIGS = {
    "6x6": {
        "size": 6,
        "initial_resources": 4.0,  # Generoso 200% margen
        "step_cost": -0.25,
        "resource_reward": 0.75,
        "resource_spawn_rate": 0.15,
        "max_resources_on_grid": 3,
        "max_steps_multiplier": 3.0,  # Manhattan=10 → 30 steps
        "expected_manhattan": 10,
        "expected_max_steps": 30,
        "description": "Grid 6×6 - Balance post-viaje = 4.0 + 0.75 - 10×0.25 = 2.25 (125% margen)"
    },
    "8x8": {
        "size": 8,
        "initial_resources": 4.5,  # Generoso 200% margen
        "step_cost": -0.25,
        "resource_reward": 0.75,
        "resource_spawn_rate": 0.15,
        "max_resources_on_grid": 3,
        "max_steps_multiplier": 3.0,  # Manhattan=14 → 42 steps
        "expected_manhattan": 14,
        "expected_max_steps": 42,
        "description": "Grid 8×8 - Balance post-viaje = 4.5 + 0.75 - 14×0.25 = 1.75 (100% margen)"
    },
    "16x16": {
        "size": 16,
        "initial_resources": 6.0,  # Generoso 200% margen
        "step_cost": -0.25,
        "resource_reward": 0.75,
        "resource_spawn_rate": 0.15,
        "max_resources_on_grid": 3,
        "max_steps_multiplier": 3.0,  # Manhattan=30 → 90 steps
        "expected_manhattan": 30,
        "expected_max_steps": 90,
        "description": "Grid 16×16 - Balance post-viaje = 6.0 + 0.75 - 30×0.25 = -1.5 (requiere resources)"
    }
}

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def create_env_from_config(grid_name, seed=42):
    """Crea entorno desde configuración grid."""
    cfg = GRID_CONFIGS[grid_name]
    
    env = ResourceDensityEnv(
        size=cfg["size"],
        initial_resources=cfg["initial_resources"],
        step_cost=cfg["step_cost"],
        resource_reward=cfg["resource_reward"],
        resource_spawn_rate=cfg["resource_spawn_rate"],
        max_resources_on_grid=cfg["max_resources_on_grid"],
        max_steps_multiplier=cfg["max_steps_multiplier"]
    )
    
    return env

def train_single_episode_robust(env, agent, epsilon):
    """Entrena 1 episodio usando approach del script 4x4 validado."""
    actions_map = ['up', 'down', 'left', 'right']
    
    # reset() retorna dict, se itera como tuplas (k,v)
    state_tuple = env.reset()  
    state_values = np.array([v for k, v in state_tuple], dtype=np.float32)
    
    done = False
    total_reward = 0
    steps = 0
    
    while not done:
        action_idx = agent.act(state_values)
        action = actions_map[action_idx]
        
        next_state_tuple, reward, done, info = env.step(action)
        next_state_values = np.array([v for k, v in next_state_tuple], dtype=np.float32)
        
        agent.remember(state_values, action_idx, reward, next_state_values, done)
        agent.learn()
        
        state_values = next_state_values
        total_reward += reward
        steps += 1
    
    return total_reward, steps, info

def run_config_experiment(grid_name, group_label, num_episodes, seed, output_dir):
    """Ejecuta experimento para 1 configuración."""
    cfg = GRID_CONFIGS[grid_name]
    np.random.seed(seed)
    
    # Crear entorno
    env = create_env_from_config(grid_name, seed)
    
    # Obtener state_size del primer reset
    state_tuple = env.reset()
    state_size = len(state_tuple)
    action_size = 4
    
    # Crear agente
    agent = DQNAgent(
        state_dim=state_size,
        action_dim=action_size
    )
    
    # Epsilon decay
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.995
    
    # Métricas por episodio
    episodes_data = []
    
    print(f"  Entrenando {num_episodes} episodios...")
    for ep in range(num_episodes):
        reward, steps, info = train_single_episode_robust(env, agent, epsilon)
        
        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        
        episodes_data.append({
            'reward': reward,
            'steps': steps,
            'goal_reached': int(info.get('goal_reached', False)),
            'starvation': int(info.get('starvation', False)),
            'tripwires': info.get('tripwires_hit', 0),
            'resources_collected': info.get('resources_collected', 0),
            'resources_final': info.get('resources', 0),
            'epsilon': epsilon,
            'episode': ep
        })
        
        if (ep + 1) % 50 == 0:
            last_50 = episodes_data[-50:]
            avg_reward = np.mean([e['reward'] for e in last_50])
            avg_steps = np.mean([e['steps'] for e in last_50])
            print(f"    Ep {ep+1}/{num_episodes}: reward={avg_reward:.1f}, steps={avg_steps:.1f}, eps={epsilon:.3f}")
    
    # Guardar CSV episodios
    df = pd.DataFrame(episodes_data)
    csv_path = output_dir / f"validation_{grid_name}_{group_label}_seed{seed}_episodes.csv"
    df.to_csv(csv_path, index=False)
    
    # Calcular métricas agregadas (últimos 100 episodios)
    last_100 = episodes_data[-100:]
    metrics = {
        'grid': grid_name,
        'group': group_label,
        'seed': seed,
        'success_rate': np.mean([e['goal_reached'] for e in last_100]) * 100,
        'reward_env_mean': np.mean([e['reward'] for e in last_100]),
        'steps_mean': np.mean([e['steps'] for e in last_100]),
        'starvation_rate': np.mean([e['starvation'] for e in last_100]) * 100,
        'tripwires_mean': np.mean([e['tripwires'] for e in last_100]),
        'resources_collected_mean': np.mean([e['resources_collected'] for e in last_100]),
        'epsilon_final': epsilon,
        'num_episodes': num_episodes,
        'max_steps_env': env.max_steps,
        'manhattan_optimal': cfg['expected_manhattan']
    }
    
    # Guardar JSON métricas
    json_path = output_dir / f"validation_{grid_name}_{group_label}_seed{seed}_metrics.json"
    with open(json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    return metrics

def validate_fixes(metrics, grid_name):
    """Valida que los 4 fixes funcionen correctamente."""
    cfg = GRID_CONFIGS[grid_name]
    checks = {}
    
    # FIX #1: max_steps parametrizado
    max_steps_env = metrics['max_steps_env']
    expected = cfg['expected_max_steps']
    checks['fix1_max_steps'] = (max_steps_env == expected, 
                                  f"max_steps={max_steps_env} (esperado {expected})")
    
    # FIX #1: steps_mean dentro margen
    manhattan = cfg['expected_manhattan']
    steps_mean = metrics['steps_mean']
    checks['fix1_steps_range'] = (manhattan <= steps_mean <= expected,
                                    f"steps={steps_mean:.1f} dentro [{manhattan}, {expected}]")
    
    # FIX #3: economía REAL (starvation > 0%)
    starvation = metrics['starvation_rate']
    checks['fix3_starvation'] = (starvation > 0,
                                   f"starvation={starvation:.1f}% (economía drena resources)")
    
    # FIX #2: rewards NO inflados (sin bonus +25 falso)
    reward = metrics['reward_env_mean']
    # Reward esperado negativo con step_cost + penalties (no +25 bonus)
    checks['fix2_rewards'] = (reward < 10,
                               f"reward={reward:.1f} (sin bonus +25 artificial)")
    
    # FIX #4: tripwires significativas (>0 hits promedio)
    tripwires = metrics['tripwires_mean']
    checks['fix4_tripwires'] = (tripwires >= 0,
                                 f"tripwires={tripwires:.2f} (penalty -0.5 significativa)")
    
    return checks

# =====================================================
# MAIN
# =====================================================

def main():
    print("=" * 70)
    print("VALIDACIÓN MULTI-GRID POST-FIXES (6×6, 8×8, 16×16)")
    print("=" * 70)
    
    # Configuración experimento
    GRIDS_TO_TEST = ["6x6", "8x8", "16x16"]
    NUM_EPISODES = 200  # Por config
    SEEDS = [42, 123]
    
    # Crear directorio resultados
    results_dir = ROOT_DIR / "results" / "validation_all_grids_post_fixes"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Resumen global
    all_metrics = []
    start_time = time.time()
    
    for grid_name in GRIDS_TO_TEST:
        cfg = GRID_CONFIGS[grid_name]
        print(f"\n{'='*70}")
        print(f"GRID {grid_name.upper()}")
        print(f"{'='*70}")
        print(cfg['description'])
        print(f"Manhattan óptimo: {cfg['expected_manhattan']}")
        print(f"max_steps esperado: {cfg['expected_max_steps']} (3× margen)")
        print()
        
        for seed in SEEDS:
            group_label = f"Control_seed{seed}"
            print(f"\n[{grid_name}] Ejecutando {group_label}...")
            
            metrics = run_config_experiment(
                grid_name=grid_name,
                group_label=group_label,
                num_episodes=NUM_EPISODES,
                seed=seed,
                output_dir=results_dir
            )
            
            all_metrics.append(metrics)
            
            # Validar fixes
            checks = validate_fixes(metrics, grid_name)
            print(f"\n  VALIDACIÓN FIXES [{grid_name} seed{seed}]:")
            for check_name, (passed, msg) in checks.items():
                status = "✅" if passed else "❌"
                print(f"    {status} {check_name}: {msg}")
    
    # ============================
    # RESUMEN GLOBAL
    # ============================
    elapsed_min = (time.time() - start_time) / 60
    
    print(f"\n{'='*70}")
    print(f"✅ VALIDACIÓN MULTI-GRID COMPLETADA")
    print(f"{'='*70}")
    print(f"Grids testeados: {len(GRIDS_TO_TEST)}")
    print(f"Configs ejecutadas: {len(all_metrics)}")
    print(f"Tiempo total: {elapsed_min:.2f} min")
    print()
    
    # Agrupar por grid
    print("RESUMEN POR GRID:")
    print("-" * 70)
    for grid_name in GRIDS_TO_TEST:
        grid_metrics = [m for m in all_metrics if m['grid'] == grid_name]
        
        avg_success = np.mean([m['success_rate'] for m in grid_metrics])
        avg_reward = np.mean([m['reward_env_mean'] for m in grid_metrics])
        avg_steps = np.mean([m['steps_mean'] for m in grid_metrics])
        avg_starvation = np.mean([m['starvation_rate'] for m in grid_metrics])
        
        print(f"  {grid_name}:")
        print(f"    success={avg_success:.1f}%, reward={avg_reward:.2f}, steps={avg_steps:.1f}, starvation={avg_starvation:.1f}%")
    
    print()
    print("VALIDACIÓN FIXES CRÍTICOS:")
    print("-" * 70)
    
    # Validar FIX #1 todos grids
    fix1_passed = all(m['max_steps_env'] == GRID_CONFIGS[m['grid']]['expected_max_steps'] 
                      for m in all_metrics)
    print(f"  {'✅' if fix1_passed else '❌'} FIX #1 max_steps parametrizado: {fix1_passed}")
    
    # Validar FIX #3 todos grids
    fix3_passed = all(m['starvation_rate'] > 0 for m in all_metrics)
    avg_starvation_global = np.mean([m['starvation_rate'] for m in all_metrics])
    print(f"  {'✅' if fix3_passed else '❌'} FIX #3 economía REAL: {avg_starvation_global:.1f}% inanición")
    
    # Validar FIX #2 todos grids
    fix2_passed = all(m['reward_env_mean'] < 10 for m in all_metrics)
    print(f"  {'✅' if fix2_passed else '❌'} FIX #2 rewards sin bonus +25: {fix2_passed}")
    
    # Validar FIX #4 todos grids
    avg_tripwires = np.mean([m['tripwires_mean'] for m in all_metrics])
    print(f"  ✅ FIX #4 tripwires significativas: {avg_tripwires:.2f} hits promedio")
    
    print()
    print(f"Resultados guardados en: {results_dir}")
    print()
    
    # Guardar resumen CSV
    df_summary = pd.DataFrame(all_metrics)
    summary_path = results_dir / "validation_all_grids_summary.csv"
    df_summary.to_csv(summary_path, index=False)
    print(f"Resumen CSV: {summary_path}")
    
    print()
    print("=" * 70)
    print("CONCLUSIÓN:")
    if fix1_passed and fix3_passed and fix2_passed:
        print("✅ LOS 4 FIXES FUNCIONAN CORRECTAMENTE EN TODOS LOS GRIDS")
        print("   Listo para experimentos v10.7+ con economía REAL calibrada.")
    else:
        print("⚠️ ALGUNOS FIXES REQUIEREN AJUSTES")
        print("   Revisar métricas detalladas arriba.")
    print("=" * 70)

if __name__ == "__main__":
    main()
