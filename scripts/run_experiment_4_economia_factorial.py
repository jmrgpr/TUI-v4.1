"""
Script de Ejecución - Experimento 4: Economía Factorial (PGF v7)
==================================================================

Experimento preregistrado para validar Hipótesis H7.1-H7.3:
- H7.1: Goldilocks emerge solo con slack económico (balance > threshold)
- H7.2: Threshold balance crítico ≈ 5.0 ± 1.0
- H7.3: Resultados robustos post-fixes metodológicos (spawn, seeds)

Diseño: 3 economías × 5 densidades × 3 seeds = 45 configuraciones

Uso:
    # Ejecución completa (45 configs, ~36 min)
    python scripts/run_experiment_4_economia_factorial.py
    
    # Test mode (3 configs, ~2 min)
    python scripts/run_experiment_4_economia_factorial.py --test_mode
    
    # Bloque específico
    python scripts/run_experiment_4_economia_factorial.py --economies harsh

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
Preregistro: results/pgf_v7/PREREGISTRO_v7.md (commit 3c7d6a8)
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import random

# Agregar directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent


# ============================================================================
# CONFIGURACIONES DE ECONOMÍA (Preregistradas)
# ============================================================================

ECONOMY_CONFIGS = {
    'harsh': {
        'step_cost': -0.3,
        'resource_reward': 1.0,
        'label': 'Harsh (v6 baseline)',
        'balance': 3.33,
        'description': 'Régimen de supervivencia extrema (step_cost alto)'
    },
    'balanced': {
        'step_cost': -0.2,
        'resource_reward': 1.0,
        'label': 'Balanced',
        'balance': 5.0,
        'description': 'Régimen equilibrado (threshold crítico esperado)'
    },
    'favorable': {
        'step_cost': -0.1,
        'resource_reward': 1.0,
        'label': 'Favorable',
        'balance': 10.0,
        'description': 'Régimen con slack económico (Goldilocks esperado)'
    }
}


# ============================================================================
# FUNCIÓN DE SEEDING COMPLETO (Fix v7)
# ============================================================================

def configure_all_seeds(seed):
    """
    Configura todos los generadores de números aleatorios para reproducibilidad completa.
    
    FIX v7: Cubre random, numpy, torch (CPU + CUDA) vs solo numpy en v6.
    
    Args:
        seed: Semilla entera (42, 123, 456, etc.)
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    # CUDA si disponible
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    
    # Opcional: Determinismo completo (más lento, no necesario para v7)
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False


# ============================================================================
# FUNCIÓN DE ENTRENAMIENTO (Idéntica a v6, pero con seeding mejorado)
# ============================================================================

def train_agent(env, agent, num_episodes, agent_type='PGF', verbose_freq=50):
    """
    Entrena un agente durante num_episodes.
    
    Args:
        env: Entorno ResourceDensityEnv
        agent: Agente DQN (PGF o Control)
        num_episodes: Número de episodios de entrenamiento
        agent_type: Etiqueta ('PGF' o 'Control')
        verbose_freq: Cada cuántos episodios imprimir progreso
    
    Returns:
        episode_data: Lista de diccionarios con datos por episodio
    """
    # Mapeo de acciones
    actions_map = ['up', 'down', 'left', 'right']
    episode_data = []
    
    for ep in range(num_episodes):
        state_dict = env.reset()
        total_reward = 0
        steps = 0
        done = False
        
        resources_collected = 0
        initial_resources = env.agent_resources
        
        while not done:
            # Convertir estado abstracto a vector
            state_vec = np.array([v for _, v in state_dict], dtype=np.float32)
            
            # Seleccionar acción
            action_idx = agent.act(state_vec)
            action = actions_map[action_idx]
            
            # Ejecutar acción
            next_state_dict, reward, done, info = env.step(action)
            next_state_vec = np.array([v for _, v in next_state_dict], dtype=np.float32)
            
            # Entrenar agente
            agent.remember(state_vec, action_idx, reward, next_state_vec, done)
            agent.learn()
            
            # Actualizar estado
            state_dict = next_state_dict
            total_reward += reward
            steps += 1
            
            # Contar recursos consumidos
            if env.agent_resources > initial_resources:
                resources_collected += 1
                initial_resources = env.agent_resources
        
        # Registrar datos del episodio
        episode_data.append({
            'episode': ep + 1,
            'total_reward': total_reward,
            'steps': steps,
            'resources_collected': resources_collected,
            'final_resources': env.agent_resources,
            'goal_reached': info.get('goal_reached', False),
            'death_by_hazard': info.get('death_by_hazard', False),
            'epsilon': agent.epsilon
        })
        
        # Verbose
        if (ep + 1) % verbose_freq == 0 or ep == 0:
            print(f"  [{agent_type}] Episodio {ep+1}/{num_episodes}: "
                  f"Reward={total_reward:.2f}, Steps={steps}, "
                  f"Resources={resources_collected}, ε={agent.epsilon:.3f}")
    
    return episode_data


# ============================================================================
# FUNCIÓN DE EJECUCIÓN DE UNA CONFIGURACIÓN
# ============================================================================

def run_single_config(economy, spawn_rate, seed, num_episodes=300, 
                      output_dir='results/pgf_v7/resultados', verbose=True):
    """
    Ejecuta una configuración completa (PGF + Control).
    
    Args:
        economy: Nombre de economía ('harsh', 'balanced', 'favorable')
        spawn_rate: Densidad de spawn (0.05-0.40)
        seed: Semilla para reproducibilidad
        num_episodes: Episodios por agente (default: 300)
        output_dir: Directorio para guardar resultados
        verbose: Si True, imprime progreso
    
    Returns:
        results: Diccionario con métricas agregadas
    """
    # Configurar seeding completo (FIX v7)
    configure_all_seeds(seed)
    
    # Obtener configuración económica
    econ_config = ECONOMY_CONFIGS[economy]
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"🚀 Configuración: {economy.upper()}, D={spawn_rate}, seed={seed}")
        print(f"   Balance económico: {econ_config['balance']:.2f}")
        print(f"   step_cost={econ_config['step_cost']}, reward={econ_config['resource_reward']}")
        print(f"={'='*70}")
    
    # Crear entorno con parámetros de economía
    env = ResourceDensityEnv(
        size=4,
        step_cost=econ_config['step_cost'],
        resource_reward=econ_config['resource_reward'],
        resource_spawn_rate=spawn_rate,
        max_resources_on_grid=3,
        resource_decay_steps=5,
        risk_scale=1.5
    )
    
    # Parámetros comunes DQN
    state = env.reset()
    state_size = len([v for _, v in state])  # Extraer tamaño del abstract state
    action_size = 4
    
    # =========================================
    # Entrenar PGF Agent
    # =========================================
    if verbose:
        print(f"\n🤖 Entrenando agente PGF ({num_episodes} episodios)...")
    
    configure_all_seeds(seed)  # Re-seed antes de PGF
    agent_pgf = DQNAgent(state_size, action_size)
    episodes_pgf = train_agent(env, agent_pgf, num_episodes, agent_type='PGF', 
                                verbose_freq=50 if verbose else 99999)
    
    # =========================================
    # Entrenar Control Agent
    # =========================================
    if verbose:
        print(f"\n🤖 Entrenando agente Control ({num_episodes} episodios)...")
    
    configure_all_seeds(seed)  # Re-seed antes de Control (entrenamiento simétrico)
    agent_control = DQNAgent(state_size, action_size)
    episodes_control = train_agent(env, agent_control, num_episodes, agent_type='Control',
                                    verbose_freq=50 if verbose else 99999)
    
    # =========================================
    # Calcular métricas agregadas
    # =========================================
    rewards_pgf = [ep['total_reward'] for ep in episodes_pgf]
    rewards_control = [ep['total_reward'] for ep in episodes_control]
    
    mean_reward_pgf = np.mean(rewards_pgf)
    mean_reward_control = np.mean(rewards_control)
    ratio_pgf_control = mean_reward_pgf / mean_reward_control if mean_reward_control != 0 else np.nan
    
    # D_effective aproximado (recursos totales spawneados / episodios / área)
    total_resources_pgf = sum([ep['resources_collected'] for ep in episodes_pgf])
    total_resources_control = sum([ep['resources_collected'] for ep in episodes_control])
    D_effective = (total_resources_pgf + total_resources_control) / (2 * num_episodes * 16)
    
    results = {
        'economy': economy,
        'balance': econ_config['balance'],
        'spawn_rate': spawn_rate,
        'seed': seed,
        'num_episodes': num_episodes,
        'mean_reward_pgf': mean_reward_pgf,
        'std_reward_pgf': np.std(rewards_pgf),
        'mean_reward_control': mean_reward_control,
        'std_reward_control': np.std(rewards_control),
        'ratio_pgf_control': ratio_pgf_control,
        'D_effective': D_effective,
        'mean_steps_pgf': np.mean([ep['steps'] for ep in episodes_pgf]),
        'mean_steps_control': np.mean([ep['steps'] for ep in episodes_control]),
        'goal_rate_pgf': np.mean([ep['goal_reached'] for ep in episodes_pgf]),
        'goal_rate_control': np.mean([ep['goal_reached'] for ep in episodes_control]),
        'timestamp': datetime.now().isoformat()
    }
    
    if verbose:
        print(f"\n📊 Resultados:")
        print(f"   PGF Mean Reward: {mean_reward_pgf:.2f} ± {results['std_reward_pgf']:.2f}")
        print(f"   Control Mean Reward: {mean_reward_control:.2f} ± {results['std_reward_control']:.2f}")
        print(f"   Ratio PGF/Control: {ratio_pgf_control:.4f} ({ratio_pgf_control*100:.2f}%)")
        print(f"   D_effective: {D_effective:.4f}")
    
    # =========================================
    # Guardar resultados
    # =========================================
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Nombre de archivo: exp4_economy_{economy}_spawn{spawn_rate}_seed{seed}
    filename_base = f"exp4_economy_{economy}_spawn{spawn_rate:.2f}_seed{seed}"
    
    # Guardar JSON con métricas agregadas
    json_path = output_path / f"{filename_base}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Guardar CSV con datos por episodio
    df_pgf = pd.DataFrame(episodes_pgf)
    df_pgf['agent_type'] = 'PGF'
    df_control = pd.DataFrame(episodes_control)
    df_control['agent_type'] = 'Control'
    
    df_all = pd.concat([df_pgf, df_control], ignore_index=True)
    df_all['economy'] = economy
    df_all['balance'] = econ_config['balance']
    df_all['spawn_rate'] = spawn_rate
    df_all['seed'] = seed
    
    csv_path = output_path / f"{filename_base}_episodes.csv"
    df_all.to_csv(csv_path, index=False)
    
    if verbose:
        print(f"✅ Guardado: {json_path.name}, {csv_path.name}")
    
    return results


# ============================================================================
# FUNCIÓN PRINCIPAL: EJECUTAR EXPERIMENTO COMPLETO
# ============================================================================

def run_experiment(economies=['harsh', 'balanced', 'favorable'],
                   densities=[0.05, 0.10, 0.20, 0.30, 0.40],
                   seeds=[42, 123, 456],
                   num_episodes=300,
                   output_dir='results/pgf_v7/resultados',
                   test_mode=False):
    """
    Ejecuta experimento factorial completo.
    
    Args:
        economies: Lista de economías a probar
        densities: Lista de densidades (spawn_rate)
        seeds: Lista de seeds
        num_episodes: Episodios por config
        output_dir: Directorio de salida
        test_mode: Si True, ejecuta solo 3 configs × 10 episodios
    
    Returns:
        summary: Lista de diccionarios con resultados de todas las configs
    """
    if test_mode:
        print("🧪 TEST MODE ACTIVADO")
        economies = ['harsh', 'balanced', 'favorable']
        densities = [0.20]  # Solo densidad intermedia
        seeds = [42]
        num_episodes = 10
        print(f"   → Ejecutando 3 configs × {num_episodes} episodios (~2 min)")
    
    total_configs = len(economies) * len(densities) * len(seeds)
    
    print("\n" + "="*70)
    print("🚀 EXPERIMENTO 4: ECONOMÍA FACTORIAL (PGF v7)")
    print("="*70)
    print(f"Configuraciones totales: {total_configs}")
    print(f"Economías: {', '.join(economies)}")
    print(f"Densidades: {densities}")
    print(f"Seeds: {seeds}")
    print(f"Episodios por config: {num_episodes} × 2 agentes = {num_episodes*2}")
    print(f"Episodios totales: {total_configs * num_episodes * 2}")
    print(f"Directorio salida: {output_dir}")
    print("="*70 + "\n")
    
    start_time = time.time()
    summary = []
    
    config_num = 0
    for economy in economies:
        for spawn_rate in densities:
            for seed in seeds:
                config_num += 1
                
                print(f"\n{'#'*70}")
                print(f"📍 Config {config_num}/{total_configs}")
                print(f"{'#'*70}")
                
                try:
                    results = run_single_config(
                        economy=economy,
                        spawn_rate=spawn_rate,
                        seed=seed,
                        num_episodes=num_episodes,
                        output_dir=output_dir,
                        verbose=True
                    )
                    summary.append(results)
                    
                except Exception as e:
                    print(f"❌ ERROR en config {config_num}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
    
    # =========================================
    # Guardar resumen general
    # =========================================
    elapsed_time = time.time() - start_time
    
    summary_path = Path(output_dir) / "experiment_4_summary.json"
    summary_data = {
        'experiment': 'PGF v7 - Economía Factorial',
        'date': datetime.now().isoformat(),
        'total_configs': total_configs,
        'configs_completed': len(summary),
        'configs_failed': total_configs - len(summary),
        'elapsed_time_seconds': elapsed_time,
        'elapsed_time_minutes': elapsed_time / 60,
        'parameters': {
            'economies': economies,
            'densities': densities,
            'seeds': seeds,
            'num_episodes': num_episodes
        },
        'results': summary
    }
    
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ EXPERIMENTO COMPLETADO")
    print("="*70)
    print(f"Configs ejecutadas: {len(summary)}/{total_configs}")
    print(f"Tiempo total: {elapsed_time/60:.1f} minutos")
    print(f"Resumen guardado: {summary_path}")
    print("="*70 + "\n")
    
    return summary


# ============================================================================
# MAIN: Parsear argumentos y ejecutar
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Experimento 4: Economía Factorial (PGF v7)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Ejecución completa (45 configs)
  python scripts/run_experiment_4_economia_factorial.py
  
  # Test mode (3 configs × 10 episodios)
  python scripts/run_experiment_4_economia_factorial.py --test_mode
  
  # Solo economía harsh (15 configs)
  python scripts/run_experiment_4_economia_factorial.py --economies harsh
  
  # Dos economías, 3 densidades
  python scripts/run_experiment_4_economia_factorial.py --economies harsh balanced --densities 0.10 0.20 0.30
        """
    )
    
    parser.add_argument('--economies', nargs='+', 
                       choices=['harsh', 'balanced', 'favorable'],
                       default=['harsh', 'balanced', 'favorable'],
                       help='Economías a ejecutar (default: todas)')
    
    parser.add_argument('--densities', nargs='+', type=float,
                       default=[0.05, 0.10, 0.20, 0.30, 0.40],
                       help='Spawn rates (densidades) a probar (default: 0.05-0.40)')
    
    parser.add_argument('--seeds', nargs='+', type=int,
                       default=[42, 123, 456],
                       help='Seeds para reproducibilidad (default: 42 123 456)')
    
    parser.add_argument('--episodes', type=int, default=300,
                       help='Episodios por agente (default: 300)')
    
    parser.add_argument('--output_dir', type=str, default='results/pgf_v7/resultados',
                       help='Directorio de salida (default: results/pgf_v7/resultados)')
    
    parser.add_argument('--test_mode', action='store_true',
                       help='Modo test: 3 configs × 10 episodios para validación rápida')
    
    args = parser.parse_args()
    
    # Ejecutar experimento
    summary = run_experiment(
        economies=args.economies,
        densities=args.densities,
        seeds=args.seeds,
        num_episodes=args.episodes,
        output_dir=args.output_dir,
        test_mode=args.test_mode
    )
    
    return summary


if __name__ == '__main__':
    main()
