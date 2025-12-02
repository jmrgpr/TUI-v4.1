"""
Script de ejecución automática para Experimento 2: Manipulación de Densidad (PGF v5)

Ejecuta configuraciones con diferentes spawn_rate en grid 4x4 fijo.
Guarda metadata completa para trazabilidad.

Uso:
    python scripts/run_experiment_2_density.py
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


def run_experiment_with_density(
    grid_size=4,
    spawn_rate=0.5,
    episodes=500,
    seed=42,
    risk_scale=1.5,
    pgf_mix=0.2,
    output_prefix="results/pgf_v5/resultados/exp2_density"
):
    """
    Ejecuta un experimento con configuración de densidad específica.
    
    Args:
        grid_size: Tamaño del grid (fijo en 4 para Exp 2)
        spawn_rate: Tasa de spawn de recursos (ρ) - Variable clave
        episodes: Número de episodios
        seed: Semilla aleatoria
        risk_scale: Escala de penalización de riesgo
        pgf_mix: Proporción de PGF vs Control
        output_prefix: Prefijo para archivos de salida
    
    Returns:
        dict con resultados y metadata
    """
    print(f"\n{'='*80}")
    print(f"🧪 EXPERIMENTO 2 - DENSIDAD DE RECURSOS")
    print(f"{'='*80}")
    print(f"Grid: {grid_size}x{grid_size} | Spawn Rate: {spawn_rate} | Seed: {seed}")
    print(f"Episodes: {episodes} | Risk Scale: {risk_scale} | PGF Mix: {pgf_mix}")
    print(f"{'='*80}\n")
    
    # Configurar semillas
    np.random.seed(seed)
    
    # Crear entorno v2 con densidad controlada
    env = ResourceDensityEnv(
        size=grid_size,
        risk_scale=risk_scale,
        resource_spawn_rate=spawn_rate,
        resource_reward=5.0,
        max_resources_on_grid=10
    )
    
    print(f"✓ Entorno v2 creado: grid {env.size}x{env.size}, spawn_rate={spawn_rate}")
    
    # Crear agentes
    agent_pgf = DQNAgent(env, use_pgf=True, name="PGF")
    agent_control = DQNAgent(env, use_pgf=False, name="Control")
    
    print(f"✓ Agentes creados: PGF + Control\n")
    
    # Listas para almacenar resultados
    results_pgf = []
    results_control = []
    episodes_data = []
    
    # Entrenamiento
    for ep in range(episodes):
        # Decidir qué agente usar (mezcla PGF/Control)
        use_pgf_this_episode = np.random.rand() < pgf_mix
        agent = agent_pgf if use_pgf_this_episode else agent_control
        agent_type = "PGF" if use_pgf_this_episode else "Control"
        
        # Reset
        state = env.reset()
        done = False
        total_reward = 0
        steps = 0
        resources_collected = 0
        
        # Episode loop
        while not done:
            action = agent.act(state, explore=True)
            next_state, reward, done, info = env.step(action)
            
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            
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
            avg_pgf = np.mean(results_pgf[-50:]) if results_pgf else 0
            avg_ctrl = np.mean(results_control[-50:]) if results_control else 0
            print(f"Episode {ep+1}/{episodes} | PGF: {avg_pgf:.2f} | Control: {avg_ctrl:.2f} | D_eff: {density_metrics['D_effective']:.3f}")
    
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
    
    # Metadata completa (LECCIÓN DE PGF v4)
    metadata = {
        'experiment': 'PGF_v5_Experimento_2_Densidad',
        'version': 'v4.3_candidate',
        'timestamp': datetime.now().isoformat(),
        'config': {
            'grid_size': grid_size,
            'spawn_rate': spawn_rate,
            'episodes': episodes,
            'seed': seed,
            'risk_scale': risk_scale,
            'pgf_mix': pgf_mix,
            'resource_reward': 5.0,
            'max_resources_on_grid': 10,
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
    print(f"✓ Guardado: {json_path}")
    
    # CSV con datos de episodios
    csv_path = f"{output_prefix}_episodes.csv"
    import csv
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if episodes_data:
            writer = csv.DictWriter(f, fieldnames=episodes_data[0].keys())
            writer.writeheader()
            writer.writerows(episodes_data)
    print(f"✓ Guardado: {csv_path}")
    
    return metadata


def main():
    """
    Ejecuta batch completo de Experimento 2:
    - 3 configuraciones de densidad (spawn_rate = 0.2, 0.5, 0.8)
    - 3 seeds (42, 123, 456)
    - Total: 9 runs
    """
    print("\n" + "="*80)
    print("🚀 EXPERIMENTO 2: BATCH COMPLETO - MANIPULACIÓN DE DENSIDAD")
    print("="*80)
    print("Configuraciones:")
    print("  - Grid: 4x4 (fijo)")
    print("  - Spawn Rates: 0.2 (baja), 0.5 (media), 0.8 (alta)")
    print("  - Seeds: 42, 123, 456")
    print("  - Episodes: 500 por run")
    print("  - Total: 9 runs × 500 episodes = 4500 episodes")
    print("="*80 + "\n")
    
    # Configuraciones
    spawn_rates = [0.2, 0.5, 0.8]
    seeds = [42, 123, 456]
    
    # Configuración fija
    grid_size = 4
    episodes = 500
    risk_scale = 1.5
    pgf_mix = 0.2
    
    results_summary = []
    
    for spawn_rate in spawn_rates:
        for seed in seeds:
            # Nombre descriptivo
            config_name = f"exp2_grid4x4_spawn{spawn_rate}_seed{seed}"
            output_prefix = f"results/pgf_v5/resultados/{config_name}"
            
            # Ejecutar experimento
            try:
                result = run_experiment_with_density(
                    grid_size=grid_size,
                    spawn_rate=spawn_rate,
                    episodes=episodes,
                    seed=seed,
                    risk_scale=risk_scale,
                    pgf_mix=pgf_mix,
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
    summary_path = "results/pgf_v5/resultados/experiment_2_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'experiment': 'PGF_v5_Experimento_2_Densidad',
            'timestamp': datetime.now().isoformat(),
            'configurations': results_summary,
            'hypothesis': 'ratio_pgf_control es inversamente proporcional a D_effective',
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ BATCH COMPLETO - {len(results_summary)} configuraciones ejecutadas")
    print(f"✓ Resumen guardado: {summary_path}")
    print(f"{'='*80}\n")
    
    # Mostrar tabla de resultados
    print("\n📊 RESUMEN DE RESULTADOS:\n")
    print(f"{'Config':<30} | {'Spawn Rate':<12} | {'D_eff':<10} | {'Ratio':<10}")
    print("-" * 80)
    for r in results_summary:
        print(f"{r['config']:<30} | {r['spawn_rate']:<12.1f} | {r['D_effective']:<10.3f} | {r['ratio_pgf_control']:<10.2f}%")


if __name__ == "__main__":
    main()
