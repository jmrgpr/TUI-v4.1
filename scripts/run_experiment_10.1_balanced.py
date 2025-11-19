"""
Script de Ejecución - Experimento 10.1: Adaptive Curriculum 8×8 Economía Calibrada
===================================================================================

Experimento preregistrado para validar Hipótesis H10.1.1-H10.4.1:
- H10.1.1: Adaptive alcanza ratio ≥ 0.70 vs Control (reintroducir presión)
- H10.2.1: Adaptive > Fixed (curriculum threshold-based superior)
- H10.3.1: Adaptive reduce varianza inter-seed (CV_ratio < 0.80)
- H10.4.1: Seeds vulnerables mantienen ≥60% success

CAMBIOS vs v10 (8.0 trivial):
    - INITIAL_BALANCE: 8.0 → 5.0 (margen 470% → 257%)
    - N seeds: 5 → 8 (potencia 45% → 65%)
    - Output: results/pgf_v10.1/ (NO sobrescribir v10)

MOTIVACIÓN:
    v10 con balance=8.0 resultó trivial (todas 100% success, ratio 0.995).
    v10.1 reintroduce presión económica usando balance=5.0 (mismo v9.1 exitoso 4×4).

Diseño: 3 grupos × 8 seeds = 24 configuraciones
        - ADAPTIVE: Curriculum threshold-based (success>0.60, timeout 150 eps/etapa)
        - FIXED: Curriculum rígido (100 eps/etapa, 5 etapas)
        - CONTROL_S0: 400 eps con s=0.0 sin shaping (baseline capacidad 8×8)

Uso:
    # Test mode (2 seeds × 100 eps, validación gates)
    python scripts/run_experiment_10.1_balanced.py --test_mode --seeds 42 789
    
    # Ejecución completa v10.1 (24 configs, ~10-12 horas)
    python scripts/run_experiment_10.1_balanced.py
    
    # Solo adaptive (debugging)
    python scripts/run_experiment_10.1_balanced.py --groups AdaptiveCurriculum

Autor: TUI v4.1 Research Team
Fecha: 4 diciembre 2025
Preregistro: results/pgf_v10.1/PREREGISTRO_v10.1.md v1.0 (commit c68f8dd)
Predecesor: v10 (N=5, balance=8.0, commit d520d18)
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

# Agregar directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent


# ============================================================================
# NUMPY ENCODER (para JSON serialization)
# ============================================================================

class NumpyEncoder(json.JSONEncoder):
    """Custom encoder para tipos numpy."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)


# ============================================================================
# CONFIGURACIÓN v10.1
# ============================================================================

# Grid 8×8 (mismo v10)
GRID_SIZE = 8
MANHATTAN_MAX = 14  # (0,0) → (7,7)

# Tripwires (spawn_rate escalado)
SPAWN_RATE = 0.25  # ~16 tripwires por episodio
TRIPWIRE_PENALTY = -100.0

# Balance inicial AJUSTADO v10.1 (CAMBIO CRÍTICO vs v10)
INITIAL_BALANCE = 5.0  # vs 8.0 en v10 (margen 257% vs 470%)
DECAY_RATE = 0.1

# Reward env (mismo v10)
GOAL_REWARD = +100.0
RESOURCE_REWARD = +10.0

# Curriculum v10.1 (mismo v10)
CURRICULUM_STAGES_ADAPTIVE = [0.0, 0.25, 0.5, 0.75, 1.0]  # 5 etapas
CURRICULUM_STAGES_FIXED = [
    {'scale': 0.0, 'episodes': 100},
    {'scale': 0.25, 'episodes': 100},
    {'scale': 0.5, 'episodes': 100},
    {'scale': 0.75, 'episodes': 100},
    {'scale': 1.0, 'episodes': 100}
]

# Threshold-based transitions (mismo v10)
THRESHOLD_SUCCESS = 0.60  # Avanzar si success > 60% en últimos 25 eps
WINDOW_SIZE = 25
TIMEOUT_EPISODES = 150  # Max eps/etapa antes de forzar avance

# Grupos experimentales
GROUPS = ['AdaptiveCurriculum', 'FixedCurriculum', 'ControlS0']

# Seeds v10.1 (CAMBIO vs v10: N=8 vs N=5)
SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021]

# Hiperparámetros DQN (mismos que v10)
HIDDEN_SIZE = 64
BUFFER_SIZE = 10000
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
TARGET_UPDATE = 10

# Checkpoints
CHECKPOINT_FREQ = 6  # Cada 6 configs (~2.5h)

# Output v10.1 (CAMBIO: NO sobrescribir v10)
RESULTS_DIR = Path('results/pgf_v10.1/resultados')
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# CLASE ADAPTIVECURRICULUM (idéntica v10)
# ============================================================================

class AdaptiveCurriculum:
    """
    Curriculum learning con transiciones threshold-based.
    
    Avanza a siguiente etapa SOLO si:
    - Success rate > THRESHOLD en últimos WINDOW_SIZE episodios (dominio)
    - O timeout > TIMEOUT_EPISODES (evitar estancamiento)
    
    Personalización: Seeds fuertes avanzan rápido, seeds vulnerables usan tiempo extra.
    """
    
    def __init__(self, stages=None, threshold=0.75, window_size=25, timeout=150):
        self.stages = stages if stages is not None else CURRICULUM_STAGES_ADAPTIVE
        self.threshold = threshold
        self.window_size = window_size
        self.timeout = timeout
        
        # Estado interno
        self.current_stage = 0
        self.episodes_in_stage = 0
        self.success_history = []
        self.transitions = []  # [(episode_global, stage_old, stage_new, reason)]
    
    def should_advance(self):
        """Decide si avanzar a siguiente etapa."""
        # Condición 1: Dominio demostrado (success > threshold)
        if len(self.success_history) >= self.window_size:
            recent_success = np.mean([s for s in self.success_history[-self.window_size:]])
            ready = recent_success > self.threshold
        else:
            ready = False
        
        # Condición 2: Timeout (evitar estancamiento)
        timeout_reached = self.episodes_in_stage >= self.timeout
        
        # Avanzar si cualquier condición se cumple
        return ready or timeout_reached
    
    def update(self, goal_reached, episode_global):
        """Actualizar historia tras cada episodio."""
        self.success_history.append(int(goal_reached))
        self.episodes_in_stage += 1
        
        # Intentar avanzar a siguiente etapa
        if self.should_advance() and self.current_stage < len(self.stages) - 1:
            # Determinar razón de avance
            if len(self.success_history) >= self.window_size:
                recent_success = np.mean([s for s in self.success_history[-self.window_size:]])
                reason = f"ready_success={recent_success:.2f}" if recent_success > self.threshold else "timeout"
            else:
                reason = "timeout"
            
            # Registrar transición
            old_stage = self.current_stage
            self.current_stage += 1
            self.transitions.append((episode_global, old_stage, self.current_stage, reason))
            
            print(f"    [ADAPTIVE] Avanzando stage {old_stage}→{self.current_stage} " 
                  f"(s={self.stages[old_stage]:.2f}→{self.stages[self.current_stage]:.2f}) "
                  f"tras {self.episodes_in_stage} eps ({reason})")
            
            # Reset contador etapa
            self.episodes_in_stage = 0
    
    def get_current_scale(self):
        """Devuelve escala actual de shaping."""
        return self.stages[self.current_stage]
    
    def get_stage_info(self):
        """Información actual para logging."""
        if len(self.success_history) >= self.window_size:
            recent_success = np.mean([s for s in self.success_history[-self.window_size:]])
        else:
            recent_success = np.nan
        
        return {
            'current_stage': self.current_stage,
            'current_scale': self.get_current_scale(),
            'episodes_in_stage': self.episodes_in_stage,
            'success_rate_last_25': recent_success,
            'total_transitions': len(self.transitions)
        }
    
    def is_finished(self, min_episodes_final=50):
        """Verifica si curriculum completado (última etapa + consolidación)."""
        return self.current_stage == len(self.stages) - 1 and self.episodes_in_stage >= min_episodes_final


# ============================================================================
# ENTRENAMIENTO (idéntico v10 excepto initial_balance)
# ============================================================================

def create_env_and_agent(grid_size, seed):
    """Crea entorno 8×8 y agente DQN."""
    np.random.seed(seed)
    
    # Generar tripwires aleatorios (basado en spawn_rate, escalado 8×8)
    num_tripwires = int(grid_size * grid_size * SPAWN_RATE)
    available_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                       if (i, j) != (0, 0) and (i, j) != (grid_size-1, grid_size-1)]
    np.random.shuffle(available_cells)
    tripwires_list = available_cells[:num_tripwires]
    
    # Crear entorno con ResourceDensityEnv
    # CAMBIO CRÍTICO v10.1: initial_resources=5.0 (vs 8.0 en v10)
    env = ResourceDensityEnv(
        size=grid_size,
        tripwires=tripwires_list,
        resource_spawn_rate=SPAWN_RATE,
        step_cost=-0.2,
        resource_reward=1.0,
        initial_resources=INITIAL_BALANCE  # v10.1: 5.0 (vs 8.0 v10)
    )
    
    # State size
    state_dict = env.reset()
    state_size = len(state_dict)
    action_size = 4
    
    agent = DQNAgent(
        state_size,
        action_size,
        lr=LEARNING_RATE,
        gamma=GAMMA,
        epsilon=EPSILON_START,
        epsilon_decay=EPSILON_DECAY,
        epsilon_end=EPSILON_MIN,
        batch_size=BATCH_SIZE,
        memory_size=BUFFER_SIZE,
        target_update_freq=TARGET_UPDATE,
        hidden_dim=HIDDEN_SIZE,
    )
    
    return env, agent


def train_single_episode(env, agent, shaping_scale):
    """Entrena un episodio con escala de shaping dada (compatible ResourceDensityEnv)."""
    actions_map = ['up', 'down', 'left', 'right']
    
    state_dict = env.reset()
    done = False
    steps = 0
    
    # Acumuladores
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
        
        next_state_dict, reward_env, done, info = env.step(action)
        
        # Calcular reward shaped (PGF con escala)
        reward_shaped = reward_env
        if shaping_scale > 0:
            # PGF components
            if info.get('tripwire_triggered', False):
                reward_shaped += shaping_scale * (-100.0)  # Penalty tripwire
            if info.get('resource_collected', False):
                reward_shaped += shaping_scale * 10.0  # Bonus resource
        
        next_state_vec = np.array([v for _, v in next_state_dict], dtype=np.float32)
        agent.remember(state_vec, action_idx, reward_shaped, next_state_vec, done)
        agent.learn()
        
        state_dict = next_state_dict
        steps += 1
        
        # Métricas
        total_reward_env += reward_env
        total_reward_shaped += reward_shaped
        
        if info.get('tripwire', False):
            tripwires_count += 1
        if info.get('resource_collected', False):
            resources_count += 1
        if info.get('goal_reached', False):
            goal_reached = True
        if info.get('death_starvation', False):
            death_starvation = 1
        if info.get('death_tripwire', False):
            death_tripwire = 1
    
    return {
        'total_reward_env': total_reward_env,
        'total_reward_shaped': total_reward_shaped,
        'steps_to_goal': steps,
        'goal_reached': int(goal_reached),
        'deaths_starvation': death_starvation,
        'deaths_tripwire': death_tripwire,
        'resources_collected': resources_count,
        'tripwires_triggered': tripwires_count
    }


def train_adaptive_curriculum(env, agent, config, verbose_freq=25):
    """
    Entrena con curriculum adaptativo (threshold-based).
    
    Episodios variables por seed (personalización):
    - Seeds fuertes: ~400 eps
    - Seeds vulnerables: ~500 eps (usan timeout en etapas difíciles)
    """
    seed = config['seed']
    curriculum = AdaptiveCurriculum(
        stages=CURRICULUM_STAGES_ADAPTIVE,
        threshold=THRESHOLD_SUCCESS,
        window_size=WINDOW_SIZE,
        timeout=TIMEOUT_EPISODES
    )
    
    episode_data = []
    episode_global = 0
    max_episodes = 600  # Límite superior (evita loops infinitos)
    
    print(f"    🔄 ADAPTIVE CURRICULUM: threshold={THRESHOLD_SUCCESS}, timeout={TIMEOUT_EPISODES}")
    
    while episode_global < max_episodes:
        # Scale actual
        current_scale = curriculum.get_current_scale()
        stage_info = curriculum.get_stage_info()
        
        # Entrenar episodio
        metrics = train_single_episode(env, agent, current_scale)
        
        # Logging extendido (v10.1)
        metrics['episode'] = episode_global
        metrics['shaping_scale'] = current_scale
        metrics['stage'] = stage_info['current_stage']
        metrics['episodes_in_stage'] = stage_info['episodes_in_stage']
        metrics['success_rate_last_25'] = stage_info['success_rate_last_25']
        metrics['epsilon'] = agent.epsilon
        metrics['seed'] = seed
        
        episode_data.append(metrics)
        
        # Actualizar curriculum
        curriculum.update(metrics['goal_reached'], episode_global)
        
        # Verbose
        if (episode_global + 1) % verbose_freq == 0:
            stage_str = f"Stage {stage_info['current_stage']} (s={current_scale:.2f})"
            success_str = f"SR_25={stage_info['success_rate_last_25']:.0%}" if not np.isnan(stage_info['success_rate_last_25']) else "SR_25=N/A"
            print(f"      [Adaptive] Ep {episode_global+1} | {stage_str} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | "
                  f"{success_str} | ε: {agent.epsilon:.3f}")
        
        episode_global += 1
        
        # Stop si curriculum completado
        if curriculum.is_finished(min_episodes_final=50):
            print(f"    ✓ Curriculum completado en {episode_global} episodios "
                  f"({len(curriculum.transitions)} transiciones)")
            break
    
    # Resumen transiciones
    if curriculum.transitions:
        print(f"    📊 Transiciones: {curriculum.transitions}")
    
    # Agregar flag de transición a episode_data
    transition_episodes = {t[0] for t in curriculum.transitions}
    for ep_data in episode_data:
        ep_data['transition_triggered'] = int(ep_data['episode'] in transition_episodes)
    
    return episode_data


def train_fixed_curriculum(env, agent, config, verbose_freq=25):
    """
    Entrena con curriculum fijo (100 eps/etapa, 5 etapas = 500 eps).
    
    Control para comparar vs adaptive.
    """
    seed = config['seed']
    episode_data = []
    episode_global = 0
    
    print(f"    🔄 FIXED CURRICULUM: 5 etapas × 100 eps/etapa = 500 eps")
    
    for stage_idx, stage_config in enumerate(CURRICULUM_STAGES_FIXED):
        scale = stage_config['scale']
        n_episodes = stage_config['episodes']
        
        print(f"      Stage {stage_idx} (s={scale:.2f}): eps {episode_global}-{episode_global+n_episodes-1}")
        
        for ep_in_stage in range(n_episodes):
            metrics = train_single_episode(env, agent, scale)
            
            # Logging extendido
            metrics['episode'] = episode_global
            metrics['shaping_scale'] = scale
            metrics['stage'] = stage_idx
            metrics['episodes_in_stage'] = ep_in_stage + 1
            metrics['success_rate_last_25'] = np.nan  # Fixed no usa esta métrica
            metrics['transition_triggered'] = int(ep_in_stage == n_episodes - 1)  # Última de etapa
            metrics['epsilon'] = agent.epsilon
            metrics['seed'] = seed
            
            episode_data.append(metrics)
            
            # Verbose
            if (episode_global + 1) % verbose_freq == 0:
                print(f"      [Fixed] Ep {episode_global+1} | Stage {stage_idx} (s={scale:.2f}) | "
                      f"Reward_env: {metrics['total_reward_env']:.1f} | "
                      f"Tripwires: {metrics['tripwires_triggered']} | ε: {agent.epsilon:.3f}")
            
            episode_global += 1
    
    print(f"    ✓ Fixed curriculum completado ({episode_global} episodios)")
    
    return episode_data


def train_control_s0(env, agent, config, n_episodes=400, verbose_freq=25):
    """
    Entrena sin shaping (s=0.0) durante 400 episodios.
    
    Baseline capacidad en 8×8.
    """
    seed = config['seed']
    episode_data = []
    
    print(f"    🔵 CONTROL S=0.0 (sin shaping): {n_episodes} episodios")
    
    for episode in range(n_episodes):
        metrics = train_single_episode(env, agent, shaping_scale=0.0)
        
        # Logging
        metrics['episode'] = episode
        metrics['shaping_scale'] = 0.0
        metrics['stage'] = 0
        metrics['episodes_in_stage'] = episode + 1
        metrics['success_rate_last_25'] = np.nan
        metrics['transition_triggered'] = 0
        metrics['epsilon'] = agent.epsilon
        metrics['seed'] = seed
        
        episode_data.append(metrics)
        
        # Verbose
        if (episode + 1) % verbose_freq == 0:
            print(f"      [ControlS0] Ep {episode+1}/{n_episodes} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | ε: {agent.epsilon:.3f}")
    
    return episode_data


# ============================================================================
# EJECUCIÓN CONFIG (idéntico v10 excepto filenames)
# ============================================================================

def run_config(config, output_dir, verbose=True):
    """Ejecuta una configuración (seed + grupo)."""
    group = config['group']
    seed = config['seed']
    
    print("\n" + "="*70)
    print(f"CONFIG v10.1: group={group}, seed={seed}, grid={GRID_SIZE}×{GRID_SIZE}, balance={INITIAL_BALANCE}")
    print("="*70)
    
    # Crear entorno y agente
    env, agent = create_env_and_agent(GRID_SIZE, seed)
    
    # Entrenar según grupo
    start_time = time.time()
    
    if group == 'AdaptiveCurriculum':
        episode_data = train_adaptive_curriculum(env, agent, config, verbose_freq=25)
    elif group == 'FixedCurriculum':
        episode_data = train_fixed_curriculum(env, agent, config, verbose_freq=25)
    elif group == 'ControlS0':
        episode_data = train_control_s0(env, agent, config, n_episodes=400, verbose_freq=25)
    else:
        raise ValueError(f"Grupo desconocido: {group}")
    
    duration_min = (time.time() - start_time) / 60
    
    # Convertir a DataFrame
    df = pd.DataFrame(episode_data)
    
    # Validar columnas críticas
    required_cols = [
        'episode', 'total_reward_env', 'total_reward_shaped', 'shaping_scale',
        'goal_reached', 'tripwires_triggered', 'epsilon', 'seed',
        'stage', 'episodes_in_stage', 'success_rate_last_25', 'transition_triggered'
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas faltantes en DataFrame: {missing_cols}")
    
    # Guardar CSV v10.1 (CAMBIO: exp10.1 prefix)
    csv_filename = f"exp10.1_{group}_seed{seed}_episodes.csv"
    csv_path = output_dir / csv_filename
    df.to_csv(csv_path, index=False)
    print(f"\n📁 Guardado: {csv_filename}")
    
    # Validar CSV
    print(f"    ✓ CSV validado: {len(df)} filas, {len(required_cols)} columnas críticas OK")
    
    # Guardar métricas agregadas (JSON)
    final_window = df.iloc[-50:] if len(df) >= 50 else df
    
    metrics_summary = {
        'group': group,
        'seed': seed,
        'grid_size': GRID_SIZE,
        'initial_balance': INITIAL_BALANCE,  # v10.1: documentar balance
        'n_episodes': len(df),
        'duration_min': round(duration_min, 2),
        'final_window': {
            'mean_reward_env': float(final_window['total_reward_env'].mean()),
            'std_reward_env': float(final_window['total_reward_env'].std()),
            'success_rate': float(final_window['goal_reached'].mean()),
            'mean_tripwires': float(final_window['tripwires_triggered'].mean())
        },
        'curriculum_info': None
    }
    
    # Info específica adaptive/fixed
    if group == 'AdaptiveCurriculum':
        transitions = df[df['transition_triggered'] == 1][['episode', 'stage', 'shaping_scale']].to_dict('records')
        metrics_summary['curriculum_info'] = {
            'type': 'adaptive',
            'n_transitions': len(transitions),
            'transitions': transitions,
            'episodes_per_stage': df.groupby('stage').size().to_dict()
        }
    elif group == 'FixedCurriculum':
        metrics_summary['curriculum_info'] = {
            'type': 'fixed',
            'episodes_per_stage': df.groupby('stage').size().to_dict()
        }
    
    json_filename = f"exp10.1_{group}_seed{seed}_metrics.json"
    json_path = output_dir / json_filename
    with open(json_path, 'w') as f:
        json.dump(metrics_summary, f, indent=2, cls=NumpyEncoder)
    print(f"📁 Guardado: {json_filename}")
    
    # Resumen visual
    print(f"\n📊 RESULTADOS v10.1 {group}:")
    print(f"   Reward env (final): {metrics_summary['final_window']['mean_reward_env']:.2f} ± {metrics_summary['final_window']['std_reward_env']:.2f}")
    print(f"   Success rate (final): {metrics_summary['final_window']['success_rate']:.1%}")
    print(f"   Tripwires (mean): {metrics_summary['final_window']['mean_tripwires']:.2f}")
    print(f"   N episodios: {metrics_summary['n_episodes']}")
    print(f"   Duración: {duration_min:.2f} min")
    
    return metrics_summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta experimento v10.1 completo o test mode."""
    parser = argparse.ArgumentParser(description='Experimento 10.1: Adaptive Curriculum 8×8 Balance=5.0')
    parser.add_argument('--test_mode', action='store_true', 
                        help='Modo test: 2 seeds × 100 eps (validación gates)')
    parser.add_argument('--groups', nargs='+', choices=GROUPS, default=GROUPS,
                        help='Grupos a ejecutar')
    parser.add_argument('--seeds', type=int, nargs='+', default=SEEDS,
                        help='Seeds a ejecutar')
    
    args = parser.parse_args()
    
    # Test mode: 2 seeds × 100 eps (validación gates críticos)
    if args.test_mode:
        test_seeds = args.seeds[:2] if len(args.seeds) >= 2 else [42, 789]
        print("="*70)
        print("🧪 MODO TEST v10.1: 2 seeds × 100 eps (VALIDACIÓN GATES)")
        print("="*70)
        print(f"Seeds: {test_seeds}")
        print(f"Balance: {INITIAL_BALANCE} (vs 8.0 trivial v10)")
        print(f"Episodios máx: 100 (adaptive puede terminar antes)")
        print(f"Grid: {GRID_SIZE}×{GRID_SIZE}")
        print(f"\n🚦 GATES CRÍTICOS:")
        print(f"   ✅ Control 70-90% success → PROCEDER batch completo")
        print(f"   ❌ Control >95% success → ABORTAR (aún trivial, bajar balance 4.5)")
        print(f"   ❌ Control <60% success → AJUSTAR (muy duro, subir balance 5.5-6.0)")
        
        # Ejecutar configs test (Control + Adaptive)
        test_configs = []
        for seed in test_seeds:
            test_configs.append({'group': 'ControlS0', 'seed': seed})
            test_configs.append({'group': 'AdaptiveCurriculum', 'seed': seed})
        
        # Modificar temporalmente para test (100 eps máx)
        global TIMEOUT_EPISODES
        original_timeout = TIMEOUT_EPISODES
        TIMEOUT_EPISODES = 30  # Forzar avances rápidos en test
        
        test_metrics = []
        try:
            for config in test_configs:
                metrics = run_config(config, RESULTS_DIR, verbose=True)
                test_metrics.append(metrics)
        
        finally:
            TIMEOUT_EPISODES = original_timeout
        
        # Análisis gates
        control_metrics = [m for m in test_metrics if m['group'] == 'ControlS0']
        if control_metrics:
            control_success = [m['final_window']['success_rate'] for m in control_metrics]
            mean_success = np.mean(control_success)
            
            print("\n" + "="*70)
            print("🚦 ANÁLISIS GATES (TEST MODE v10.1)")
            print("="*70)
            print(f"Control success rate (N={len(control_success)}): {mean_success:.1%}")
            
            if 0.70 <= mean_success <= 0.90:
                print(f"   ✅ GATE OK: Control en zona óptima 70-90%")
                print(f"   🟢 DECISIÓN: PROCEDER con batch completo v10.1")
            elif mean_success > 0.95:
                print(f"   ❌ GATE FALLA: Control >95% (AÚN TRIVIAL)")
                print(f"   🔴 DECISIÓN: ABORTAR v10.1, crear v10.2 con balance=4.0-4.5")
            elif mean_success > 0.90:
                print(f"   ⚠️  GATE BORDERLINE: Control 90-95% (cercano trivial)")
                print(f"   🟡 DECISIÓN: CONSIDERAR bajar balance a 4.5 (opcional)")
            elif mean_success < 0.60:
                print(f"   ❌ GATE FALLA: Control <60% (MUY DIFÍCIL)")
                print(f"   🔴 DECISIÓN: AJUSTAR balance a 5.5-6.0, repetir test")
            else:
                print(f"   ⚠️  GATE PARCIAL: Control 60-70% (al límite)")
                print(f"   🟡 DECISIÓN: PROCEDER con cautela O subir balance a 5.5")
        
        return
    
    # Modo completo v10.1
    print("="*70)
    print("EXPERIMENTO v10.1: Adaptive Curriculum 8×8 Balance=5.0")
    print("="*70)
    print(f"Cambios vs v10:")
    print(f"   Balance: 8.0 → {INITIAL_BALANCE} (margen 470% → 257%)")
    print(f"   Seeds: 5 → {len(SEEDS)} (potencia 45% → 65%)")
    print(f"Grupos: {args.groups}")
    print(f"Seeds (N={len(args.seeds)}): {args.seeds}")
    print(f"Grid: {GRID_SIZE}×{GRID_SIZE}")
    
    # Generar configs
    configs = []
    for group in args.groups:
        for seed in args.seeds:
            configs.append({'group': group, 'seed': seed})
    
    print(f"\n📊 TOTAL: {len(configs)} configuraciones")
    
    # Estimación tiempo (mismo v10)
    n_adaptive = sum(1 for c in configs if c['group'] == 'AdaptiveCurriculum')
    n_fixed = sum(1 for c in configs if c['group'] == 'FixedCurriculum')
    n_control = sum(1 for c in configs if c['group'] == 'ControlS0')
    
    total_eps = n_adaptive * 450 + n_fixed * 500 + n_control * 400
    estimated_minutes = total_eps * 0.08  # ~0.08 min/ep en 8×8
    
    print(f"   Episodios totales estimados: ~{total_eps:,}")
    print(f"   Tiempo estimado: ~{estimated_minutes:.0f} minutos (~{estimated_minutes/60:.1f} horas)")
    print(f"   Checkpoints: cada {CHECKPOINT_FREQ} configs (~{estimated_minutes/len(configs)*CHECKPOINT_FREQ:.0f} min)")
    
    # Ejecutar configs
    all_metrics = []
    start_time = time.time()
    
    for i, config in enumerate(configs, 1):
        print(f"\n\n🔄 CONFIG {i}/{len(configs)}")
        metrics = run_config(config, RESULTS_DIR, verbose=True)
        all_metrics.append(metrics)
        
        # Checkpoint
        if i % CHECKPOINT_FREQ == 0 and i < len(configs):
            elapsed = (time.time() - start_time) / 60
            remaining = (len(configs) - i) * (elapsed / i)
            print(f"\n⏱️  CHECKPOINT {i//CHECKPOINT_FREQ}: {i}/{len(configs)} completo "
                  f"({elapsed:.1f} min, ~{remaining:.1f} min restantes)")
            print(f"      Progreso: {i/len(configs)*100:.1f}% | "
                  f"Seeds procesadas: {len(set([m['seed'] for m in all_metrics]))}")
    
    # Resumen final
    total_time = (time.time() - start_time) / 60
    print("\n\n" + "="*70)
    print("✅ EXPERIMENTO v10.1 COMPLETADO")
    print("="*70)
    print(f"   Configs ejecutadas: {len(configs)}")
    print(f"   Tiempo total: {total_time:.1f} min ({total_time/60:.1f} horas)")
    print(f"   Output directory: {RESULTS_DIR}")
    
    # Resumen por grupo
    print(f"\n📊 RESUMEN POR GRUPO (reward_env final):")
    for group in args.groups:
        group_metrics = [m for m in all_metrics if m['group'] == group]
        if group_metrics:
            rewards = [m['final_window']['mean_reward_env'] for m in group_metrics]
            mean_reward = np.mean(rewards)
            std_reward = np.std(rewards, ddof=1)
            print(f"   {group:18}: {mean_reward:7.2f} ± {std_reward:5.2f} (N={len(group_metrics)})")
    
    # Quick check H10.1.1 (preliminar)
    if 'AdaptiveCurriculum' in args.groups and 'ControlS0' in args.groups:
        adaptive_rewards = [m['final_window']['mean_reward_env'] for m in all_metrics if m['group'] == 'AdaptiveCurriculum']
        control_rewards = [m['final_window']['mean_reward_env'] for m in all_metrics if m['group'] == 'ControlS0']
        
        if len(adaptive_rewards) == len(control_rewards):
            ratios = [a/c for a,c in zip(adaptive_rewards, control_rewards)]
            ratio_mean = np.mean(ratios)
            
            print(f"\n🎯 QUICK CHECK H10.1.1 (v10.1 balance=5.0):")
            print(f"   Ratio Adaptive/Control: {ratio_mean:.3f}")
            if ratio_mean >= 0.70:
                print(f"   ✅ H10.1.1 preliminar: Adaptive ≥ 0.70 (ÉXITO)")
            elif ratio_mean >= 0.60:
                print(f"   ⚠️  H10.1.1 preliminar: Ratio 0.60-0.70 (PARCIAL)")
            else:
                print(f"   ❌ H10.1.1 preliminar: Ratio < 0.60 (FALLA)")
            
            # Comparación vs v10 (trivial)
            print(f"\n📈 COMPARACIÓN v10 vs v10.1:")
            print(f"   v10 (balance=8.0): ratio ≈ 0.995 (trivial, sin discriminación)")
            print(f"   v10.1 (balance=5.0): ratio = {ratio_mean:.3f} ({'discrimina' if ratio_mean < 0.95 else 'aún trivial'})")
    
    print(f"\n🔬 Próximo paso: Análisis estadístico completo")
    print(f"   python scripts/analyze_v10.1.py")
    print(f"\n📄 Actualizar TRACKING:")
    print(f"   results/pgf_v10.1/TRACKING_v10.1.md")


if __name__ == '__main__':
    main()
