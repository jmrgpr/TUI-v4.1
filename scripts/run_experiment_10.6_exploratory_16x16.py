"""
Script de Ejecución - Experimento 10.6 EXPLORATORIO: Grid 16×16
================================================================

HIPÓTESIS CONTRAINTUITIVA:
──────────────────────────────────────────────────────────────────────────────
v10.3-v10.5 FRACASARON en 8×8 (Manhattan=14) por rango viable estrecho:
  - step=-0.20: 100% trivial
  - step=-0.25: 0%   inviable
  
NUEVA HIPÓTESIS v10.6 (EXPLORATORIO):
Grid MÁS GRANDE (16×16, Manhattan=30) puede MEJORAR aprendizaje DQN:

1. **Más espacio de maniobra**: 
   - Múltiples rutas alternativas (no forzado camino único)
   - DQN explora opciones sin colapsar inmediato
   
2. **Margen temporal mayor**:
   - Camino más largo tolera más steps exploración
   - Balance puede absorber vagabundeo inicial
   
3. **Gradiente aprendizaje suave**:
   - Recompensas distribuidas (más resources spawn)
   - Señal refuerzo menos binaria (éxito/fracaso)

PARÁMETROS EXPLORATORIOS v10.6:
──────────────────────────────────────────────────────────────────────────────
Grid:              16×16 (Manhattan max = 30 steps, 2.14× más largo que 8×8)
Balance inicial:   7.5 resources (≈2.14× proporción 8×8)
Spawn rate:        0.30 (≈77 tripwires/episodio, densidad alta)
Tripwire penalty:  -100.0 (mantener presión evasión)

ECONOMÍA PROPORCIONAL:
──────────────────────────────────────────────────────────────────────────────
resource_reward:   0.75  (mantener valor intermedio)
step_cost:        -0.25  (mantener penalización)

CÁLCULO VIABILIDAD:
Balance inicial:     7.5
Costo viaje mínimo:  30 steps × -0.25 = -7.5
Balance post-viaje:  7.5 - 7.5 = 0.0 ✓ (JUSTO viable, igual 8×8)

Con 1 recolección:
Balance + resource:  7.5 + 0.75 = 8.25
Costo viaje + desvío: ~32 steps × -0.25 = -8.0
Balance final:        8.25 - 8.0 = 0.25 ✓ (viable con margen)

Con 3 recolecciones:
Balance + 3×resource: 7.5 + 2.25 = 9.75
Costo viaje + desvíos: ~36 steps × -0.25 = -9.0
Balance final:         9.75 - 9.0 = 0.75 ✓ (viable con eficiencia)

HIPÓTESIS COMPARATIVA:
──────────────────────────────────────────────────────────────────────────────
8×8:  Manhattan=14, balance post-viaje=0.0 → DQN FALLA (0% success)
16×16: Manhattan=30, balance post-viaje=0.0 → DQN APRENDE? (>50% success?)

Razones potenciales mejora:
  - Más opciones de ruta (256 celdas vs 64)
  - Exploración tolera error (margen temporal)
  - Señal refuerzo acumulativa (más steps = más experiencia)
  
Razones potenciales fallo:
  - Complejidad estado mayor (harder planning)
  - Espacio acción exponencial (más difícil convergencia)
  - Mismo DQN arquitectura (Hidden=64 puede ser insuficiente)

DISEÑO EXPLORATORIO (CORTO):
──────────────────────────────────────────────────────────────────────────────
N seeds:           2 (42, 123) - exploración rápida
N episodes:        200 (vs 400 estándar) - convergencia preliminar
Grupos:            2 (ControlS0, AdaptiveCurriculum) - foco discriminación
Verbose freq:      25 (monitoreo regular)
Duración estimada: ~5-8 min (episodios más largos pero menos total)

GATES EXPLORATORIOS:
──────────────────────────────────────────────────────────────────────────────
SI Control >20% success:
   ✅ HIPÓTESIS SOPORTADA: Grid grande MEJORA aprendizaje
   → Calibrar 16×16 completo (ajustar economía discriminativa)
   
SI Control 0-10% success:
   ⚠️  HIPÓTESIS PARCIAL: Espacio no suficiente, complejidad domina
   → Considerar 12×12 intermedio O retroceder 6×6
   
SI Control 10-20% success:
   🔄 HIPÓTESIS AMBIGUA: Margen existe pero débil
   → Probar economía más generosa 16×16 (step=-0.20)

MÉTRICAS CLAVE OBSERVAR:
──────────────────────────────────────────────────────────────────────────────
1. Success rate (>20% indica viabilidad)
2. Steps to goal (comparar con Manhattan=30 óptimo)
3. Resources collected (eficiencia recolección)
4. Tripwires triggered (evasión aprendida)
5. Reward convergencia (plateau indica aprendizaje)

RIESGO CONOCIDO:
──────────────────────────────────────────────────────────────────────────────
- Episodios 16×16 más lentos (~2-3× tiempo 8×8)
- DQN Hidden=64 puede ser pequeño (estado 256 celdas)
- Curriculum timeout=150 puede ser corto (grid grande requiere más eps)

Uso:
    # Exploratorio 16×16 (2 seeds × 200 eps, ~5-8 min)
    python scripts/run_experiment_10.6_exploratory_16x16.py
    
Autor: TUI v4.1 Research Team
Fecha: 4 diciembre 2025
Motivación: Exploración contraintuitiva post-fracaso 8×8 (v10.3-v10.5)
Referencias: docs/CALIBRACION_8x8_FRACASO_v10.3-10.5.md
"""

import sys
import os
import json
import time
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
# NUMPY ENCODER
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
# CONFIGURACIÓN v10.6 EXPLORATORIO 16×16
# ============================================================================

# Grid 16×16 (EXPLORACIÓN GRANDE)
GRID_SIZE = 16
MANHATTAN_MAX = 30  # (0,0) → (15,15)

# Tripwires (densidad alta)
SPAWN_RATE = 0.30  # ~77 tripwires por episodio
TRIPWIRE_PENALTY = -100.0

# Balance inicial PROPORCIONAL
INITIAL_BALANCE = 7.5  # 2.14× proporción 8×8 (3.5 × 30/14)
DECAY_RATE = 0.1

# Economía (mantener v10.5)
GOAL_REWARD = +100.0
RESOURCE_REWARD = 0.75  # Intermedio
STEP_COST = -0.25  # Restrictivo pero viable teóricamente

# Curriculum adaptativo
CURRICULUM_STAGES_ADAPTIVE = [0.0, 0.25, 0.5, 0.75, 1.0]  # 5 etapas
THRESHOLD_SUCCESS = 0.60
WINDOW_SIZE = 25
TIMEOUT_EPISODES = 100  # Más largo (grid grande requiere más tiempo)

# Grupos exploratorios
GROUPS = ['ControlS0', 'AdaptiveCurriculum']  # Solo 2 (foco)

# Seeds exploratorios
SEEDS = [42, 123]  # N=2 (rápido)

# Hiperparámetros DQN (mantener)
HIDDEN_SIZE = 64  # RIESGO: puede ser pequeño para 16×16
BUFFER_SIZE = 10000
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
TARGET_UPDATE = 10

# Episodios REDUCIDOS (exploratorio)
N_EPISODES_CONTROL = 200  # vs 400 estándar
MAX_EPISODES_ADAPTIVE = 400  # con curriculum

# Output
RESULTS_DIR = Path('results/pgf_v10.6_exploratory_16x16/resultados')
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# CLASE ADAPTIVECURRICULUM
# ============================================================================

class AdaptiveCurriculum:
    """Curriculum learning con transiciones threshold-based."""
    
    def __init__(self, stages=None, threshold=0.75, window_size=25, timeout=100):
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
# ENTRENAMIENTO 16×16
# ============================================================================

def create_env_and_agent(grid_size, seed):
    """Crea entorno 16×16 EXPLORATORIO."""
    np.random.seed(seed)
    
    num_tripwires = int(grid_size * grid_size * SPAWN_RATE)
    available_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                       if (i, j) != (0, 0) and (i, j) != (grid_size-1, grid_size-1)]
    np.random.shuffle(available_cells)
    tripwires_list = available_cells[:num_tripwires]
    
    env = ResourceDensityEnv(
        size=grid_size,
        tripwires=tripwires_list,
        resource_spawn_rate=SPAWN_RATE,
        step_cost=STEP_COST,
        resource_reward=RESOURCE_REWARD,
        initial_resources=INITIAL_BALANCE
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
    max_episodes = MAX_EPISODES_ADAPTIVE
    
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
                  f"Reward: {metrics['total_reward_env']:.1f} | "
                  f"Steps: {metrics['steps_to_goal']} | "
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


def train_control_s0(env, agent, config, n_episodes=200, verbose_freq=25):
    """Entrena sin shaping (s=0.0) durante N episodios."""
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
                  f"Reward: {metrics['total_reward_env']:.1f} | "
                  f"Steps: {metrics['steps_to_goal']} | "
                  f"Goal: {metrics['goal_reached']} | ε: {agent.epsilon:.3f}")
    
    return episode_data


# ============================================================================
# EJECUCIÓN CONFIG
# ============================================================================

def run_config(config, output_dir, verbose=True):
    """Ejecuta una configuración (seed + grupo)."""
    group = config['group']
    seed = config['seed']
    
    print("\n" + "="*70)
    print(f"CONFIG v10.6 EXPLORATORIO: group={group}, seed={seed}, grid={GRID_SIZE}×{GRID_SIZE}")
    print(f"   HIPÓTESIS: Grid GRANDE mejora aprendizaje (más maniobra)")
    print(f"   Economía: resource={RESOURCE_REWARD}, step={STEP_COST}, balance={INITIAL_BALANCE}")
    print(f"   Manhattan max: {MANHATTAN_MAX} steps (2.14× más que 8×8)")
    print("="*70)
    
    env, agent = create_env_and_agent(GRID_SIZE, seed)
    
    start_time = time.time()
    
    if group == 'AdaptiveCurriculum':
        episode_data = train_adaptive_curriculum(env, agent, config, verbose_freq=25)
    elif group == 'ControlS0':
        episode_data = train_control_s0(env, agent, config, n_episodes=N_EPISODES_CONTROL, verbose_freq=25)
    else:
        raise ValueError(f"Grupo desconocido: {group}")
    
    duration_min = (time.time() - start_time) / 60
    
    df = pd.DataFrame(episode_data)
    
    required_cols = [
        'episode', 'total_reward_env', 'total_reward_shaped', 'shaping_scale',
        'goal_reached', 'tripwires_triggered', 'epsilon', 'seed',
        'stage', 'episodes_in_stage', 'success_rate_last_25', 'transition_triggered',
        'steps_to_goal', 'resources_collected'
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas faltantes en DataFrame: {missing_cols}")
    
    csv_filename = f"exp10.6_exploratory_{group}_seed{seed}_episodes.csv"
    csv_path = output_dir / csv_filename
    df.to_csv(csv_path, index=False)
    print(f"\n📁 Guardado: {csv_filename}")
    
    final_window = df.iloc[-50:] if len(df) >= 50 else df
    
    metrics_summary = {
        'group': group,
        'seed': seed,
        'grid_size': GRID_SIZE,
        'manhattan_max': MANHATTAN_MAX,
        'initial_balance': INITIAL_BALANCE,
        'spawn_rate': SPAWN_RATE,
        'resource_reward': RESOURCE_REWARD,
        'step_cost': STEP_COST,
        'n_episodes': len(df),
        'duration_min': round(duration_min, 2),
        'final_window': {
            'mean_reward_env': float(final_window['total_reward_env'].mean()),
            'std_reward_env': float(final_window['total_reward_env'].std()),
            'success_rate': float(final_window['goal_reached'].mean()),
            'mean_tripwires': float(final_window['tripwires_triggered'].mean()),
            'mean_steps': float(final_window['steps_to_goal'].mean()),
            'mean_resources': float(final_window['resources_collected'].mean())
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
    
    json_filename = f"exp10.6_exploratory_{group}_seed{seed}_metrics.json"
    json_path = output_dir / json_filename
    with open(json_path, 'w') as f:
        json.dump(metrics_summary, f, indent=2, cls=NumpyEncoder)
    print(f"📁 Guardado: {json_filename}")
    
    print(f"\n📊 RESULTADOS v10.6 EXPLORATORIO {group}:")
    print(f"   Reward env (final): {metrics_summary['final_window']['mean_reward_env']:.2f} ± {metrics_summary['final_window']['std_reward_env']:.2f}")
    print(f"   Success rate (final): {metrics_summary['final_window']['success_rate']:.1%}")
    print(f"   Steps mean (final): {metrics_summary['final_window']['mean_steps']:.1f} (vs Manhattan={MANHATTAN_MAX})")
    print(f"   Resources mean (final): {metrics_summary['final_window']['mean_resources']:.2f}")
    print(f"   Tripwires (mean): {metrics_summary['final_window']['mean_tripwires']:.2f}")
    print(f"   N episodios: {metrics_summary['n_episodes']}")
    print(f"   Duración: {duration_min:.2f} min")
    
    return metrics_summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta experimento EXPLORATORIO v10.6 (16×16)."""
    
    print("="*70)
    print("EXPERIMENTO v10.6 EXPLORATORIO: Grid 16×16")
    print("="*70)
    print(f"⚠️  v10.3-v10.5 FRACASARON en 8×8 (rango viable estrecho)")
    print(f"\n💡 HIPÓTESIS CONTRAINTUITIVA:")
    print(f"   Grid MÁS GRANDE (16×16) puede MEJORAR aprendizaje DQN")
    print(f"   - Más espacio maniobra (múltiples rutas)")
    print(f"   - Margen temporal mayor (tolera exploración)")
    print(f"   - Gradiente aprendizaje suave (señal refuerzo distribuida)")
    print(f"\n🔧 CONFIGURACIÓN:")
    print(f"   Grid: {GRID_SIZE}×{GRID_SIZE} (Manhattan={MANHATTAN_MAX} steps)")
    print(f"   Balance: {INITIAL_BALANCE} (proporcional 8×8)")
    print(f"   Economía: resource={RESOURCE_REWARD}, step={STEP_COST}")
    print(f"   Balance post-viaje: {INITIAL_BALANCE + MANHATTAN_MAX * STEP_COST:.1f} (justo viable)")
    print(f"\n📊 DISEÑO EXPLORATORIO:")
    print(f"   Seeds: {SEEDS} (N={len(SEEDS)})")
    print(f"   Episodios: Control={N_EPISODES_CONTROL}, Adaptive=max{MAX_EPISODES_ADAPTIVE}")
    print(f"   Grupos: {GROUPS}")
    print(f"   Duración estimada: ~5-8 min")
    
    configs = []
    for group in GROUPS:
        for seed in SEEDS:
            configs.append({'group': group, 'seed': seed})
    
    print(f"\n📊 TOTAL: {len(configs)} configuraciones")
    
    all_metrics = []
    start_time = time.time()
    
    for i, config in enumerate(configs, 1):
        print(f"\n\n🔄 CONFIG {i}/{len(configs)}")
        metrics = run_config(config, RESULTS_DIR, verbose=True)
        all_metrics.append(metrics)
    
    total_time = (time.time() - start_time) / 60
    print("\n\n" + "="*70)
    print("✅ EXPERIMENTO v10.6 EXPLORATORIO COMPLETADO")
    print("="*70)
    print(f"   Configs ejecutadas: {len(configs)}")
    print(f"   Tiempo total: {total_time:.1f} min")
    print(f"   Output directory: {RESULTS_DIR}")
    
    print(f"\n📊 RESUMEN EXPLORATORIO:")
    for group in GROUPS:
        group_metrics = [m for m in all_metrics if m['group'] == group]
        if group_metrics:
            success_rates = [m['final_window']['success_rate'] for m in group_metrics]
            rewards = [m['final_window']['mean_reward_env'] for m in group_metrics]
            steps = [m['final_window']['mean_steps'] for m in group_metrics]
            mean_success = np.mean(success_rates)
            mean_reward = np.mean(rewards)
            mean_steps = np.mean(steps)
            print(f"   {group:18}: success={mean_success:.1%}, reward={mean_reward:7.2f}, steps={mean_steps:.1f}")
    
    if 'AdaptiveCurriculum' in GROUPS and 'ControlS0' in GROUPS:
        control_metrics = [m for m in all_metrics if m['group'] == 'ControlS0']
        adaptive_metrics = [m for m in all_metrics if m['group'] == 'AdaptiveCurriculum']
        
        control_success = [m['final_window']['success_rate'] for m in control_metrics]
        adaptive_success = [m['final_window']['success_rate'] for m in adaptive_metrics]
        
        mean_control_success = np.mean(control_success)
        mean_adaptive_success = np.mean(adaptive_success)
        
        print(f"\n🚦 EVALUACIÓN HIPÓTESIS EXPLORATORIA:")
        print(f"   Control success rate: {mean_control_success:.1%}")
        print(f"   Adaptive success rate: {mean_adaptive_success:.1%}")
        
        if mean_control_success > 0.20:
            print(f"\n   ✅ HIPÓTESIS SOPORTADA: Grid 16×16 MEJORA aprendizaje")
            print(f"   🎯 Control {mean_control_success:.1%} > 20% (viable con espacio maniobra)")
            print(f"   🔬 Próximo: Calibrar 16×16 completo (ajustar economía discriminativa)")
        elif mean_control_success > 0.10:
            print(f"\n   🔄 HIPÓTESIS AMBIGUA: Mejora marginal detectada")
            print(f"   ⚠️  Control {mean_control_success:.1%} (10-20% rango débil)")
            print(f"   🔬 Próximo: Probar economía más generosa 16×16 (step=-0.20)")
        else:
            print(f"\n   ❌ HIPÓTESIS NO SOPORTADA: Complejidad domina")
            print(f"   🔴 Control {mean_control_success:.1%} < 10% (espacio NO suficiente)")
            print(f"   🔬 Próximo: Considerar 12×12 intermedio O retroceder 6×6")
        
        print(f"\n📈 COMPARACIÓN HISTÓRICA:")
        print(f"   8×8 (v10.5): Control 0%, step=-0.25, balance post=0.0")
        print(f"   16×16 (v10.6): Control {mean_control_success:.1%}, step=-0.25, balance post=0.0")
        print(f"   Diferencia: Manhattan 14→30 (2.14× más largo)")


if __name__ == '__main__':
    main()
