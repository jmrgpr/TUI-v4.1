"""
Script de Ejecución - Experimento 9: Curriculum Learning para Mitigar Over-Alignment (PGF v9)
==============================================================================================

Experimento preregistrado para validar Hipótesis H9.1-H9.4:
- H9.1: Curriculum > DirectoS1 (ratio_final ≥ 0.70 vs ~0.35)
- H9.2: Degradación gradual vs súbita (pendiente uniforme, NO salto final)
- H9.3: Transfer learning efectivo (retención ≥90% entre etapas)
- H9.4: Prudencia mantenida (tripwires curriculum ≤ DirectoS1)

Diseño: 3 grupos × 3 seeds = 9 configuraciones
        - CURRICULUM: 4 etapas (s=0.0→0.25→0.5→1.0), 75 eps/etapa, transfer learning
        - DIRECTO_S1: 300 eps con s=1.0 constante (réplica v8)
        - CONTROL_S0: 300 eps con s=0.0 sin shaping (baseline funcional)

Uso:
    # Ejecución completa v9 (9 configs, ~15 min)
    python scripts/run_experiment_9_curriculum.py
    
    # Test mode (3 configs, 30 eps/config, ~2 min)
    python scripts/run_experiment_9_curriculum.py --test_mode
    
    # Solo curriculum (debugging)
    python scripts/run_experiment_9_curriculum.py --groups Curriculum
    
    # Seed específica
    python scripts/run_experiment_9_curriculum.py --seeds 42

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
Preregistro: results/pgf_v9/PREREGISTRO_v9.md v1.0 (commit 99afd68)
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
# CONFIGURACIONES PREREGISTRADAS (v9 v1.0)
# ============================================================================

# PGF Shaping Parameters (idénticos v8)
PGF_BASE_TRIPWIRE_PENALTY = 100.0
PGF_BASE_RESOURCE_BONUS = 50.0

# Economía fija (balance=5.0, idéntico v8)
BALANCED_ECONOMY = {
    'step_cost': -0.2,
    'goal_reward': 1.0,
    'balance': 5.0
}

# Grid size (4×4 preregistrado)
DEFAULT_GRID_SIZE = 4

# Spawn rate fijo (densidad moderada, óptima v8)
SPAWN_RATE = 0.25

# Grupos experimentales
GROUPS = ['Curriculum', 'DirectoS1', 'ControlS0']

# Seeds (replicación)
SEEDS = [42, 123, 456]

# Episodes
DEFAULT_EPISODES = 300
EPISODES_PER_STAGE = 75  # 4 etapas × 75 = 300 total
TEST_MODE_EPISODES = 30  # Test: 4 etapas × 7-8 eps

# Curriculum stages (preregistrado)
CURRICULUM_STAGES = [
    {'scale': 0.0,  'episodes': 75},   # Etapa 1: baseline navigation
    {'scale': 0.25, 'episodes': 75},   # Etapa 2: débil aversión riesgos
    {'scale': 0.5,  'episodes': 75},   # Etapa 3: prudencia moderada
    {'scale': 1.0,  'episodes': 75}    # Etapa 4: shaping fuerte
]


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
# ENTRENAMIENTO SINGLE EPISODE (CORE LOOP)
# ============================================================================

def train_single_episode(env, agent, shaping_scale, apply_pgf=True):
    """
    Entrena un episodio completo retornando métricas.
    
    Args:
        env: ResourceDensityEnv
        agent: DQNAgent
        shaping_scale: Escala de shaping actual (0.0-1.0)
        apply_pgf: Si aplicar PGF (True) o ser control puro (False)
    
    Returns:
        dict con métricas del episodio
    """
    actions_map = ['up', 'down', 'left', 'right']
    
    state_dict = env.reset()
    done = False
    steps = 0
    
    # Acumuladores separados (CRÍTICO v8)
    total_reward_env = 0.0
    total_reward_shaped = 0.0
    tripwires_count = 0
    resources_count = 0
    
    # Flags de muerte
    death_starvation = 0
    death_tripwire = 0
    goal_reached = False
    
    while not done:
        state_vec = np.array([v for _, v in state_dict], dtype=np.float32)
        action_idx = agent.act(state_vec)
        action = actions_map[action_idx]
        
        next_state_dict, reward, done, info = env.step(action)
        next_state_vec = np.array([v for _, v in next_state_dict], dtype=np.float32)
        
        # Acumular reward crudo
        total_reward_env += reward
        
        # Calcular train_signal (con o sin shaping)
        train_signal = reward
        if apply_pgf and shaping_scale > 0:
            penalty = -PGF_BASE_TRIPWIRE_PENALTY * shaping_scale
            bonus = PGF_BASE_RESOURCE_BONUS * shaping_scale
            
            # Tripwire penalty
            if info.get('tripwire', False):
                train_signal += penalty
                tripwires_count += 1
            
            # Resource bonus
            if info.get('resource_collected', False):
                train_signal += bonus
                resources_count += 1
        else:
            # Control: solo contar eventos sin modificar reward
            if info.get('tripwire', False):
                tripwires_count += 1
            if info.get('resource_collected', False):
                resources_count += 1
        
        # Acumular reward shaped
        total_reward_shaped += train_signal
        
        # Entrenar con señal shaped
        agent.remember(state_vec, action_idx, train_signal, next_state_vec, done)
        agent.learn()
        
        # Actualizar estado
        state_dict = next_state_dict
        steps += 1
        
        # Detectar causas de muerte
        if done:
            if info.get('starvation', False):
                death_starvation = 1
            if info.get('tripwire_death', False):
                death_tripwire = 1
            if info.get('goal_reached', False):
                goal_reached = True
    
    return {
        'total_reward_env': total_reward_env,
        'total_reward_shaped': total_reward_shaped,
        'tripwires_triggered': tripwires_count,
        'resources_collected': resources_count,
        'steps_to_goal': steps,
        'goal_reached': goal_reached,
        'deaths_starvation': death_starvation,
        'deaths_tripwire': death_tripwire,
        'epsilon': agent.epsilon
    }


# ============================================================================
# TRAINING FUNCTIONS POR GRUPO
# ============================================================================

def train_curriculum(env, agent, config, verbose_freq=25):
    """
    Entrena agente con curriculum learning (4 etapas secuenciales).
    
    CRÍTICO: Transfer learning implementado:
    - Pesos Q-network se preservan entre etapas
    - Epsilon continúa decrecimiento lineal (NO reinicia)
    - Replay buffer se mantiene (experiencia acumulativa)
    
    Args:
        env: ResourceDensityEnv
        agent: DQNAgent (inicializado)
        config: Dict con configuración
        verbose_freq: Frecuencia de logging
    
    Returns:
        episode_data: Lista de dicts con métricas por episodio
    """
    episode_data = []
    global_episode = 0
    
    # Determinar duración etapas (test mode ajusta)
    stages = []
    cumulative_eps = 0
    for stage_config in CURRICULUM_STAGES:
        stage_eps = stage_config['episodes']
        if config.get('test_mode', False):
            # En test mode: ~7-8 eps por etapa
            stage_eps = config['episodes'] // 4
        
        stages.append({
            'scale': stage_config['scale'],
            'start_ep': cumulative_eps,
            'end_ep': cumulative_eps + stage_eps,
            'episodes': stage_eps
        })
        cumulative_eps += stage_eps
    
    # Entrenar por etapas
    for stage_idx, stage in enumerate(stages, 1):
        print(f"\n    🔄 ETAPA {stage_idx}/4: s={stage['scale']} "
              f"(eps {stage['start_ep']}-{stage['end_ep']})")
        
        for ep in range(stage['start_ep'], stage['end_ep']):
            metrics = train_single_episode(
                env, agent, 
                shaping_scale=stage['scale'], 
                apply_pgf=True
            )
            
            # Agregar metadata
            episode_data.append({
                'episode': ep + 1,
                'stage': stage_idx,
                'shaping_scale_current': stage['scale'],
                'agent_type': 'Curriculum',
                **metrics,
                'spawn_rate': config['spawn_rate'],
                'seed': config['seed'],
                'grid_size': config.get('grid_size', DEFAULT_GRID_SIZE)
            })
            
            global_episode = ep + 1
            
            # Logging
            if global_episode % verbose_freq == 0:
                print(f"      [Curriculum] Ep {global_episode} | "
                      f"Stage {stage_idx} (s={stage['scale']}) | "
                      f"Reward_env: {metrics['total_reward_env']:.1f} | "
                      f"Tripwires: {metrics['tripwires_triggered']} | "
                      f"ε: {metrics['epsilon']:.3f}")
    
    return episode_data


def train_direct_s1(env, agent, config, verbose_freq=50):
    """
    Entrena agente con shaping s=1.0 constante (réplica v8 directo).
    
    Args:
        env: ResourceDensityEnv
        agent: DQNAgent (inicializado)
        config: Dict con configuración
        verbose_freq: Frecuencia de logging
    
    Returns:
        episode_data: Lista de dicts con métricas por episodio
    """
    episode_data = []
    num_episodes = config['episodes']
    
    print(f"\n    ⚡ DIRECTO S=1.0 (réplica v8): {num_episodes} episodios")
    
    for ep in range(num_episodes):
        metrics = train_single_episode(
            env, agent, 
            shaping_scale=1.0, 
            apply_pgf=True
        )
        
        # Agregar metadata (sin stage, shaping constante)
        episode_data.append({
            'episode': ep + 1,
            'stage': np.nan,  # No aplica
            'shaping_scale_current': 1.0,
            'agent_type': 'DirectoS1',
            **metrics,
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'grid_size': config.get('grid_size', DEFAULT_GRID_SIZE)
        })
        
        # Logging
        if (ep + 1) % verbose_freq == 0:
            print(f"      [DirectoS1] Ep {ep+1}/{num_episodes} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | "
                  f"ε: {metrics['epsilon']:.3f}")
    
    return episode_data


def train_control_s0(env, agent, config, verbose_freq=50):
    """
    Entrena agente sin shaping (s=0.0, baseline funcional).
    
    Args:
        env: ResourceDensityEnv
        agent: DQNAgent (inicializado)
        config: Dict con configuración
        verbose_freq: Frecuencia de logging
    
    Returns:
        episode_data: Lista de dicts con métricas por episodio
    """
    episode_data = []
    num_episodes = config['episodes']
    
    print(f"\n    🔵 CONTROL S=0.0 (sin shaping): {num_episodes} episodios")
    
    for ep in range(num_episodes):
        metrics = train_single_episode(
            env, agent, 
            shaping_scale=0.0, 
            apply_pgf=False  # Control puro
        )
        
        # Agregar metadata
        episode_data.append({
            'episode': ep + 1,
            'stage': np.nan,
            'shaping_scale_current': 0.0,
            'agent_type': 'ControlS0',
            **metrics,
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'grid_size': config.get('grid_size', DEFAULT_GRID_SIZE)
        })
        
        # Logging
        if (ep + 1) % verbose_freq == 0:
            print(f"      [ControlS0] Ep {ep+1}/{num_episodes} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | "
                  f"ε: {metrics['epsilon']:.3f}")
    
    return episode_data


# ============================================================================
# VALIDACIÓN CSV (v9 EXTENDIDO)
# ============================================================================

def validate_csv_output(csv_path, expected_group):
    """
    Valida que CSV contenga todas las columnas críticas v9 (incluye stage).
    
    Args:
        csv_path: Path al CSV
        expected_group: 'Curriculum', 'DirectoS1', o 'ControlS0'
    """
    df = pd.read_csv(csv_path)
    
    required_columns = [
        'episode', 'stage', 'shaping_scale_current', 'agent_type',
        'total_reward_env', 'total_reward_shaped',
        'tripwires_triggered', 'resources_collected',
        'steps_to_goal', 'goal_reached',
        'deaths_starvation', 'deaths_tripwire',
        'epsilon', 'spawn_rate', 'seed', 'grid_size'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV inválido: faltan columnas {missing}")
    
    # Validar tipos
    if not np.issubdtype(df['tripwires_triggered'].dtype, np.integer):
        raise TypeError("tripwires_triggered debe ser entero")
    
    if not np.issubdtype(df['episode'].dtype, np.integer):
        raise TypeError("episode debe ser entero")
    
    # Validar agent_type consistente
    unique_types = df['agent_type'].unique()
    if len(unique_types) != 1 or unique_types[0] != expected_group:
        raise ValueError(f"agent_type inconsistente: esperado {expected_group}, encontrado {unique_types}")
    
    # Validar stage solo para Curriculum
    if expected_group == 'Curriculum':
        if df['stage'].isna().all():
            raise ValueError("Curriculum debe tener stage definido (no todo NaN)")
        
        # Verificar que hay 4 etapas
        stages_present = df['stage'].dropna().unique()
        if len(stages_present) != 4:
            raise ValueError(f"Curriculum debe tener 4 etapas, encontradas {len(stages_present)}")
    
    print(f"    ✓ CSV validado: {len(df)} filas, {len(required_columns)} columnas críticas OK")
    return True


# ============================================================================
# EJECUCIÓN DE UNA CONFIGURACIÓN
# ============================================================================

def run_config(config, output_dir, verbose=True):
    """
    Ejecuta una configuración completa (un grupo con una seed).
    
    Args:
        config: Dict con group, seed, episodes, spawn_rate, grid_size
        output_dir: Path para guardar resultados
        verbose: Si imprimir progreso
    
    Returns:
        metrics: Dict con resultados agregados
    """
    start_time = time.time()
    
    group = config['group']
    seed = config['seed']
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"CONFIG: group={group}, seed={seed}, episodes={config['episodes']}")
        print(f"{'='*70}")
    
    # Configurar semilla
    configure_all_seeds(seed)
    
    # Crear entorno con tripwires fijos (CRÍTICO: reproducibilidad)
    grid_size = config.get('grid_size', DEFAULT_GRID_SIZE)
    num_tripwires = max(1, int(grid_size * grid_size * config['spawn_rate']))
    
    available_cells = [(x, y) for x in range(grid_size) for y in range(grid_size) 
                       if not (x == 0 and y == 0) and not (x == grid_size-1 and y == grid_size-1)]
    np.random.shuffle(available_cells)
    tripwires_list = available_cells[:num_tripwires]
    
    env = ResourceDensityEnv(
        size=grid_size,
        tripwires=tripwires_list,
        resource_spawn_rate=config['spawn_rate'],
        step_cost=BALANCED_ECONOMY['step_cost'],
        resource_reward=BALANCED_ECONOMY['goal_reward']
    )
    
    state_size = len(env.reset())
    action_size = 4
    
    # Crear agente (fresh para cada config)
    agent = DQNAgent(state_size, action_size)
    
    # Entrenar según grupo
    if group == 'Curriculum':
        episode_data = train_curriculum(env, agent, config, verbose_freq=25)
    elif group == 'DirectoS1':
        episode_data = train_direct_s1(env, agent, config, verbose_freq=50)
    elif group == 'ControlS0':
        episode_data = train_control_s0(env, agent, config, verbose_freq=50)
    else:
        raise ValueError(f"Grupo desconocido: {group}")
    
    # Crear DataFrame
    df = pd.DataFrame(episode_data)
    
    # Generar nombres de archivo
    base_name = f"exp9_{group}_seed{seed}"
    csv_path = output_dir / f"{base_name}_episodes.csv"
    json_path = output_dir / f"{base_name}_metrics.json"
    
    # Guardar CSV
    df.to_csv(csv_path, index=False)
    if verbose:
        print(f"\n✓ Guardado: {csv_path.name}")
    
    # Validar CSV
    validate_csv_output(csv_path, expected_group=group)
    
    # Calcular métricas agregadas
    # Últimos 50 episodios (250-300 o equivalente en test mode)
    final_window = max(10, len(df) // 6)  # 1/6 final (50 de 300, o 5 de 30)
    df_final = df.iloc[-final_window:]
    
    stats = {
        'mean_reward_env_all': float(df['total_reward_env'].mean()),
        'std_reward_env_all': float(df['total_reward_env'].std()),
        'mean_reward_env_final': float(df_final['total_reward_env'].mean()),
        'std_reward_env_final': float(df_final['total_reward_env'].std()),
        'mean_tripwires_all': float(df['tripwires_triggered'].mean()),
        'mean_tripwires_final': float(df_final['tripwires_triggered'].mean()),
        'total_tripwires': int(df['tripwires_triggered'].sum()),
        'mean_resources_all': float(df['resources_collected'].mean()),
        'mean_steps_all': float(df['steps_to_goal'].mean()),
        'success_rate_all': float(df['goal_reached'].mean()),
        'success_rate_final': float(df_final['goal_reached'].mean()),
        'survival_rate_all': float(1 - df['deaths_starvation'].mean()),
        'final_epsilon': float(df.iloc[-1]['epsilon'])
    }
    
    # Stats específicos Curriculum
    if group == 'Curriculum':
        stage_stats = {}
        for stage_num in [1, 2, 3, 4]:
            df_stage = df[df['stage'] == stage_num]
            if len(df_stage) > 0:
                stage_stats[f'stage_{stage_num}'] = {
                    'mean_reward_env': float(df_stage['total_reward_env'].mean()),
                    'mean_tripwires': float(df_stage['tripwires_triggered'].mean()),
                    'success_rate': float(df_stage['goal_reached'].mean())
                }
        
        stats['by_stage'] = stage_stats
    
    # Guardar JSON con metadatos completos
    metrics = {
        'config': {
            'group': group,
            'seed': seed,
            'episodes': config['episodes'],
            'spawn_rate': config['spawn_rate'],
            'grid_size': grid_size,
            'balance': BALANCED_ECONOMY['balance'],
            'pgf_base_tripwire_penalty': PGF_BASE_TRIPWIRE_PENALTY,
            'pgf_base_resource_bonus': PGF_BASE_RESOURCE_BONUS,
            'curriculum_stages': CURRICULUM_STAGES if group == 'Curriculum' else None
        },
        'stats': stats,
        'timestamp': datetime.now().isoformat(),
        'duration_minutes': (time.time() - start_time) / 60
    }
    
    with open(json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    if verbose:
        print(f"✓ Guardado: {json_path.name}")
        print(f"\n📊 RESULTADOS {group}:")
        print(f"   Reward env (final): {stats['mean_reward_env_final']:.2f} ± {stats['std_reward_env_final']:.2f}")
        print(f"   Success rate (final): {stats['success_rate_final']:.2%}")
        print(f"   Tripwires (mean): {stats['mean_tripwires_all']:.2f}")
        print(f"   Duración: {metrics['duration_minutes']:.2f} min")
        
        if group == 'Curriculum':
            print(f"\n   📈 Por etapa (reward_env):")
            for stage_num in [1, 2, 3, 4]:
                if f'stage_{stage_num}' in stats['by_stage']:
                    stage_data = stats['by_stage'][f'stage_{stage_num}']
                    print(f"      Etapa {stage_num}: {stage_data['mean_reward_env']:.2f}")
    
    return metrics


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Experimento 9: Curriculum Learning para Mitigar Over-Alignment (v9)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # v9 completo preregistrado (9 configs)
  python scripts/run_experiment_9_curriculum.py
  
  # Test mode (3 configs con 30 eps cada una)
  python scripts/run_experiment_9_curriculum.py --test_mode
  
  # Solo curriculum (debugging)
  python scripts/run_experiment_9_curriculum.py --groups Curriculum
  
  # Seed específica
  python scripts/run_experiment_9_curriculum.py --seeds 42
        """
    )
    
    parser.add_argument('--test_mode', action='store_true',
                        help='Ejecutar solo 3 configs con 30 episodios (validación rápida)')
    parser.add_argument('--groups', nargs='+', choices=GROUPS,
                        help='Grupos a ejecutar (default: todos)')
    parser.add_argument('--seeds', nargs='+', type=int,
                        help='Seeds a ejecutar (default: todos)')
    parser.add_argument('--episodes', type=int,
                        help='Episodios totales (default: 300, test_mode: 30)')
    parser.add_argument('--grid_size', type=int, default=DEFAULT_GRID_SIZE,
                        help='Tamaño del grid (default: 4)')
    
    args = parser.parse_args()
    
    # Determinar parámetros
    if args.test_mode:
        groups = ['Curriculum', 'DirectoS1', 'ControlS0']
        seeds = [42]
        episodes = TEST_MODE_EPISODES
        print("\n🧪 MODO TEST: 3 configs × 30 episodios (~2 min)")
    else:
        groups = args.groups or GROUPS
        seeds = args.seeds or SEEDS
        episodes = args.episodes or DEFAULT_EPISODES
        print("\n📋 MODO CONFIRMATORIO: 9 configs × 300 episodios (~15 min)")
    
    grid_size = args.grid_size
    
    # Output directory
    output_dir = Path('results/pgf_v9/resultados')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar configuraciones
    configs = []
    for group in groups:
        for seed in seeds:
            configs.append({
                'group': group,
                'seed': seed,
                'episodes': episodes,
                'spawn_rate': SPAWN_RATE,
                'grid_size': grid_size,
                'test_mode': args.test_mode
            })
    
    print(f"\n📊 EXPERIMENTO v9: {len(configs)} configuraciones")
    print(f"   Grupos: {groups}")
    print(f"   Seeds: {seeds}")
    print(f"   Episodios: {episodes} por config")
    print(f"   Grid: {grid_size}×{grid_size}")
    print(f"   Spawn rate: {SPAWN_RATE}")
    
    if args.test_mode:
        print(f"   Tiempo estimado: ~2 minutos")
    else:
        print(f"   Tiempo estimado: ~{len(configs) * 1.5:.0f} minutos")
    
    # Ejecutar todas las configuraciones
    all_metrics = []
    start_time = time.time()
    
    for i, config in enumerate(configs, 1):
        print(f"\n\n🔄 CONFIG {i}/{len(configs)}")
        metrics = run_config(config, output_dir, verbose=True)
        all_metrics.append(metrics)
        
        # Checkpoint cada 3 configs
        if i % 3 == 0 and i < len(configs):
            elapsed = (time.time() - start_time) / 60
            remaining = (len(configs) - i) * (elapsed / i)
            print(f"\n⏱️  CHECKPOINT: {i}/{len(configs)} completo ({elapsed:.1f} min, ~{remaining:.1f} min restantes)")
    
    # Resumen final
    total_time = (time.time() - start_time) / 60
    print(f"\n\n{'='*70}")
    print(f"✅ EXPERIMENTO v9 COMPLETADO")
    print(f"{'='*70}")
    print(f"   Configs ejecutadas: {len(configs)}")
    print(f"   Tiempo total: {total_time:.1f} min")
    print(f"   Output directory: {output_dir}")
    print(f"\n📁 Archivos generados:")
    print(f"   {len(configs)} × CSV (episodes)")
    print(f"   {len(configs)} × JSON (metrics)")
    
    # Resumen por grupo (solo si ejecución completa)
    if not args.test_mode and len(groups) == 3:
        print(f"\n📊 RESUMEN POR GRUPO (reward_env final):")
        for group in GROUPS:
            configs_group = [m for m in all_metrics if m['config']['group'] == group]
            if configs_group:
                rewards = [m['stats']['mean_reward_env_final'] for m in configs_group]
                print(f"   {group:12s}: {np.mean(rewards):6.2f} ± {np.std(rewards):5.2f} (N={len(rewards)})")
        
        # Quick check H9.1
        curriculum_rewards = [m['stats']['mean_reward_env_final'] for m in all_metrics if m['config']['group'] == 'Curriculum']
        directo_rewards = [m['stats']['mean_reward_env_final'] for m in all_metrics if m['config']['group'] == 'DirectoS1']
        control_rewards = [m['stats']['mean_reward_env_final'] for m in all_metrics if m['config']['group'] == 'ControlS0']
        
        if curriculum_rewards and control_rewards:
            ratio_curriculum = np.mean(curriculum_rewards) / np.mean(control_rewards)
            ratio_directo = np.mean(directo_rewards) / np.mean(control_rewards) if directo_rewards else 0
            
            print(f"\n🎯 QUICK CHECK H9.1:")
            print(f"   Ratio Curriculum/Control: {ratio_curriculum:.3f}")
            print(f"   Ratio DirectoS1/Control:  {ratio_directo:.3f}")
            
            if ratio_curriculum >= 0.70:
                print(f"   ✅ H9.1 preliminar: Curriculum ≥ 0.70 (ÉXITO)")
            elif ratio_curriculum > ratio_directo:
                print(f"   ⚠️  H9.1 intermedio: Curriculum > Directo pero < 0.70")
            else:
                print(f"   ❌ H9.1 preliminar: Curriculum NO supera Directo")
    
    print(f"\n🎯 Próximo paso: Análisis estadístico completo")
    print(f"   python scripts/analyze_curriculum_effectiveness.py")
    print(f"   python scripts/analyze_temporal_stages.py")


if __name__ == '__main__':
    main()
