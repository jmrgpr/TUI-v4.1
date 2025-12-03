"""
Script de Ejecución - Experimento 8: Intensidad de Shaping (PGF v8)
====================================================================

Experimento preregistrado para validar Hipótesis H8.1-H8.3:
- H8.1: Umbral de intensidad s* ∈ [0.5, 1.0] donde shaping diverge conductas
- H8.2: Amplificación por densidad moderada (spawn=0.25 > spawn=0.40)
- H8.3: Control negativo (s=0.0 → paridad PGF/Control)

Diseño: 4 shaping × 2 densidades × 3 seeds = 24 configuraciones (v8.0)
        + opcional: 6 configs 6×6 exploratorias (v8.0b hedge)

Uso:
    # Ejecución completa v8.0 (24 configs 4×4, ~12 min)
    python scripts/run_experiment_8_shaping_intensity.py
    
    # Test mode (3 configs, 10 eps, ~2 min)
    python scripts/run_experiment_8_shaping_intensity.py --test_mode
    
    # Hedge exploratorio 6×6 (6 configs, ~90 min)
    python scripts/run_experiment_8_shaping_intensity.py --grid_size 6 --episodes 100 --seeds 42
    
    # Bloque específico shaping
    python scripts/run_experiment_8_shaping_intensity.py --shaping_scales 0.0 1.0

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
Preregistro: results/pgf_v8/PREREGISTRO_v8.md v1.3 (commit TBD)
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
# CONFIGURACIONES PREREGISTRADAS (v8 v1.3)
# ============================================================================

# PGF Shaping Parameters (5× más fuerte que v7)
PGF_BASE_TRIPWIRE_PENALTY = 100.0  # vs -20 en v7
PGF_BASE_RESOURCE_BONUS = 50.0     # vs +2 en v7

# Economía fija (balance=5.0, threshold detectado en v7)
BALANCED_ECONOMY = {
    'step_cost': -0.2,
    'goal_reward': 1.0,
    'balance': 5.0
}

# Shaping scales (principal IV)
SHAPING_SCALES = [0.0, 0.25, 0.5, 1.0]

# Densidades (moderador, v1.3: eliminado 0.10 por laberinto trivial)
SPAWN_RATES = [0.25, 0.40]

# Seeds (replicación)
SEEDS = [42, 123, 456]

# Grid size (4×4 preregistrado, 6×6 exploratorio)
DEFAULT_GRID_SIZE = 4
EXPLORATORY_GRID_SIZE = 6

# Episodes
DEFAULT_EPISODES = 300
TEST_MODE_EPISODES = 10


# ============================================================================
# SEEDING COMPLETO (v7 validated)
# ============================================================================

def configure_all_seeds(seed):
    """Configura todos los RNGs para reproducibilidad completa."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


# ============================================================================
# ENTRENAMIENTO CON MÉTRICAS DUALES (CRÍTICO v8)
# ============================================================================

def train_agent(env, agent, config, agent_type='PGF', verbose_freq=50):
    """
    Entrena un agente guardando MÉTRICAS DUALES (reward_env + reward_shaped).
    
    FIX CRÍTICO v8 (vs v7):
    - Separa total_reward_env (crudo) de total_reward_shaped (train signal)
    - Cuenta tripwires_triggered (contador, no booleano)
    - Cuenta resources_collected (contador)
    - Usa flags explícitas para causas de muerte
    
    Args:
        env: ResourceDensityEnv con size especificado
        agent: DQNAgent
        config: Dict con shaping_scale, spawn_rate, seed, etc.
        agent_type: 'PGF' o 'Control'
        verbose_freq: Frecuencia de logging
    
    Returns:
        episode_data: Lista de dicts con métricas por episodio
    """
    actions_map = ['up', 'down', 'left', 'right']
    episode_data = []
    
    # Determinar si aplicamos PGF shaping
    apply_pgf = (agent_type == 'PGF')
    shaping_scale = config['shaping_scale'] if apply_pgf else 0.0
    
    num_episodes = config['episodes']
    
    for ep in range(num_episodes):
        state_dict = env.reset()
        done = False
        steps = 0
        
        # Acumuladores separados (CRÍTICO v8)
        total_reward_env = 0.0       # Reward crudo del entorno
        total_reward_shaped = 0.0    # Train signal con shaping
        tripwires_count = 0          # Contador de tripwires pisados
        resources_count = 0          # Contador de recursos consumidos
        
        # Flags de muerte (para v8.1)
        death_starvation = 0
        death_tripwire = 0
        goal_reached = False
        
        while not done:
            state_vec = np.array([v for _, v in state_dict], dtype=np.float32)
            action_idx = agent.act(state_vec)
            action = actions_map[action_idx]
            
            next_state_dict, reward, done, info = env.step(action)
            next_state_vec = np.array([v for _, v in next_state_dict], dtype=np.float32)
            
            # Acumular reward crudo (lo que "importa al mundo")
            total_reward_env += reward
            
            # Calcular train_signal (lo que "ve" el agente)
            train_signal = reward
            if apply_pgf:
                penalty = -PGF_BASE_TRIPWIRE_PENALTY * shaping_scale
                bonus = PGF_BASE_RESOURCE_BONUS * shaping_scale
                
                # Tripwire penalty
                if info.get('tripwire', False):
                    train_signal += penalty
                    tripwires_count += 1
                
                # Resource bonus (usar flag explícita)
                if info.get('resource_collected', False):
                    train_signal += bonus
                    resources_count += 1
            else:
                # Control: solo cuenta eventos sin modificar reward
                if info.get('tripwire', False):
                    tripwires_count += 1
                if info.get('resource_collected', False):
                    resources_count += 1
            
            # Acumular reward shaped
            total_reward_shaped += train_signal
            
            # Entrenar con señal shaped
            agent.remember(state_vec, action_idx, train_signal, next_state_vec, done)
            agent.replay()
            
            # Actualizar estado
            state_dict = next_state_dict
            steps += 1
            
            # Detectar causas de muerte (para v8.1)
            if done:
                if info.get('starvation', False):
                    death_starvation = 1
                if info.get('tripwire_death', False):
                    death_tripwire = 1
                if info.get('goal_reached', False):
                    goal_reached = True
        
        # Guardar episodio con TODAS las métricas
        episode_data.append({
            'episode': ep + 1,
            'agent_type': agent_type,
            'total_reward_env': total_reward_env,           # CRÍTICO
            'total_reward_shaped': total_reward_shaped,     # CRÍTICO
            'tripwires_triggered': tripwires_count,         # CRÍTICO (contador)
            'resources_collected': resources_count,         # CRÍTICO (contador)
            'steps_to_goal': steps,
            'goal_reached': goal_reached,
            'deaths_starvation': death_starvation,
            'deaths_tripwire': death_tripwire,
            'epsilon': agent.epsilon,
            # Metadata para análisis robusto
            'shaping_scale': shaping_scale,
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'grid_size': config.get('grid_size', DEFAULT_GRID_SIZE)
        })
        
        # Logging
        if (ep + 1) % verbose_freq == 0:
            print(f"    [{agent_type}] Ep {ep+1}/{num_episodes} | "
                  f"Reward_env: {total_reward_env:.1f} | "
                  f"Reward_shaped: {total_reward_shaped:.1f} | "
                  f"Tripwires: {tripwires_count} | "
                  f"Steps: {steps} | ε: {agent.epsilon:.3f}")
    
    return episode_data


# ============================================================================
# VALIDACIÓN CSV (v8 OBLIGATORIA)
# ============================================================================

def validate_csv_output(csv_path):
    """
    Valida que CSV contenga todas las columnas críticas con dtypes correctos.
    
    FIX v8: Validación robusta con subtipos de integer (pandas flexibility)
    """
    df = pd.read_csv(csv_path)
    
    required_columns = [
        'episode', 'agent_type',
        'total_reward_env',       # CRÍTICO
        'total_reward_shaped',    # CRÍTICO
        'tripwires_triggered',    # CRÍTICO
        'resources_collected',    # CRÍTICO
        'steps_to_goal',
        'goal_reached',
        'deaths_starvation',
        'deaths_tripwire',
        'epsilon',
        'shaping_scale',
        'spawn_rate',
        'seed',
        'grid_size'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV inválido: faltan columnas {missing}")
    
    # Validar tipos (flexible con subtipos de integer)
    if not np.issubdtype(df['tripwires_triggered'].dtype, np.integer):
        raise TypeError("tripwires_triggered debe ser entero")
    
    if not np.issubdtype(df['resources_collected'].dtype, np.integer):
        raise TypeError("resources_collected debe ser entero")
    
    if not np.issubdtype(df['episode'].dtype, np.integer):
        raise TypeError("episode debe ser entero")
    
    # goal_reached puede ser bool o int 0/1
    if df['goal_reached'].dtype not in [bool, np.bool_, int, np.int64, np.int32]:
        raise TypeError("goal_reached debe ser bool o int")
    
    print(f"    ✓ CSV validado: {len(df)} filas, {len(required_columns)} columnas críticas OK")
    return True


# ============================================================================
# EJECUCIÓN DE UNA CONFIGURACIÓN
# ============================================================================

def run_config(config, output_dir, verbose=True):
    """
    Ejecuta una configuración completa (PGF + Control).
    
    Args:
        config: Dict con shaping_scale, spawn_rate, seed, episodes, grid_size
        output_dir: Path para guardar resultados
        verbose: Si imprimir progreso
    
    Returns:
        metrics: Dict con resultados agregados
    """
    start_time = time.time()
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"CONFIG: shaping={config['shaping_scale']}, spawn={config['spawn_rate']}, "
              f"seed={config['seed']}, grid={config.get('grid_size', 4)}")
        print(f"{'='*70}")
    
    # Configurar semilla
    configure_all_seeds(config['seed'])
    
    # Crear entorno con grid_size especificado
    grid_size = config.get('grid_size', DEFAULT_GRID_SIZE)
    env = ResourceDensityEnv(
        size=grid_size,
        spawn_rate=config['spawn_rate'],
        step_cost=BALANCED_ECONOMY['step_cost'],
        goal_reward=BALANCED_ECONOMY['goal_reward']
    )
    
    state_size = len(env.reset())
    action_size = 4
    
    # Entrenar PGF
    if verbose:
        print("\n[1/2] Entrenando agente PGF...")
    pgf_agent = DQNAgent(state_size, action_size)
    pgf_data = train_agent(env, pgf_agent, config, agent_type='PGF', verbose_freq=50)
    
    # Re-configurar semilla para Control (mismo entorno, diferente política)
    configure_all_seeds(config['seed'])
    env = ResourceDensityEnv(
        size=grid_size,
        spawn_rate=config['spawn_rate'],
        step_cost=BALANCED_ECONOMY['step_cost'],
        goal_reward=BALANCED_ECONOMY['goal_reward']
    )
    
    # Entrenar Control
    if verbose:
        print("\n[2/2] Entrenando agente Control...")
    control_agent = DQNAgent(state_size, action_size)
    control_data = train_agent(env, control_agent, config, agent_type='Control', verbose_freq=50)
    
    # Combinar datos
    all_data = pgf_data + control_data
    df = pd.DataFrame(all_data)
    
    # Generar nombres de archivo
    grid_suffix = f"_{grid_size}x{grid_size}" if grid_size != 4 else ""
    base_name = f"exp8{grid_suffix}_shaping{config['shaping_scale']}_spawn{config['spawn_rate']}_seed{config['seed']}"
    csv_path = output_dir / f"{base_name}_episodes.csv"
    json_path = output_dir / f"{base_name}_metrics.json"
    
    # Guardar CSV
    df.to_csv(csv_path, index=False)
    if verbose:
        print(f"\n✓ Guardado: {csv_path.name}")
    
    # Validar CSV
    validate_csv_output(csv_path)
    
    # Calcular métricas agregadas
    pgf_df = df[df['agent_type'] == 'PGF']
    control_df = df[df['agent_type'] == 'Control']
    
    pgf_stats = {
        'mean_reward_env': float(pgf_df['total_reward_env'].mean()),
        'std_reward_env': float(pgf_df['total_reward_env'].std()),
        'mean_reward_shaped': float(pgf_df['total_reward_shaped'].mean()),
        'std_reward_shaped': float(pgf_df['total_reward_shaped'].std()),
        'mean_tripwires': float(pgf_df['tripwires_triggered'].mean()),
        'total_tripwires': int(pgf_df['tripwires_triggered'].sum()),
        'mean_resources': float(pgf_df['resources_collected'].mean()),
        'mean_steps': float(pgf_df['steps_to_goal'].mean()),
        'success_rate': float(pgf_df['goal_reached'].mean()),
        'survival_rate': float(1 - pgf_df['deaths_starvation'].mean())
    }
    
    control_stats = {
        'mean_reward_env': float(control_df['total_reward_env'].mean()),
        'std_reward_env': float(control_df['total_reward_env'].std()),
        'mean_reward_shaped': float(control_df['total_reward_shaped'].mean()),
        'std_reward_shaped': float(control_df['total_reward_shaped'].std()),
        'mean_tripwires': float(control_df['tripwires_triggered'].mean()),
        'total_tripwires': int(control_df['tripwires_triggered'].sum()),
        'mean_resources': float(control_df['resources_collected'].mean()),
        'mean_steps': float(control_df['steps_to_goal'].mean()),
        'success_rate': float(control_df['goal_reached'].mean()),
        'survival_rate': float(1 - control_df['deaths_starvation'].mean())
    }
    
    # Calcular ratios (con protección división por cero)
    ratios = {
        'reward_env': pgf_stats['mean_reward_env'] / control_stats['mean_reward_env'] if control_stats['mean_reward_env'] != 0 else np.nan,
        'reward_shaped': pgf_stats['mean_reward_shaped'] / control_stats['mean_reward_shaped'] if control_stats['mean_reward_shaped'] != 0 else np.nan,
        'tripwires': pgf_stats['mean_tripwires'] / control_stats['mean_tripwires'] if control_stats['mean_tripwires'] != 0 else np.nan,
        'resources': pgf_stats['mean_resources'] / control_stats['mean_resources'] if control_stats['mean_resources'] != 0 else np.nan,
        'steps': pgf_stats['mean_steps'] / control_stats['mean_steps'] if control_stats['mean_steps'] != 0 else np.nan
    }
    
    # Guardar JSON con metadatos completos
    metrics = {
        'config': {
            'shaping_scale': config['shaping_scale'],
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'balance': BALANCED_ECONOMY['balance'],
            'tripwire_fatal': False,  # v8.0, cambia en v8.1
            'pgf_base_tripwire_penalty': PGF_BASE_TRIPWIRE_PENALTY,
            'pgf_base_resource_bonus': PGF_BASE_RESOURCE_BONUS,
            'episodes': config['episodes'],
            'grid_size': grid_size
        },
        'pgf_stats': pgf_stats,
        'control_stats': control_stats,
        'ratios': ratios,
        'timestamp': datetime.now().isoformat(),
        'duration_minutes': (time.time() - start_time) / 60
    }
    
    with open(json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    if verbose:
        print(f"✓ Guardado: {json_path.name}")
        print(f"\n📊 RESULTADOS:")
        print(f"   Ratio reward_env:    {ratios['reward_env']:.3f}")
        print(f"   Ratio reward_shaped: {ratios['reward_shaped']:.3f}")
        print(f"   Ratio tripwires:     {ratios['tripwires']:.3f}")
        print(f"   Duración: {metrics['duration_minutes']:.2f} min")
    
    return metrics


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Experimento 8: Intensidad de Shaping (v8)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # v8.0 completo preregistrado (24 configs 4×4)
  python scripts/run_experiment_8_shaping_intensity.py
  
  # Test mode (3 configs rápidas)
  python scripts/run_experiment_8_shaping_intensity.py --test_mode
  
  # Hedge exploratorio 6×6 (6 configs)
  python scripts/run_experiment_8_shaping_intensity.py --grid_size 6 --episodes 100 --seeds 42
  
  # Solo shaping fuerte
  python scripts/run_experiment_8_shaping_intensity.py --shaping_scales 1.0
        """
    )
    
    parser.add_argument('--test_mode', action='store_true',
                        help='Ejecutar solo 3 configs con 10 episodios (validación rápida)')
    parser.add_argument('--shaping_scales', nargs='+', type=float,
                        help='Shaping scales a ejecutar (default: todos)')
    parser.add_argument('--spawn_rates', nargs='+', type=float,
                        help='Spawn rates a ejecutar (default: todos)')
    parser.add_argument('--seeds', nargs='+', type=int,
                        help='Seeds a ejecutar (default: todos)')
    parser.add_argument('--episodes', type=int,
                        help='Episodios por agente (default: 300, test_mode: 10)')
    parser.add_argument('--grid_size', type=int, choices=[4, 6],
                        help='Tamaño del grid (4 preregistrado, 6 exploratorio)')
    
    args = parser.parse_args()
    
    # Determinar parámetros
    if args.test_mode:
        shaping_scales = [0.0, 0.5, 1.0]
        spawn_rates = [0.25]
        seeds = [42]
        episodes = TEST_MODE_EPISODES
        print("\n🧪 MODO TEST: 3 configs × 10 episodios")
    else:
        shaping_scales = args.shaping_scales or SHAPING_SCALES
        spawn_rates = args.spawn_rates or SPAWN_RATES
        seeds = args.seeds or SEEDS
        episodes = args.episodes or DEFAULT_EPISODES
    
    grid_size = args.grid_size or DEFAULT_GRID_SIZE
    
    # Determinar directorio de salida
    if grid_size == 6:
        output_dir = Path('results/pgf_v8/exploratorio_6x6')
        print("\n🔬 MODO EXPLORATORIO 6×6 (NO PREREGISTRADO)")
    else:
        output_dir = Path('results/pgf_v8/resultados')
        print("\n📋 MODO CONFIRMATORIO 4×4 (PREREGISTRADO v1.3)")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar configuraciones
    configs = []
    for shaping in shaping_scales:
        for spawn in spawn_rates:
            for seed in seeds:
                configs.append({
                    'shaping_scale': shaping,
                    'spawn_rate': spawn,
                    'seed': seed,
                    'episodes': episodes,
                    'grid_size': grid_size
                })
    
    print(f"\n📊 EXPERIMENTO v8: {len(configs)} configuraciones")
    print(f"   Shaping scales: {shaping_scales}")
    print(f"   Spawn rates: {spawn_rates}")
    print(f"   Seeds: {seeds}")
    print(f"   Episodios: {episodes} por agente")
    print(f"   Grid: {grid_size}×{grid_size}")
    print(f"   Tiempo estimado: {len(configs) * episodes * 2 / 600:.1f} min")
    
    # Ejecutar todas las configuraciones
    all_metrics = []
    start_time = time.time()
    
    for i, config in enumerate(configs, 1):
        print(f"\n\n🔄 CONFIG {i}/{len(configs)}")
        metrics = run_config(config, output_dir, verbose=True)
        all_metrics.append(metrics)
        
        # Checkpoint cada 6 configs
        if i % 6 == 0:
            elapsed = (time.time() - start_time) / 60
            remaining = (len(configs) - i) * (elapsed / i)
            print(f"\n⏱️  CHECKPOINT: {i}/{len(configs)} completo ({elapsed:.1f} min, ~{remaining:.1f} min restantes)")
    
    # Resumen final
    total_time = (time.time() - start_time) / 60
    print(f"\n\n{'='*70}")
    print(f"✅ EXPERIMENTO COMPLETADO")
    print(f"{'='*70}")
    print(f"   Configs ejecutadas: {len(configs)}")
    print(f"   Tiempo total: {total_time:.1f} min")
    print(f"   Output directory: {output_dir}")
    print(f"\n📁 Archivos generados:")
    print(f"   {len(configs)} × CSV (episodes)")
    print(f"   {len(configs)} × JSON (metrics)")
    
    # Resumen de ratios
    print(f"\n📊 RESUMEN DE RATIOS (reward_env):")
    for shaping in sorted(set(c['shaping_scale'] for c in configs)):
        configs_shaping = [m for m in all_metrics if m['config']['shaping_scale'] == shaping]
        ratios = [m['ratios']['reward_env'] for m in configs_shaping if not np.isnan(m['ratios']['reward_env'])]
        if ratios:
            print(f"   s={shaping}: {np.mean(ratios):.3f} ± {np.std(ratios):.3f} (N={len(ratios)})")
    
    print(f"\n🎯 Próximo paso: Análisis estadístico")
    print(f"   python scripts/analyze_experiment_8.py")


if __name__ == '__main__':
    main()
