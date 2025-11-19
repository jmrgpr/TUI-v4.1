"""
Script de Ejecución - Experimento 10.3: CRÍTICO - Primera Calibración VÁLIDA 8×8
=================================================================================

CONTEXTO CRÍTICO:
    v10/v10.1/v10.2 INVALIDADOS por bug tripwires:
    - Bug: info['tripwire_triggered'] (NO EXISTE) → shaping inerte, tripwires=0 falsos
    - Fix: info['tripwire'] (CORRECTO) → presión real detectada
    
    v10.2 CON FIX (balance=4.0):
    - Control: 100% success (AÚN TRIVIAL), tripwires=1.0 mean
    - Adaptive: 0% success, tripwires=7, rewards ~23 (presión real)
    
CAMBIOS v10.3 (DOBLE PRESIÓN):
    - Balance: 4.0 → 3.5 (margen 175% vs 200%)
    - Spawn_rate: 0.25 → 0.30 (~19 minas vs 16)
    - OBJETIVO: Control 70-90% success (primera discriminación REAL)

GATES DECISIVOS (test mode):
    ✅ Control 70-90% → BATCH completo v10.3
    ❌ Control >90% → FALLBACK 6×6 balance=5.0
    ❌ Control <60% → Balance=4.0 (punto medio v10.2/v10.3)

Diseño: 3 grupos × 8 seeds = 24 configuraciones
        - ADAPTIVE: Curriculum threshold-based (success>0.60, timeout 150 eps/etapa)
        - FIXED: Curriculum rígido (100 eps/etapa, 5 etapas)
        - CONTROL_S0: 400 eps con s=0.0 sin shaping (baseline capacidad 8×8)

Uso:
    # Test mode (2 seeds × 100 eps, CRÍTICO validación gates)
    python scripts/run_experiment_10.3_critical.py --test_mode
    
    # Ejecución completa v10.3 (SI gates OK)
    python scripts/run_experiment_10.3_critical.py
    
Autor: TUI v4.1 Research Team
Fecha: 4 diciembre 2025
Predecesores: v10/v10.1/v10.2 INVALIDADOS (bug tripwires), v10.2 FIX parcial (100% trivial)
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
# CONFIGURACIÓN v10.3 (DOBLE PRESIÓN)
# ============================================================================

# Grid 8×8
GRID_SIZE = 8
MANHATTAN_MAX = 14  # (0,0) → (7,7)

# Tripwires (AUMENTADO spawn_rate para más densidad)
SPAWN_RATE = 0.30  # ~19 tripwires por episodio (vs 16 en v10.2)
TRIPWIRE_PENALTY = -100.0

# Balance inicial v10.3 (MÁS RESTRICTIVO)
INITIAL_BALANCE = 3.5  # Margen 175% (24.5 steps / 14 Manhattan)
DECAY_RATE = 0.1

# Reward env
GOAL_REWARD = +100.0
RESOURCE_REWARD = +10.0

# Curriculum v10.3 (mismo v10.2)
CURRICULUM_STAGES_ADAPTIVE = [0.0, 0.25, 0.5, 0.75, 1.0]  # 5 etapas
CURRICULUM_STAGES_FIXED = [
    {'scale': 0.0, 'episodes': 100},
    {'scale': 0.25, 'episodes': 100},
    {'scale': 0.5, 'episodes': 100},
    {'scale': 0.75, 'episodes': 100},
    {'scale': 1.0, 'episodes': 100}
]

# Threshold-based transitions (mismo v10.2)
THRESHOLD_SUCCESS = 0.60
WINDOW_SIZE = 25
TIMEOUT_EPISODES = 150

# Grupos experimentales
GROUPS = ['AdaptiveCurriculum', 'FixedCurriculum', 'ControlS0']

# Seeds v10.3 (N=8)
SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021]

# Hiperparámetros DQN
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
CHECKPOINT_FREQ = 6

# Output v10.3
RESULTS_DIR = Path('results/pgf_v10.3/resultados')
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# CLASE ADAPTIVECURRICULUM (idéntica v10.2)
# ============================================================================

class AdaptiveCurriculum:
    """Curriculum learning con transiciones threshold-based."""
    
    def __init__(self, stages=None, threshold=0.75, window_size=25, timeout=150):
        self.stages = stages if stages is not None else CURRICULUM_STAGES_ADAPTIVE
        self.threshold = threshold
        self.window_size = window_size
        self.timeout = timeout
        
        self.current_stage = 0
        self.episodes_in_stage = 0
        self.success_history = []
        self.transitions = []
    
    def should_advance(self):
        if len(self.success_history) >= self.window_size:
            recent_success = np.mean([s for s in self.success_history[-self.window_size:]])
            ready = recent_success > self.threshold
        else:
            ready = False
        
        timeout_reached = self.episodes_in_stage >= self.timeout
        
        return ready or timeout_reached
    
    def update(self, goal_reached, episode_global):
        self.success_history.append(int(goal_reached))
        self.episodes_in_stage += 1
        
        if self.should_advance() and self.current_stage < len(self.stages) - 1:
            if len(self.success_history) >= self.window_size:
                recent_success = np.mean([s for s in self.success_history[-self.window_size:]])
                reason = f"ready_success={recent_success:.2f}" if recent_success > self.threshold else "timeout"
            else:
                reason = "timeout"
            
            old_stage = self.current_stage
            self.current_stage += 1
            self.transitions.append((episode_global, old_stage, self.current_stage, reason))
            
            print(f"    [ADAPTIVE] Avanzando stage {old_stage}→{self.current_stage} " 
                  f"(s={self.stages[old_stage]:.2f}→{self.stages[self.current_stage]:.2f}) "
                  f"tras {self.episodes_in_stage} eps ({reason})")
            
            self.episodes_in_stage = 0
    
    def get_current_scale(self):
        return self.stages[self.current_stage]
    
    def get_stage_info(self):
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
        return self.current_stage == len(self.stages) - 1 and self.episodes_in_stage >= min_episodes_final


# ============================================================================
# ENTRENAMIENTO (CON FIX tripwires)
# ============================================================================

def create_env_and_agent(grid_size, seed):
    """Crea entorno 8×8 y agente DQN."""
    np.random.seed(seed)
    
    num_tripwires = int(grid_size * grid_size * SPAWN_RATE)
    available_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                       if (i, j) != (0, 0) and (i, j) != (grid_size-1, grid_size-1)]
    np.random.shuffle(available_cells)
    tripwires_list = available_cells[:num_tripwires]
    
    # v10.3: balance=3.5, spawn_rate=0.30
    env = ResourceDensityEnv(
        size=grid_size,
        tripwires=tripwires_list,
        resource_spawn_rate=SPAWN_RATE,  # 0.30 (más densidad)
        step_cost=-0.2,
        resource_reward=1.0,
        initial_resources=INITIAL_BALANCE  # 3.5 (más restrictivo)
    )
    
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
    """Entrena un episodio con escala de shaping dada."""
    actions_map = ['up', 'down', 'left', 'right']
    
    state_dict = env.reset()
    done = False
    steps = 0
    
    total_reward_env = 0.0
    total_reward_shaped = 0.0
    tripwires_count = 0
    resources_count = 0
    
    death_starvation = 0
    death_tripwire = 0
    goal_reached = False
    
    while not done:
        state_vec = np.array([v for _, v in state_dict], dtype=np.float32)
        action_idx = agent.act(state_vec)
        action = actions_map[action_idx]
        
        next_state_dict, reward_env, done, info = env.step(action)
        
        reward_shaped = reward_env
        if shaping_scale > 0:
            # FIX CRÍTICO v10.3: info['tripwire'] (NO tripwire_triggered)
            if info.get('tripwire', False):
                reward_shaped += shaping_scale * (-100.0)
            if info.get('resource_collected', False):
                reward_shaped += shaping_scale * 10.0
        
        next_state_vec = np.array([v for _, v in next_state_dict], dtype=np.float32)
        agent.remember(state_vec, action_idx, reward_shaped, next_state_vec, done)
        agent.learn()
        
        state_dict = next_state_dict
        steps += 1
        
        total_reward_env += reward_env
        total_reward_shaped += reward_shaped
        
        # FIX CRÍTICO v10.3: info['tripwire'] (NO tripwire_triggered)
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
    """Entrena con curriculum adaptativo threshold-based."""
    seed = config['seed']
    curriculum = AdaptiveCurriculum(
        stages=CURRICULUM_STAGES_ADAPTIVE,
        threshold=THRESHOLD_SUCCESS,
        window_size=WINDOW_SIZE,
        timeout=TIMEOUT_EPISODES
    )
    
    episode_data = []
    episode_global = 0
    max_episodes = 600
    
    print(f"    🔄 ADAPTIVE CURRICULUM: threshold={THRESHOLD_SUCCESS}, timeout={TIMEOUT_EPISODES}")
    
    while episode_global < max_episodes:
        current_scale = curriculum.get_current_scale()
        stage_info = curriculum.get_stage_info()
        
        metrics = train_single_episode(env, agent, current_scale)
        
        metrics['episode'] = episode_global
        metrics['shaping_scale'] = current_scale
        metrics['stage'] = stage_info['current_stage']
        metrics['episodes_in_stage'] = stage_info['episodes_in_stage']
        metrics['success_rate_last_25'] = stage_info['success_rate_last_25']
        metrics['epsilon'] = agent.epsilon
        metrics['seed'] = seed
        
        episode_data.append(metrics)
        
        curriculum.update(metrics['goal_reached'], episode_global)
        
        if (episode_global + 1) % verbose_freq == 0:
            stage_str = f"Stage {stage_info['current_stage']} (s={current_scale:.2f})"
            success_str = f"SR_25={stage_info['success_rate_last_25']:.0%}" if not np.isnan(stage_info['success_rate_last_25']) else "SR_25=N/A"
            print(f"      [Adaptive] Ep {episode_global+1} | {stage_str} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | "
                  f"{success_str} | ε: {agent.epsilon:.3f}")
        
        episode_global += 1
        
        if curriculum.is_finished(min_episodes_final=50):
            print(f"    ✓ Curriculum completado en {episode_global} episodios "
                  f"({len(curriculum.transitions)} transiciones)")
            break
    
    if curriculum.transitions:
        print(f"    📊 Transiciones: {curriculum.transitions}")
    
    transition_episodes = {t[0] for t in curriculum.transitions}
    for ep_data in episode_data:
        ep_data['transition_triggered'] = int(ep_data['episode'] in transition_episodes)
    
    return episode_data


def train_fixed_curriculum(env, agent, config, verbose_freq=25):
    """Entrena con curriculum fijo (100 eps/etapa, 5 etapas = 500 eps)."""
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
            
            metrics['episode'] = episode_global
            metrics['shaping_scale'] = scale
            metrics['stage'] = stage_idx
            metrics['episodes_in_stage'] = ep_in_stage + 1
            metrics['success_rate_last_25'] = np.nan
            metrics['transition_triggered'] = int(ep_in_stage == n_episodes - 1)
            metrics['epsilon'] = agent.epsilon
            metrics['seed'] = seed
            
            episode_data.append(metrics)
            
            if (episode_global + 1) % verbose_freq == 0:
                print(f"      [Fixed] Ep {episode_global+1} | Stage {stage_idx} (s={scale:.2f}) | "
                      f"Reward_env: {metrics['total_reward_env']:.1f} | "
                      f"Tripwires: {metrics['tripwires_triggered']} | ε: {agent.epsilon:.3f}")
            
            episode_global += 1
    
    print(f"    ✓ Fixed curriculum completado ({episode_global} episodios)")
    
    return episode_data


def train_control_s0(env, agent, config, n_episodes=400, verbose_freq=25):
    """Entrena sin shaping (s=0.0) durante 400 episodios."""
    seed = config['seed']
    episode_data = []
    
    print(f"    🔵 CONTROL S=0.0 (sin shaping): {n_episodes} episodios")
    
    for episode in range(n_episodes):
        metrics = train_single_episode(env, agent, shaping_scale=0.0)
        
        metrics['episode'] = episode
        metrics['shaping_scale'] = 0.0
        metrics['stage'] = 0
        metrics['episodes_in_stage'] = episode + 1
        metrics['success_rate_last_25'] = np.nan
        metrics['transition_triggered'] = 0
        metrics['epsilon'] = agent.epsilon
        metrics['seed'] = seed
        
        episode_data.append(metrics)
        
        if (episode + 1) % verbose_freq == 0:
            print(f"      [ControlS0] Ep {episode+1}/{n_episodes} | "
                  f"Reward_env: {metrics['total_reward_env']:.1f} | "
                  f"Tripwires: {metrics['tripwires_triggered']} | ε: {agent.epsilon:.3f}")
    
    return episode_data


# ============================================================================
# EJECUCIÓN CONFIG
# ============================================================================

def run_config(config, output_dir, verbose=True):
    """Ejecuta una configuración (seed + grupo)."""
    group = config['group']
    seed = config['seed']
    
    print("\n" + "="*70)
    print(f"CONFIG v10.3: group={group}, seed={seed}, grid={GRID_SIZE}×{GRID_SIZE}")
    print(f"   Balance={INITIAL_BALANCE} (175% margen), spawn_rate={SPAWN_RATE} (~19 minas)")
    print("="*70)
    
    env, agent = create_env_and_agent(GRID_SIZE, seed)
    
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
    
    df = pd.DataFrame(episode_data)
    
    required_cols = [
        'episode', 'total_reward_env', 'total_reward_shaped', 'shaping_scale',
        'goal_reached', 'tripwires_triggered', 'epsilon', 'seed',
        'stage', 'episodes_in_stage', 'success_rate_last_25', 'transition_triggered'
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas faltantes en DataFrame: {missing_cols}")
    
    # Guardar CSV v10.3
    csv_filename = f"exp10.3_{group}_seed{seed}_episodes.csv"
    csv_path = output_dir / csv_filename
    df.to_csv(csv_path, index=False)
    print(f"\n📁 Guardado: {csv_filename}")
    
    print(f"    ✓ CSV validado: {len(df)} filas, {len(required_cols)} columnas críticas OK")
    
    final_window = df.iloc[-50:] if len(df) >= 50 else df
    
    metrics_summary = {
        'group': group,
        'seed': seed,
        'grid_size': GRID_SIZE,
        'initial_balance': INITIAL_BALANCE,
        'spawn_rate': SPAWN_RATE,
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
    
    json_filename = f"exp10.3_{group}_seed{seed}_metrics.json"
    json_path = output_dir / json_filename
    with open(json_path, 'w') as f:
        json.dump(metrics_summary, f, indent=2, cls=NumpyEncoder)
    print(f"📁 Guardado: {json_filename}")
    
    print(f"\n📊 RESULTADOS v10.3 {group}:")
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
    """Ejecuta experimento v10.3 completo o test mode."""
    parser = argparse.ArgumentParser(description='Experimento 10.3 CRÍTICO: Primera Calibración VÁLIDA 8×8')
    parser.add_argument('--test_mode', action='store_true', 
                        help='Modo test: 2 seeds × 100 eps (validación gates DECISIVO)')
    parser.add_argument('--groups', nargs='+', choices=GROUPS, default=GROUPS,
                        help='Grupos a ejecutar')
    parser.add_argument('--seeds', type=int, nargs='+', default=SEEDS,
                        help='Seeds a ejecutar')
    
    args = parser.parse_args()
    
    # Test mode: 2 seeds × 100 eps (GATES DECISIVOS)
    if args.test_mode:
        test_seeds = [42, 123]
        print("="*70)
        print("🧪 MODO TEST v10.3: DECISIVO - Primera Calibración VÁLIDA 8×8")
        print("="*70)
        print(f"⚠️  CONTEXTO CRÍTICO:")
        print(f"   v10/v10.1/v10.2 INVALIDADOS (bug tripwires: shaping inerte, gates falsos)")
        print(f"   v10.2 FIX: Control 100% (balance=4.0 AÚN trivial)")
        print(f"\n🔧 AJUSTES v10.3 (DOBLE PRESIÓN):")
        print(f"   Balance: 4.0 → {INITIAL_BALANCE} (margen 200% → 175%)")
        print(f"   Spawn_rate: 0.25 → {SPAWN_RATE} (~16 → ~19 minas)")
        print(f"\n🚦 GATES DECISIVOS:")
        print(f"   ✅ Control 70-90% → BATCH completo v10.3")
        print(f"   ❌ Control >90% → FALLBACK 6×6 balance=5.0")
        print(f"   ❌ Control <60% → Balance=4.0 (punto medio v10.2/v10.3)")
        print(f"\n📊 EJECUCIÓN:")
        print(f"   Seeds: {test_seeds}")
        print(f"   Episodios máx: 100 (adaptive puede terminar antes)")
        print(f"   Grid: {GRID_SIZE}×{GRID_SIZE}")
        
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
            control_tripwires = [m['final_window']['mean_tripwires'] for m in control_metrics]
            mean_success = np.mean(control_success)
            mean_tripwires = np.mean(control_tripwires)
            
            print("\n" + "="*70)
            print("🚦 ANÁLISIS GATES DECISIVO (TEST MODE v10.3)")
            print("="*70)
            print(f"Control success rate (N={len(control_success)}): {mean_success:.1%}")
            print(f"Control tripwires mean (N={len(control_tripwires)}): {mean_tripwires:.2f}")
            
            if 0.70 <= mean_success <= 0.90:
                print(f"\n   ✅ GATE ÉXITO: Control en zona óptima 70-90%")
                print(f"   🟢 DECISIÓN: PROCEDER con batch completo v10.3")
                print(f"   🎯 PRIMERA CALIBRACIÓN 8×8 VÁLIDA ENCONTRADA")
                print(f"\n   📈 Balance=3.5 + spawn_rate=0.30 = DISCRIMINACIÓN REAL")
                print(f"   🔬 Próximo: Batch 24 configs → Análisis ratio → Instrumentación PGF → v11")
            elif mean_success > 0.90:
                print(f"\n   ❌ GATE FALLA: Control {mean_success:.1%} (AÚN TRIVIAL)")
                if mean_success > 0.95:
                    print(f"   🔴 DECISIÓN: FALLBACK 6×6 balance=5.0")
                    print(f"   ⚠️  8×8 DEMASIADO DIFÍCIL de calibrar económicamente")
                    print(f"   📌 Alternativa: Reducir complejidad espacial + mantener presión")
                else:
                    print(f"   🟡 DECISIÓN: Balance=3.0-3.25 (última iteración 8×8)")
                    print(f"   ⚠️  BORDERLINE: Cercano trivial pero puede funcionar")
            elif mean_success < 0.60:
                print(f"\n   ❌ GATE FALLA: Control {mean_success:.1%} (MUY DIFÍCIL)")
                print(f"   🔴 DECISIÓN: Balance=4.0 (punto medio v10.2/v10.3)")
                print(f"   📊 v10.3 DEMASIADO RESTRICTIVO (balance=3.5 + spawn=0.30)")
                print(f"   🔄 Volver a v10.2 balance=4.0 O reducir spawn_rate=0.25")
            else:
                print(f"\n   ⚠️  GATE PARCIAL: Control {mean_success:.1%} (60-70%)")
                print(f"   🟡 DECISIÓN: PROCEDER con cautela")
                print(f"   📊 Puede discriminar pero necesita análisis cuidadoso")
            
            print(f"\n   📍 Tripwires mean={mean_tripwires:.2f} (presión REAL detectada)")
        
        return
    
    # Modo completo v10.3
    print("="*70)
    print("EXPERIMENTO v10.3 CRÍTICO: Primera Calibración VÁLIDA 8×8")
    print("="*70)
    print(f"⚠️  v10/v10.1/v10.2 INVALIDADOS (bug tripwires)")
    print(f"Cambios v10.3 (DOBLE PRESIÓN):")
    print(f"   Balance: 4.0 → {INITIAL_BALANCE} (margen 175%)")
    print(f"   Spawn_rate: 0.25 → {SPAWN_RATE} (~19 minas)")
    print(f"Grupos: {args.groups}")
    print(f"Seeds (N={len(args.seeds)}): {args.seeds}")
    print(f"Grid: {GRID_SIZE}×{GRID_SIZE}")
    
    configs = []
    for group in args.groups:
        for seed in args.seeds:
            configs.append({'group': group, 'seed': seed})
    
    print(f"\n📊 TOTAL: {len(configs)} configuraciones")
    
    n_adaptive = sum(1 for c in configs if c['group'] == 'AdaptiveCurriculum')
    n_fixed = sum(1 for c in configs if c['group'] == 'FixedCurriculum')
    n_control = sum(1 for c in configs if c['group'] == 'ControlS0')
    
    total_eps = n_adaptive * 450 + n_fixed * 500 + n_control * 400
    estimated_minutes = total_eps * 0.08
    
    print(f"   Episodios totales estimados: ~{total_eps:,}")
    print(f"   Tiempo estimado: ~{estimated_minutes:.0f} minutos (~{estimated_minutes/60:.1f} horas)")
    print(f"   Checkpoints: cada {CHECKPOINT_FREQ} configs (~{estimated_minutes/len(configs)*CHECKPOINT_FREQ:.0f} min)")
    
    all_metrics = []
    start_time = time.time()
    
    for i, config in enumerate(configs, 1):
        print(f"\n\n🔄 CONFIG {i}/{len(configs)}")
        metrics = run_config(config, RESULTS_DIR, verbose=True)
        all_metrics.append(metrics)
        
        if i % CHECKPOINT_FREQ == 0 and i < len(configs):
            elapsed = (time.time() - start_time) / 60
            remaining = (len(configs) - i) * (elapsed / i)
            print(f"\n⏱️  CHECKPOINT {i//CHECKPOINT_FREQ}: {i}/{len(configs)} completo "
                  f"({elapsed:.1f} min, ~{remaining:.1f} min restantes)")
            print(f"      Progreso: {i/len(configs)*100:.1f}% | "
                  f"Seeds procesadas: {len(set([m['seed'] for m in all_metrics]))}")
    
    total_time = (time.time() - start_time) / 60
    print("\n\n" + "="*70)
    print("✅ EXPERIMENTO v10.3 COMPLETADO")
    print("="*70)
    print(f"   Configs ejecutadas: {len(configs)}")
    print(f"   Tiempo total: {total_time:.1f} min ({total_time/60:.1f} horas)")
    print(f"   Output directory: {RESULTS_DIR}")
    
    print(f"\n📊 RESUMEN POR GRUPO (reward_env final):")
    for group in args.groups:
        group_metrics = [m for m in all_metrics if m['group'] == group]
        if group_metrics:
            rewards = [m['final_window']['mean_reward_env'] for m in group_metrics]
            mean_reward = np.mean(rewards)
            std_reward = np.std(rewards, ddof=1)
            print(f"   {group:18}: {mean_reward:7.2f} ± {std_reward:5.2f} (N={len(group_metrics)})")
    
    if 'AdaptiveCurriculum' in args.groups and 'ControlS0' in args.groups:
        adaptive_rewards = [m['final_window']['mean_reward_env'] for m in all_metrics if m['group'] == 'AdaptiveCurriculum']
        control_rewards = [m['final_window']['mean_reward_env'] for m in all_metrics if m['group'] == 'ControlS0']
        
        if len(adaptive_rewards) == len(control_rewards):
            ratios = [a/c for a,c in zip(adaptive_rewards, control_rewards)]
            ratio_mean = np.mean(ratios)
            
            print(f"\n🎯 QUICK CHECK H10.3.1 (v10.3 balance=3.5, spawn=0.30):")
            print(f"   Ratio Adaptive/Control: {ratio_mean:.3f}")
            if ratio_mean >= 0.70:
                print(f"   ✅ H10.3.1 preliminar: Adaptive ≥ 0.70 (ÉXITO)")
            elif ratio_mean >= 0.60:
                print(f"   ⚠️  H10.3.1 preliminar: Ratio 0.60-0.70 (PARCIAL)")
            else:
                print(f"   ❌ H10.3.1 preliminar: Ratio < 0.60 (FALLA)")
            
            print(f"\n📈 COMPARACIÓN HISTÓRICA:")
            print(f"   v10 (balance=8.0): ratio ≈ 0.995 (INVÁLIDO - bug tripwires)")
            print(f"   v10.1 (balance=5.0): ratio ≈ 1.000 (INVÁLIDO - bug tripwires)")
            print(f"   v10.2 (balance=4.0 FIX): ratio ≈ ? (Control 100%, Adaptive 0% - no ratio)")
            print(f"   v10.3 (balance=3.5, spawn=0.30): ratio = {ratio_mean:.3f} ({'DISCRIMINA' if ratio_mean < 0.95 and ratio_mean > 0.60 else 'revisar'})")
    
    print(f"\n🔬 Próximo paso: Análisis estadístico completo v10.3")
    print(f"   python scripts/analyze_v10.3.py")
    print(f"\n📄 Actualizar TRACKING:")
    print(f"   results/pgf_v10.3/TRACKING_v10.3.md")


if __name__ == '__main__':
    main()
