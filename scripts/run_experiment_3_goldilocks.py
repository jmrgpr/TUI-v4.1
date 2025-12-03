"""
Script de ejecución automática para Experimento 3: Caracterización Curva Goldilocks (PGF v6)

Ejecuta barrido fino de densidades (5 niveles) con mayor N (300 eps/agente).
Valida hipótesis de parábola invertida con máximo en D intermedia.

Uso:
    python scripts/run_experiment_3_goldilocks.py
"""
import sys
import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.environment_v2 import ResourceDensityEnv
from sim.dqn_agent import DQNAgent


def run_experiment_goldilocks(
    grid_size=4,
    spawn_rate=0.2,
    episodes=300,
    seed=42,
    risk_scale=1.5,
    output_prefix="results/pgf_v6/resultados/exp3_goldilocks"
):
    """
    Ejecuta experimento Goldilocks con episodios separados por agente.
    
    Args:
        grid_size: Tamaño del grid (fijo en 4)
        spawn_rate: Tasa de spawn de recursos (ρ) - Variable clave v6
        episodes: Número de episodios POR AGENTE (300 PGF + 300 Control)
        seed: Semilla aleatoria
        risk_scale: Escala de penalización de riesgo
        output_prefix: Prefijo para archivos de salida
    
    Returns:
        dict con resultados y metadata
    """
    print(f"\n{'='*80}")
    print(f"🧪 EXPERIMENTO 3 - CURVA GOLDILOCKS (PGF v6)")
    print(f"{'='*80}")
    print(f"Grid: {grid_size}x{grid_size} | Spawn Rate: {spawn_rate} | Seed: {seed}")
    print(f"Episodes: {episodes} PGF + {episodes} Control | Risk Scale: {risk_scale}")
    print(f"{'='*80}\n")
    
    # Configurar semillas
    np.random.seed(seed)
    
    # Crear entorno v2 con PARÁMETROS ENDURECIDOS V3 (congelados para v6)
    env = ResourceDensityEnv(
        size=grid_size,
        risk_scale=risk_scale,
        resource_spawn_rate=spawn_rate,
        resource_reward=1.0,         # Calibrado v5
        max_resources_on_grid=3,     # Escasez real
        step_cost=-0.3,              # Castigo fuerte vagabundeo
        resource_decay_steps=5       # Recursos caducan rápido
    )
    
    print(f"✓ Entorno v3 creado: grid {env.size}x{env.size}, spawn_rate={spawn_rate}")
    print(f"  Parámetros: reward={env.resource_reward}, max_res={env.max_resources_on_grid}")
    print(f"              step_cost={env.step_cost}, decay={env.resource_decay_steps}\n")
    
    # Crear agentes
    state = env.reset()
    state_dim = len([v for _, v in state])
    action_dim = 4  # up, down, left, right
    
    agent_pgf = DQNAgent(state_dim, action_dim)
    agent_control = DQNAgent(state_dim, action_dim)
    
    print(f"✓ Agentes creados: state_dim={state_dim}, action_dim={action_dim}\n")
    
    # Mapeo de acciones
    actions_map = ['up', 'down', 'left', 'right']
    
    # Listas para almacenar resultados
    results_pgf = []
    results_control = []
    episodes_data = []
    
    # EPISODIOS SEPARADOS POR AGENTE (corrección v5 → v6)
    for agent_type in ["PGF", "Control"]:
        agent = agent_pgf if agent_type == "PGF" else agent_control
        
        print(f"\n{'─'*80}")
        print(f"🤖 Entrenando agente {agent_type} ({episodes} episodios)")
        print(f"{'─'*80}\n")
        
        for ep in range(episodes):
            # Reset
            state = env.reset()
            done = False
            total_reward = 0
            steps = 0
            resources_collected = 0
            
            # Episode loop
            while not done:
                # Convertir estado a vector
                state_vec = np.array([v for _, v in state], dtype=np.float32)
                action_idx = agent.act(state_vec)
                action = actions_map[action_idx]
                
                next_state, reward, done, info = env.step(action)
                
                # Remember transition
                next_state_vec = np.array([v for _, v in next_state], dtype=np.float32)
                agent.remember(state_vec, action_idx, reward, next_state_vec, done)
                agent.learn()
                
                state = next_state
                total_reward += reward
                steps += 1
                
                if info.get('resource_collected', False):
                    resources_collected += 1
            
            # Calcular D_efectiva al final del episodio
            density_metrics = env.compute_D_effective()
            
            # Guardar resultado
            episode_result = {
                'episode': ep + 1,
                'agent': agent_type,
                'total_reward': total_reward,
                'steps': steps,
                'resources_collected': resources_collected,
                'final_resources': env.resources,
                'D_effective': density_metrics['D_effective'],
                'rho': density_metrics['rho'],
                'p_acceso': density_metrics['p_acceso'],
                'tau_consumo': density_metrics['tau_consumo'],
                'cells_visited': density_metrics['cells_visited'],
            }
            
            episodes_data.append(episode_result)
            
            if agent_type == "PGF":
                results_pgf.append(total_reward)
            else:
                results_control.append(total_reward)
            
            # Log progreso cada 50 episodios
            if (ep + 1) % 50 == 0:
                avg = np.mean(results_pgf[-50:]) if agent_type == "PGF" else np.mean(results_control[-50:])
                print(f"[{agent_type}] Episode {ep+1}/{episodes} | Avg reward: {avg:.2f} | D_eff: {density_metrics['D_effective']:.3f}")
    
    # Calcular estadísticas finales
    mean_pgf = np.mean(results_pgf) if results_pgf else 0
    mean_control = np.mean(results_control) if results_control else 0
    ratio_pgf_control = (mean_pgf / mean_control * 100) if mean_control != 0 else 0
    
    # D_efectiva promedio del experimento
    D_effective_mean = np.mean([ep['D_effective'] for ep in episodes_data])
    
    print(f"\n{'='*80}")
    print(f"📊 RESULTADOS FINALES")
    print(f"{'='*80}")
    print(f"PGF Mean Reward:     {mean_pgf:.2f}")
    print(f"Control Mean Reward: {mean_control:.2f}")
    print(f"Ratio PGF/Control:   {ratio_pgf_control:.2f}%")
    print(f"D_efectiva Media:    {D_effective_mean:.3f}")
    print(f"{'='*80}\n")
    
    # Metadata completa
    metadata = {
        'experiment': 'PGF_v6_Experimento_3_Goldilocks',
        'version': 'v4.3_candidate',
        'timestamp': datetime.now().isoformat(),
        'config': {
            'grid_size': grid_size,
            'spawn_rate': spawn_rate,
            'episodes': episodes,
            'seed': seed,
            'risk_scale': risk_scale,
            'resource_reward': env.resource_reward,
            'max_resources_on_grid': env.max_resources_on_grid,
            'step_cost': env.step_cost,
            'resource_decay_steps': env.resource_decay_steps,
        },
        'results': {
            'mean_reward_pgf': float(mean_pgf),
            'mean_reward_control': float(mean_control),
            'ratio_pgf_control': float(ratio_pgf_control),
            'D_effective_mean': float(D_effective_mean),
            'n_episodes_pgf': len(results_pgf),
            'n_episodes_control': len(results_control),
        },
        'density_metrics': {
            'rho': spawn_rate,
            'N': grid_size,
            'p_acceso_mean': float(np.mean([ep['p_acceso'] for ep in episodes_data])),
            'tau_consumo_mean': float(np.mean([ep['tau_consumo'] for ep in episodes_data])),
        }
    }
    
    # Guardar archivos
    output_dir = Path(output_prefix).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON con metadata completa
    json_path = f"{output_prefix}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✓ JSON guardado: {json_path}")
    
    # CSV con datos de episodios
    import pandas as pd
    df = pd.DataFrame(episodes_data)
    csv_path = f"{output_prefix}_episodes.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"✓ CSV guardado: {csv_path}")
    
    return metadata


def main():
    """Ejecuta batch completo de Experimento 3 (PGF v6)"""
    print("="*80)
    print("🚀 EXPERIMENTO 3: BARRIDO FINO - CURVA GOLDILOCKS")
    print("="*80)
    print("Configuraciones:")
    print("  - Grid: 4x4 (fijo)")
    print("  - Spawn Rates: 0.05, 0.10, 0.20, 0.30, 0.40 (mapeo completo)")
    print("  - Seeds: 42, 123, 456, 789, 101112")
    print("  - Episodes: 300 PGF + 300 Control = 600 por config")
    print("  - Total: 25 configs × 600 episodes = 15,000 episodes")
    print("  - Economía: step_cost=-0.3, max_resources=3, decay=5 (v3 congelado)")
    print("="*80 + "\n")
    
    # Configuraciones (BATCH COMPLETO v6: 5 densidades × 5 seeds)
    spawn_rates = [0.05, 0.10, 0.20, 0.30, 0.40]  # Barrido fino
    seeds = [42, 123, 456, 789, 101112]            # 5 réplicas
    
    # Configuración fija
    grid_size = 4
    episodes = 300  # Por agente (vs 100 en v5)
    risk_scale = 1.5
    
    results_summary = []
    
    for spawn_rate in spawn_rates:
        for seed in seeds:
            # Nombre descriptivo
            config_name = f"exp3_spawn{spawn_rate}_seed{seed}"
            output_prefix = f"results/pgf_v6/resultados/{config_name}"
            
            # Ejecutar experimento
            try:
                result = run_experiment_goldilocks(
                    grid_size=grid_size,
                    spawn_rate=spawn_rate,
                    episodes=episodes,
                    seed=seed,
                    risk_scale=risk_scale,
                    output_prefix=output_prefix
                )
                
                results_summary.append({
                    'config': config_name,
                    'spawn_rate': spawn_rate,
                    'seed': seed,
                    'ratio_pgf_control': result['results']['ratio_pgf_control'],
                    'D_effective': result['results']['D_effective_mean'],
                })
                
            except Exception as e:
                print(f"❌ Error en {config_name}: {e}")
                continue
    
    # Guardar resumen global
    summary_path = "results/pgf_v6/resultados/experiment_3_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'experiment': 'PGF_v6_Experimento_3_Goldilocks',
            'timestamp': datetime.now().isoformat(),
            'configurations': results_summary,
            'hypothesis': 'ratio_pgf_control sigue parábola invertida con máximo en D intermedia',
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ BATCH COMPLETO - {len(results_summary)} configuraciones ejecutadas")
    print(f"✓ Resumen guardado: {summary_path}")
    print(f"{'='*80}")


if __name__ == "__main__":
    import sys
    
    print("="*80)
    print("🚀 EXPERIMENTO 3: BARRIDO FINO DENSIDADES (Goldilocks) - PGF v6")
    print("="*80)
    print()
    
    # Modo test: 1 config, 50 episodios
    if "--test" in sys.argv:
        print("⚙️  MODO TEST ACTIVADO")
        print("   - 1 configuración: spawn_rate=0.20, seed=42")
        print("   - 50 episodios por agente (100 total)")
        print("   - Duración: ~3-5 minutos")
        print()
        
        config = {
            'spawn_rate': 0.20,
            'seed': 42,
            'episodes': 50
        }
        
        print(f"📊 Ejecutando test: spawn_rate={config['spawn_rate']}, seed={config['seed']}")
        run_experiment_goldilocks(**config)
        
        print("\n✅ TEST COMPLETO")
        print("   Verificar: results/pgf_v6/resultados/exp3_spawn0.20_seed42.json")
        print("\nSi el test pasó, ejecutar batch completo:")
        print("   python scripts/run_experiment_3_goldilocks.py")
    else:
        main()
