"""
Análisis Temporal v9: Degradación por Etapas
=============================================

Análisis preregistrado para validar Hipótesis H9.4:
- H9.4: Degradación gradual (NO súbita) a través de etapas curriculum

Métodos:
- Ratios por etapa (1, 2, 3, 4)
- Pendientes inter-etapas
- Detección saltos anómalos (colapso súbito etapa 4)
- Transfer efficiency entre etapas

Uso:
    python scripts/analyze_temporal_stages.py

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
Preregistro: results/pgf_v9/PREREGISTRO_v9.md v1.0
"""

import sys
import os
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# Agregar directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================================
# CONFIGURACIÓN
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


RESULTS_DIR = Path('results/pgf_v9/resultados')
OUTPUT_DIR = Path('results/pgf_v9/analisis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = [42, 123, 456]


# ============================================================================
# ANÁLISIS POR ETAPAS
# ============================================================================

def load_curriculum_data():
    """
    Carga datos Curriculum de todas las seeds.
    
    Returns:
        dict: {seed: DataFrame}
    """
    data = {}
    
    for seed in SEEDS:
        csv_path = RESULTS_DIR / f"exp9_Curriculum_seed{seed}_episodes.csv"
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV no encontrado: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Validar que tiene columna stage
        if 'stage' not in df.columns:
            raise ValueError(f"{csv_path.name}: falta columna 'stage'")
        
        # Verificar que tiene 4 etapas
        stages_present = df['stage'].dropna().unique()
        if len(stages_present) != 4:
            raise ValueError(f"{csv_path.name}: esperado 4 etapas, encontrado {len(stages_present)}")
        
        data[seed] = df
        print(f"✓ Cargado: {csv_path.name} ({len(df)} episodios, {len(stages_present)} etapas)")
    
    return data


def analyze_by_stage(df_curriculum, seed):
    """
    Analiza métricas por etapa para una seed.
    
    Args:
        df_curriculum: DataFrame con columna 'stage'
        seed: int
    
    Returns:
        dict con métricas por etapa
    """
    stage_metrics = {}
    
    for stage_num in [1, 2, 3, 4]:
        df_stage = df_curriculum[df_curriculum['stage'] == stage_num]
        
        if len(df_stage) == 0:
            print(f"  ⚠️  Seed {seed}: Stage {stage_num} vacío")
            continue
        
        stage_metrics[stage_num] = {
            'n_episodes': int(len(df_stage)),
            'mean_reward_env': float(df_stage['total_reward_env'].mean()),
            'std_reward_env': float(df_stage['total_reward_env'].std()),
            'mean_reward_shaped': float(df_stage['total_reward_shaped'].mean()),
            'mean_tripwires': float(df_stage['tripwires_triggered'].mean()),
            'mean_resources': float(df_stage['resources_collected'].mean()),
            'success_rate': float(df_stage['goal_reached'].mean()),
            'survival_rate': float(1 - df_stage['deaths_starvation'].mean()),
            'epsilon_start': float(df_stage.iloc[0]['epsilon']),
            'epsilon_end': float(df_stage.iloc[-1]['epsilon']),
            'shaping_scale': float(df_stage.iloc[0]['shaping_scale_current'])
        }
    
    return stage_metrics


def compute_stage_slopes(stage_metrics):
    """
    Calcula pendientes (slopes) entre etapas consecutivas.
    
    Args:
        stage_metrics: dict {stage_num: metrics}
    
    Returns:
        dict con slopes inter-etapas
    """
    slopes = {}
    
    for stage_num in [1, 2, 3]:
        next_stage = stage_num + 1
        
        if stage_num in stage_metrics and next_stage in stage_metrics:
            reward_diff = (stage_metrics[next_stage]['mean_reward_env'] - 
                          stage_metrics[stage_num]['mean_reward_env'])
            
            slopes[f'stage_{stage_num}_to_{next_stage}'] = float(reward_diff)
    
    return slopes


def detect_sudden_collapse(stage_metrics, threshold=-50):
    """
    Detecta si hubo colapso súbito en etapa final.
    
    Args:
        stage_metrics: dict {stage_num: metrics}
        threshold: Caída de reward considerada "colapso" (default: -50)
    
    Returns:
        dict con detección colapso
    """
    if 3 not in stage_metrics or 4 not in stage_metrics:
        return {'sudden_collapse': False, 'reason': 'missing_stages'}
    
    reward_stage3 = stage_metrics[3]['mean_reward_env']
    reward_stage4 = stage_metrics[4]['mean_reward_env']
    drop = reward_stage4 - reward_stage3
    
    collapsed = drop < threshold
    
    return {
        'sudden_collapse': bool(collapsed),
        'reward_stage3': float(reward_stage3),
        'reward_stage4': float(reward_stage4),
        'drop': float(drop),
        'threshold': threshold
    }


def compute_transfer_efficiency(stage_metrics):
    """
    Calcula eficiencia de transferencia entre etapas.
    
    Transfer efficiency = (reward_final_etapa_i / reward_final_etapa_i-1)
    
    Args:
        stage_metrics: dict {stage_num: metrics}
    
    Returns:
        dict con transfer efficiencies
    """
    efficiencies = {}
    
    for stage_num in [2, 3, 4]:
        prev_stage = stage_num - 1
        
        if prev_stage in stage_metrics and stage_num in stage_metrics:
            prev_reward = stage_metrics[prev_stage]['mean_reward_env']
            curr_reward = stage_metrics[stage_num]['mean_reward_env']
            
            # Evitar división por cero
            if prev_reward > 0:
                efficiency = curr_reward / prev_reward
            else:
                efficiency = np.nan
            
            efficiencies[f'stage_{prev_stage}_to_{stage_num}'] = float(efficiency)
    
    return efficiencies


# ============================================================================
# AGREGACIÓN CROSS-SEEDS
# ============================================================================

def aggregate_stage_metrics(all_seed_data):
    """
    Agrega métricas por etapa a través de seeds.
    
    Args:
        all_seed_data: dict {seed: {stage_num: metrics}}
    
    Returns:
        dict con agregados por etapa
    """
    aggregated = {}
    
    for stage_num in [1, 2, 3, 4]:
        rewards_stage = []
        success_rates_stage = []
        
        for seed, stage_data in all_seed_data.items():
            if stage_num in stage_data:
                rewards_stage.append(stage_data[stage_num]['mean_reward_env'])
                success_rates_stage.append(stage_data[stage_num]['success_rate'])
        
        if rewards_stage:
            aggregated[stage_num] = {
                'n_seeds': len(rewards_stage),
                'mean_reward_env': float(np.mean(rewards_stage)),
                'std_reward_env': float(np.std(rewards_stage, ddof=1)),
                'min_reward_env': float(np.min(rewards_stage)),
                'max_reward_env': float(np.max(rewards_stage)),
                'mean_success_rate': float(np.mean(success_rates_stage)),
                'std_success_rate': float(np.std(success_rates_stage, ddof=1))
            }
    
    return aggregated


def test_gradual_vs_sudden(aggregated_metrics):
    """
    Test estadístico: ¿degradación es gradual (lineal) o hay salto súbito etapa 4?
    
    Args:
        aggregated_metrics: dict {stage_num: metrics}
    
    Returns:
        dict con test results
    """
    stages = [1, 2, 3, 4]
    rewards = [aggregated_metrics[s]['mean_reward_env'] for s in stages]
    
    # Ajuste lineal (modelo gradual)
    slope, intercept, r_value, p_value, std_err = stats.linregress(stages, rewards)
    
    # Residuo etapa 4 (si muy negativo → colapso súbito)
    predicted_stage4 = slope * 4 + intercept
    residual_stage4 = rewards[3] - predicted_stage4
    
    # ¿Residuo significativamente negativo?
    sudden_collapse = residual_stage4 < -20  # Threshold pragmático
    
    return {
        'linear_model': {
            'slope': float(slope),
            'intercept': float(intercept),
            'r_squared': float(r_value**2),
            'p_value': float(p_value)
        },
        'stage4_residual': float(residual_stage4),
        'stage4_predicted': float(predicted_stage4),
        'stage4_observed': float(rewards[3]),
        'sudden_collapse_detected': bool(sudden_collapse),
        'interpretation': 'GRADUAL' if not sudden_collapse else 'SUDDEN_COLLAPSE'
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*70)
    print("ANÁLISIS TEMPORAL POR ETAPAS (v9)")
    print("="*70)
    print(f"\nOutput: {OUTPUT_DIR}")
    
    # Cargar datos Curriculum
    print("\n[1/5] Cargando datos Curriculum...")
    curriculum_data = load_curriculum_data()
    
    print(f"\n✓ Datos cargados: {len(SEEDS)} seeds")
    
    # Analizar por seed
    print("\n[2/5] Analizando métricas por etapa y seed...")
    all_seed_stage_data = {}
    
    for seed in SEEDS:
        print(f"\n  Seed {seed}:")
        stage_metrics = analyze_by_stage(curriculum_data[seed], seed)
        slopes = compute_stage_slopes(stage_metrics)
        collapse = detect_sudden_collapse(stage_metrics)
        transfer_eff = compute_transfer_efficiency(stage_metrics)
        
        all_seed_stage_data[seed] = {
            'stage_metrics': stage_metrics,
            'slopes': slopes,
            'collapse_detection': collapse,
            'transfer_efficiency': transfer_eff
        }
        
        # Logging
        for stage_num in [1, 2, 3, 4]:
            if stage_num in stage_metrics:
                metrics = stage_metrics[stage_num]
                print(f"    Stage {stage_num}: reward={metrics['mean_reward_env']:.1f}, success={metrics['success_rate']:.0%}")
        
        if collapse['sudden_collapse']:
            print(f"    ⚠️  COLAPSO DETECTADO etapa 3→4: {collapse['drop']:.1f}")
    
    # Agregar cross-seeds
    print("\n[3/5] Agregando métricas cross-seeds...")
    aggregated = aggregate_stage_metrics(
        {seed: data['stage_metrics'] for seed, data in all_seed_stage_data.items()}
    )
    
    print("\n  Agregados por etapa:")
    for stage_num in [1, 2, 3, 4]:
        if stage_num in aggregated:
            agg = aggregated[stage_num]
            print(f"    Stage {stage_num}: {agg['mean_reward_env']:.1f} ± {agg['std_reward_env']:.1f} (N={agg['n_seeds']})")
    
    # Test gradual vs súbito
    print("\n[4/5] Test degradación gradual vs súbita...")
    gradual_test = test_gradual_vs_sudden(aggregated)
    
    print(f"\n  Modelo lineal:")
    print(f"    Slope:      {gradual_test['linear_model']['slope']:.2f} reward/stage")
    print(f"    R²:         {gradual_test['linear_model']['r_squared']:.3f}")
    print(f"    p-value:    {gradual_test['linear_model']['p_value']:.4f}")
    
    print(f"\n  Residuo etapa 4:")
    print(f"    Predicho:   {gradual_test['stage4_predicted']:.1f}")
    print(f"    Observado:  {gradual_test['stage4_observed']:.1f}")
    print(f"    Residuo:    {gradual_test['stage4_residual']:.1f}")
    
    if gradual_test['sudden_collapse_detected']:
        print(f"\n  ⚠️  COLAPSO SÚBITO DETECTADO en etapa 4")
        print(f"      H9.4 RECHAZADA: No degradación gradual")
    else:
        print(f"\n  ✅ DEGRADACIÓN GRADUAL detectada")
        print(f"      H9.4 VALIDADA: Pendiente uniforme")
    
    # Compilar resultados
    results = {
        'analysis': 'temporal_stages',
        'experiment': 'v9',
        'date': '2025-12-03',
        'n_seeds': len(SEEDS),
        'by_seed': all_seed_stage_data,
        'aggregated': aggregated,
        'gradual_test': gradual_test,
        'hypothesis_h94': {
            'description': 'Degradación gradual (NO súbita) a través de etapas',
            'validated': not gradual_test['sudden_collapse_detected'],
            'interpretation': gradual_test['interpretation']
        }
    }
    
    # Guardar JSON
    print("\n[5/5] Guardando resultados...")
    json_path = OUTPUT_DIR / "temporal_stages.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    
    print(f"✓ Resultados guardados: {json_path.name}")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN H9.4")
    print("="*70)
    print(f"\n✅ H9.4 (Degradación gradual): {results['hypothesis_h94']['interpretation']}")
    
    # Conteo colapsos
    collapses = sum(1 for seed_data in all_seed_stage_data.values() 
                   if seed_data['collapse_detection']['sudden_collapse'])
    print(f"\n📊 Seeds con colapso súbito: {collapses}/{len(SEEDS)}")
    
    if collapses > 0:
        print(f"\n⚠️  OBSERVACIÓN CRÍTICA:")
        print(f"    {collapses} seed(s) colapsaron súbitamente en etapa 4.")
        print(f"    Sugiere que s=1.0 es inherentemente frágil.")


if __name__ == '__main__':
    main()
