"""
SCRIPT VALIDACIÓN 4×4 POST-FIXES
=================================

Objetivo: Validar 4 fixes críticos bugs sistemáticos en entorno minimal 4×4

FIXES APLICADOS:
1. max_steps parametrizado por grid (3× Manhattan = 18 steps vs 30 hardcoded)
2. risk_penalty signo correcto (reward += penalty, no -=)
3. step_cost descuenta resources (economía REAL, muerte por inanición)
4. Penalizaciones proporcionales (tripwire=-0.5 vs -0.01)

CONFIGURACIÓN 4×4:
- Grid: 4×4 (Manhattan óptimo = 6 steps)
- max_steps: 18 (3× margen, calculado dinámicamente)
- Balance inicial: 1.5
- step_cost: -0.25 (descuenta resources cada paso)
- resource_reward: 0.75
- Balance post-viaje teórico: 1.5 + 0.75 - 6×0.25 = 0.75 (50% margen)

GATES ESPERADOS (post-fixes):
✅ Control success rate: 70-85% (economía viable con margen)
✅ Resources decrementan cada step (CSV columna resources)
✅ Muerte por inanición observable (starvation flag)
✅ Rewards ~0-5 (SIN bonus +25 invertido)
✅ Tripwires impactan 6-33% resources (0.5/1.5=33% significativo)
✅ max_steps=18 permite exploración (vs 6 óptimo)

DURACIÓN: ~2 min (N=2 seeds × 2 grupos × 100 eps)

SI PASA → v10.7 grid 6×6
SI FALLA → Diagnóstico adicional fixes

Autor: TUI v4.1 Research Team (Post-Auditoría Bugs Sistemáticos)
Fecha: 4 diciembre 2025
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
# CONFIGURACIÓN VALIDACIÓN 4×4
# ============================================================================

# Grid y economía
GRID_SIZE = 4
INITIAL_BALANCE = 3.0  # Generoso 4×4 (permite aprendizaje)
STEP_COST = -0.25  # Ahora descuenta resources (FIX #3)
RESOURCE_REWARD = 0.75
SPAWN_RATE = 0.15

# Cálculo viabilidad económica (CON FIXES):
# Manhattan óptimo 4×4 = (4-1)*2 = 6 steps
# Balance post-viaje = 3.0 + 0.75 - 6×0.25 = 2.25 (150% margen económico)
# max_steps = 6 × 3.0 = 18 (FIX #1: parametrizado dinámicamente)

# DQN hyperparams (estándar)
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995  # DECAY RATE (0.995 multiplicativo por acción)
BATCH_SIZE = 32
BUFFER_SIZE = 10000
TARGET_UPDATE = 100
HIDDEN_SIZE = 64

# Experimento
SEEDS = [42, 123]  # N=2 exploratorio
EPISODES_CONTROL = 100  # Reducido validación rápida
EPISODES_ADAPTIVE = 200  # Max curriculum

GROUPS = {
    'ControlS0': {'shaping': 0.0, 'max_episodes': EPISODES_CONTROL},
    'AdaptiveCurriculum': {'shaping': 'curriculum', 'max_episodes': EPISODES_ADAPTIVE}
}


# ============================================================================
# GATES VALIDACIÓN POST-FIXES
# ============================================================================

def evaluate_gates_validation(control_success, adaptive_success, control_reward, adaptive_reward):
    """
    Gates validación post-fixes (más estrictos que exploratorios).
    
    CRITERIOS:
    1. Control ≥ 70% (economía viable con margen 50%)
    2. Adaptive ≥ Control (curriculum ayuda o neutral)
    3. Rewards 0-10 rango (sin bonus +25 invertido)
    4. NO trivial (Control < 95%)
    """
    gates_passed = []
    gates_failed = []
    
    # Gate 1: Control viable (70-90%)
    if 70 <= control_success <= 90:
        gates_passed.append(f"✅ Control {control_success:.1f}% en rango viable (70-90%)")
    elif control_success > 90:
        gates_failed.append(f"❌ Control {control_success:.1f}% TRIVIAL (>90%)")
    else:
        gates_failed.append(f"❌ Control {control_success:.1f}% BAJO (<70%)")
    
    # Gate 2: Adaptive ayuda o neutral
    if adaptive_success >= control_success * 0.95:
        gates_passed.append(f"✅ Adaptive {adaptive_success:.1f}% ≥ Control (curriculum funciona)")
    else:
        gates_failed.append(f"❌ Adaptive {adaptive_success:.1f}% < Control {control_success:.1f}%")
    
    # Gate 3: Rewards rango esperado (sin bonus +25)
    if 0 <= control_reward <= 10:
        gates_passed.append(f"✅ Control reward {control_reward:.2f} rango esperado (0-10)")
    else:
        gates_failed.append(f"❌ Control reward {control_reward:.2f} fuera rango (¿bonus +25?)")
    
    # Gate 4: NO trivial
    if control_success < 95:
        gates_passed.append("✅ Control NO trivial (<95%)")
    else:
        gates_failed.append("❌ Control TRIVIAL (≥95%)")
    
    # Decisión final
    all_passed = len(gates_failed) == 0
    
    print("\n" + "="*70)
    print("🚦 GATES VALIDACIÓN POST-FIXES")
    print("="*70)
    
    for gate in gates_passed:
        print(gate)
    
    if gates_failed:
        print()
        for gate in gates_failed:
            print(gate)
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ VALIDACIÓN EXITOSA: Todos los gates pasados")
        print("➡️  PRÓXIMO: Ejecutar v10.7 grid 6×6 con fixes")
    else:
        print(f"❌ VALIDACIÓN FALLÓ: {len(gates_failed)} gates fallidos")
        print("➡️  DIAGNÓSTICO: Revisar fixes aplicados")
    print("="*70 + "\n")
    
    return all_passed


# ============================================================================
# ENTRENAMIENTO
# ============================================================================

def create_env_agent(seed, grid_size):
    """Crea entorno y agente con seed."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    num_tripwires = int(grid_size * grid_size * SPAWN_RATE)
    available_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                       if (i, j) != (0, 0) and (i, j) != (grid_size-1, grid_size-1)]
    np.random.shuffle(available_cells)
    tripwires_list = available_cells[:num_tripwires]
    
    # FIX #1: max_steps_multiplier=3.0 (parametrizado dinámicamente)
    env = ResourceDensityEnv(
        size=grid_size,
        tripwires=tripwires_list,
        resource_spawn_rate=SPAWN_RATE,
        step_cost=STEP_COST,
        resource_reward=RESOURCE_REWARD,
        initial_resources=INITIAL_BALANCE,
        max_steps_multiplier=3.0  # 4×4: 6×3=18 steps
    )
    
    state_tuple = env.reset()
    state_size = len(state_tuple)  # Tuple length
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
    state_tuple = env.reset()  # Returns tuple of (key, value) pairs
    state_values = np.array([v for k, v in state_tuple], dtype=np.float32)
    
    episode_reward_env = 0.0
    episode_steps = 0
    done = False
    
    info_history = []
    
    while not done:
        action_idx = agent.act(state_values)
        action = actions_map[action_idx]
        
        next_state_tuple, reward_env, done, info = env.step(action)
        next_state_values = np.array([v for k, v in next_state_tuple], dtype=np.float32)
        
        # Shaping (si aplica)
        if shaping_scale > 0:
            shaping_reward = 0.0
            if info.get('tripwire'):
                shaping_reward -= 0.2
            if info.get('resource_collected'):
                shaping_reward += 0.3
            reward_total = reward_env + shaping_scale * shaping_reward
        else:
            reward_total = reward_env
        
        agent.remember(state_values, action_idx, reward_total, next_state_values, done)
        agent.learn()  # DQNAgent usa learn() no replay()
        
        episode_reward_env += reward_env
        episode_steps += 1
        state_values = next_state_values
        
        info_history.append(info.copy())
    
    # Métricas episodio
    goal_reached = info_history[-1].get('goal_reached', False) if info_history else False
    
    # FIX #3: Validar muerte por inanición (nueva flag)
    starvation = info_history[-1].get('starvation', False) if info_history else False
    
    tripwires_hit = sum(1 for i in info_history if i.get('tripwire', False))
    resources_collected = sum(1 for i in info_history if i.get('resource_collected', False))
    
    # FIX #3: Resources final (debería decrementar cada step)
    resources_final = env.resources
    
    return {
        'reward_env': episode_reward_env,
        'steps': episode_steps,
        'goal_reached': 1 if goal_reached else 0,
        'starvation': 1 if starvation else 0,  # FIX #3: Nueva métrica
        'tripwires': tripwires_hit,
        'resources_collected': resources_collected,
        'resources_final': resources_final,  # FIX #3: Validar decremento
        'epsilon': agent.epsilon
    }


def run_control_group(env, agent, seed, episodes):
    """Ejecuta grupo Control (shaping=0.0)."""
    print(f"    🔵 CONTROL S=0.0 (sin shaping): {episodes} episodios")
    
    results = []
    for ep in range(1, episodes + 1):
        metrics = train_single_episode(env, agent, shaping_scale=0.0)
        metrics['episode'] = ep
        results.append(metrics)
        
        if ep % 25 == 0 or ep == episodes:
            avg_reward = np.mean([r['reward_env'] for r in results[-25:]])
            avg_steps = np.mean([r['steps'] for r in results[-25:]])
            success = metrics['goal_reached']  # Usar metrics actual, no variable 'r'
            eps = agent.epsilon
            print(f"      [Control] Ep {ep}/{episodes} | Reward: {avg_reward:.1f} | Steps: {avg_steps:.0f} | Goal: {success} | ε: {eps:.3f}")
    
    return results


def run_adaptive_curriculum(env, agent, seed, max_episodes):
    """Ejecuta grupo Adaptive Curriculum."""
    print(f"    🔄 ADAPTIVE CURRICULUM: threshold=0.6, timeout=100")
    
    # Curriculum: stages 0→4 (s: 0.0, 0.25, 0.5, 0.75, 1.0)
    stages = [0.0, 0.25, 0.50, 0.75, 1.00]
    current_stage = 0
    episodes_in_stage = 0
    success_threshold = 0.6
    timeout_episodes = 100
    
    results = []
    transitions = []
    
    for ep in range(1, max_episodes + 1):
        shaping = stages[current_stage]
        metrics = train_single_episode(env, agent, shaping_scale=shaping)
        metrics['episode'] = ep
        metrics['stage'] = current_stage
        metrics['shaping'] = shaping
        results.append(metrics)
        
        episodes_in_stage += 1
        
        # Calcular success rate últimos 25 eps
        recent_results = [r for r in results if r['stage'] == current_stage][-25:]
        success_rate = np.mean([r['goal_reached'] for r in recent_results]) if len(recent_results) >= 25 else 0.0
        
        # Avanzar stage (por success o timeout)
        should_advance = False
        reason = None
        
        if success_rate >= success_threshold and len(recent_results) >= 25:
            should_advance = True
            reason = "success"
        elif episodes_in_stage >= timeout_episodes:
            should_advance = True
            reason = "timeout"
        
        if should_advance and current_stage < len(stages) - 1:
            transitions.append((ep - 1, current_stage, current_stage + 1, reason))
            print(f"    [ADAPTIVE] Avanzando stage {current_stage}→{current_stage+1} (s={shaping:.2f}→{stages[current_stage+1]:.2f}) tras {episodes_in_stage} eps ({reason})")
            current_stage += 1
            episodes_in_stage = 0
        
        if ep % 25 == 0 or ep == max_episodes:
            avg_reward = np.mean([r['reward_env'] for r in results[-25:]])
            avg_steps = np.mean([r['steps'] for r in results[-25:]])
            success = metrics['goal_reached']
            eps = agent.epsilon
            sr_display = f"SR_25={success_rate*100:.0f}%" if len(recent_results) >= 25 else "SR_25=N/A"
            print(f"      [Adaptive] Ep {ep} | Stage {current_stage} (s={shaping:.2f}) | Reward: {avg_reward:.1f} | Steps: {avg_steps:.0f} | {sr_display} | ε: {eps:.3f}")
    
    # Agregar transiciones a resultados
    for r in results:
        r['transitions'] = transitions
    
    return results


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def main():
    print("="*70)
    print("VALIDACIÓN 4×4 POST-FIXES (4 bugs críticos corregidos)")
    print("="*70)
    print(f"⚠️  FIXES APLICADOS:")
    print(f"   1. max_steps = Manhattan × 3.0 (18 steps vs 30 hardcoded)")
    print(f"   2. risk_penalty signo correcto (reward += penalty)")
    print(f"   3. step_cost descuenta resources (economía REAL)")
    print(f"   4. Tripwire penalty = -0.5 (vs -0.01 insignificante)")
    print()
    print(f"💡 ECONOMÍA 4×4:")
    print(f"   Manhattan óptimo: 6 steps")
    print(f"   max_steps: 18 (3× margen exploración)")
    print(f"   Balance inicial: {INITIAL_BALANCE}")
    print(f"   step_cost: {STEP_COST} (descuenta resources)")
    print(f"   resource_reward: {RESOURCE_REWARD}")
    print(f"   Balance post-viaje: {INITIAL_BALANCE} + {RESOURCE_REWARD} - 6×{abs(STEP_COST)} = {INITIAL_BALANCE + RESOURCE_REWARD - 6*abs(STEP_COST):.2f} (150% margen)")
    print()
    print(f"🔧 CONFIGURACIÓN:")
    print(f"   Grid: {GRID_SIZE}×{GRID_SIZE}")
    print(f"   Seeds: {SEEDS} (N={len(SEEDS)})")
    print(f"   Episodios: Control={EPISODES_CONTROL}, Adaptive={EPISODES_ADAPTIVE}")
    print(f"   Grupos: {list(GROUPS.keys())}")
    print()
    print(f"📊 TOTAL: {len(SEEDS) * len(GROUPS)} configuraciones")
    print()
    
    # Output directory
    output_dir = Path("results") / "validation_4x4_post_fixes" / "resultados"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    start_time = time.time()
    all_results = {}
    
    # Iterar seeds y grupos
    config_idx = 0
    total_configs = len(SEEDS) * len(GROUPS)
    
    for seed in SEEDS:
        for group_name, group_config in GROUPS.items():
            config_idx += 1
            print(f"\n🔄 CONFIG {config_idx}/{total_configs}\n")
            print("="*70)
            print(f"VALIDACIÓN 4×4: group={group_name}, seed={seed}, grid={GRID_SIZE}×{GRID_SIZE}")
            print(f"   ECONOMÍA: balance={INITIAL_BALANCE}, step={STEP_COST}, resource={RESOURCE_REWARD}")
            print(f"   max_steps: {(GRID_SIZE-1)*2 * 3} (3× Manhattan óptimo={((GRID_SIZE-1)*2)})")
            print("="*70)
            
            env, agent = create_env_agent(seed, GRID_SIZE)
            
            config_start = time.time()
            
            if group_name == 'ControlS0':
                results = run_control_group(env, agent, seed, group_config['max_episodes'])
            elif group_name == 'AdaptiveCurriculum':
                results = run_adaptive_curriculum(env, agent, seed, group_config['max_episodes'])
            
            config_duration = (time.time() - config_start) / 60
            
            # Guardar CSV
            df = pd.DataFrame(results)
            csv_path = output_dir / f"validation4x4_{group_name}_seed{seed}_episodes.csv"
            df.to_csv(csv_path, index=False)
            print(f"\n📁 Guardado: {csv_path.name}")
            
            # Calcular métricas agregadas
            last_50 = results[-50:] if len(results) >= 50 else results
            metrics_summary = {
                'group': group_name,
                'seed': seed,
                'grid_size': GRID_SIZE,
                'episodes': len(results),
                'success_rate': np.mean([r['goal_reached'] for r in last_50]) * 100,
                'reward_env_mean': np.mean([r['reward_env'] for r in last_50]),
                'reward_env_std': np.std([r['reward_env'] for r in last_50]),
                'steps_mean': np.mean([r['steps'] for r in last_50]),
                'resources_mean': np.mean([r['resources_final'] for r in last_50]),
                'starvation_rate': np.mean([r['starvation'] for r in last_50]) * 100,  # FIX #3
                'tripwires_mean': np.mean([r['tripwires'] for r in last_50]),
                'duration_min': config_duration
            }
            
            # Guardar JSON
            if group_name == 'AdaptiveCurriculum' and results:
                metrics_summary['curriculum_transitions'] = results[0].get('transitions', [])
            
            json_path = output_dir / f"validation4x4_{group_name}_seed{seed}_metrics.json"
            with open(json_path, 'w') as f:
                json.dump(metrics_summary, f, indent=2, cls=NumpyEncoder)
            print(f"📁 Guardado: {json_path.name}")
            
            # Print summary
            print(f"\n📊 RESULTADOS VALIDACIÓN {group_name}:")
            print(f"   Reward env (final 50): {metrics_summary['reward_env_mean']:.2f} ± {metrics_summary['reward_env_std']:.2f}")
            print(f"   Success rate (final 50): {metrics_summary['success_rate']:.1f}%")
            print(f"   Steps mean (final 50): {metrics_summary['steps_mean']:.1f} (vs Manhattan=6, max=18)")
            print(f"   Resources mean (final 50): {metrics_summary['resources_mean']:.2f}")
            print(f"   Starvation rate (final 50): {metrics_summary['starvation_rate']:.1f}%  [FIX #3 validación]")
            print(f"   Tripwires (mean): {metrics_summary['tripwires_mean']:.2f}")
            print(f"   N episodios: {len(results)}")
            print(f"   Duración: {config_duration:.2f} min")
            print()
            
            all_results[f"{group_name}_seed{seed}"] = metrics_summary
    
    # Resumen final
    total_duration = (time.time() - start_time) / 60
    
    print("\n" + "="*70)
    print("✅ VALIDACIÓN 4×4 POST-FIXES COMPLETADA")
    print("="*70)
    print(f"   Configs ejecutadas: {total_configs}")
    print(f"   Tiempo total: {total_duration:.2f} min")
    print(f"   Output directory: {output_dir}")
    print()
    
    # Calcular promedios por grupo
    print("📊 RESUMEN POR GRUPO:")
    for group_name in GROUPS.keys():
        group_results = [v for k, v in all_results.items() if group_name in k]
        if group_results:
            avg_success = np.mean([r['success_rate'] for r in group_results])
            avg_reward = np.mean([r['reward_env_mean'] for r in group_results])
            avg_steps = np.mean([r['steps_mean'] for r in group_results])
            avg_starvation = np.mean([r['starvation_rate'] for r in group_results])
            print(f"   {group_name:20s}: success={avg_success:5.1f}%, reward={avg_reward:6.2f}, steps={avg_steps:.1f}, starvation={avg_starvation:.1f}%")
    
    # Evaluar gates validación
    control_results = [v for k, v in all_results.items() if 'ControlS0' in k]
    adaptive_results = [v for k, v in all_results.items() if 'Adaptive' in k]
    
    if control_results and adaptive_results:
        control_success = np.mean([r['success_rate'] for r in control_results])
        adaptive_success = np.mean([r['success_rate'] for r in adaptive_results])
        control_reward = np.mean([r['reward_env_mean'] for r in control_results])
        adaptive_reward = np.mean([r['reward_env_mean'] for r in adaptive_results])
        
        gates_passed = evaluate_gates_validation(
            control_success, adaptive_success, 
            control_reward, adaptive_reward
        )
        
        # Diagnóstico fixes
        print("\n📈 DIAGNÓSTICO FIXES:")
        control_starvation = np.mean([r['starvation_rate'] for r in control_results])
        control_resources = np.mean([r['resources_mean'] for r in control_results])
        
        if control_starvation > 5:
            print(f"   ✅ FIX #3 funciona: {control_starvation:.1f}% muerte por inanición")
        else:
            print(f"   ⚠️  FIX #3 dudoso: {control_starvation:.1f}% inanición (esperado >5%)")
        
        if 0 <= control_reward <= 10:
            print(f"   ✅ FIX #2 funciona: reward {control_reward:.2f} rango esperado (sin +25)")
        else:
            print(f"   ⚠️  FIX #2 dudoso: reward {control_reward:.2f} fuera rango esperado")
        
        if 10 <= np.mean([r['steps_mean'] for r in control_results]) <= 18:
            print(f"   ✅ FIX #1 funciona: steps exploración {np.mean([r['steps_mean'] for r in control_results]):.1f} dentro margen (6-18)")
        else:
            print(f"   ⚠️  FIX #1 dudoso: steps {np.mean([r['steps_mean'] for r in control_results]):.1f} fuera margen esperado")
        
        print()


if __name__ == "__main__":
    main()
