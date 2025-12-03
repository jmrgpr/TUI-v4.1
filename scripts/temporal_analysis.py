"""
Análisis Temporal - Learning Curves por Tramos
Experimento v8: ¿Cuándo emerge el over-alignment?

Método: Descomposición temporal en tramos de 100 episodios
Objetivo: Detectar si degradación es gradual (learning) o súbita (colapso)
Preregistrado en: PREREGISTRO_v8.md §Plan de Análisis Estadístico
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
RESULTS_DIR = Path("results/pgf_v8/resultados")
OUTPUT_DIR = Path("results/pgf_v8/analisis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_episode_data():
    """Cargar todos los episodios individuales"""
    all_data = []
    
    shaping_levels = [0.0, 0.25, 0.5, 1.0]
    spawn_rates = [0.25, 0.40]
    seeds = [42, 123, 456]
    
    for shaping in shaping_levels:
        for spawn in spawn_rates:
            for seed in seeds:
                csv_path = RESULTS_DIR / f"exp8_shaping{shaping}_spawn{spawn}_seed{seed}_episodes.csv"
                
                if not csv_path.exists():
                    continue
                
                df = pd.read_csv(csv_path)
                df['shaping_scale'] = shaping
                df['spawn_rate'] = spawn
                df['seed'] = seed
                all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

def compute_temporal_ratios(df):
    """Calcular ratios por tramos temporales"""
    
    # Definir tramos
    tramos = {
        'exploration': (1, 100),
        'convergence': (101, 200),
        'stability': (201, 300)
    }
    
    results = []
    
    for shaping in sorted(df['shaping_scale'].unique()):
        for spawn in sorted(df['spawn_rate'].unique()):
            for seed in sorted(df['seed'].unique()):
                # Filtrar config
                config_mask = (df['shaping_scale'] == shaping) & \
                              (df['spawn_rate'] == spawn) & \
                              (df['seed'] == seed)
                
                config_df = df[config_mask]
                
                if len(config_df) == 0:
                    continue
                
                for tramo_name, (ep_start, ep_end) in tramos.items():
                    # Filtrar tramo
                    tramo_mask = (config_df['episode'] >= ep_start) & \
                                 (config_df['episode'] <= ep_end)
                    tramo_df = config_df[tramo_mask]
                    
                    # PGF vs Control en tramo
                    pgf = tramo_df[tramo_df['agent_type'] == 'PGF']
                    ctrl = tramo_df[tramo_df['agent_type'] == 'Control']
                    
                    pgf_reward = pgf['total_reward_env'].mean()
                    ctrl_reward = ctrl['total_reward_env'].mean()
                    
                    ratio = pgf_reward / ctrl_reward if ctrl_reward > 0 else np.nan
                    
                    # Métricas adicionales
                    pgf_tripwires = pgf['tripwires_triggered'].mean()
                    ctrl_tripwires = ctrl['tripwires_triggered'].mean()
                    tripwires_ratio = pgf_tripwires / ctrl_tripwires if ctrl_tripwires > 0.1 else np.nan
                    
                    pgf_success = pgf['goal_reached'].mean()
                    ctrl_success = ctrl['goal_reached'].mean()
                    
                    results.append({
                        'shaping_scale': shaping,
                        'spawn_rate': spawn,
                        'seed': seed,
                        'tramo': tramo_name,
                        'episode_range': f"{ep_start}-{ep_end}",
                        'ratio_reward_env': ratio,
                        'ratio_tripwires': tripwires_ratio,
                        'pgf_success_rate': pgf_success,
                        'ctrl_success_rate': ctrl_success,
                        'pgf_reward': pgf_reward,
                        'ctrl_reward': ctrl_reward
                    })
    
    return pd.DataFrame(results)

def analyze_temporal_patterns(df):
    """Analizar patrones temporales"""
    
    print("="*60)
    print("TEMPORAL ANALYSIS - Experimento v8")
    print("="*60)
    
    # Agrupar por shaping y tramo (promediar seeds y spawn_rates)
    temporal_agg = df.groupby(['shaping_scale', 'tramo']).agg({
        'ratio_reward_env': ['mean', 'std'],
        'ratio_tripwires': ['mean', 'std'],
        'pgf_success_rate': 'mean',
        'ctrl_success_rate': 'mean'
    }).reset_index()
    
    # Aplanar columnas
    temporal_agg.columns = ['shaping_scale', 'tramo', 
                            'ratio_reward_mean', 'ratio_reward_std',
                            'ratio_tripwires_mean', 'ratio_tripwires_std',
                            'pgf_success_rate', 'ctrl_success_rate']
    
    print("\n📊 Ratios por tramo temporal:")
    
    # Ordenar tramos
    tramo_order = {'exploration': 1, 'convergence': 2, 'stability': 3}
    temporal_agg['tramo_order'] = temporal_agg['tramo'].map(tramo_order)
    temporal_agg = temporal_agg.sort_values(['shaping_scale', 'tramo_order'])
    
    for shaping in sorted(temporal_agg['shaping_scale'].unique()):
        print(f"\n   s = {shaping}:")
        subset = temporal_agg[temporal_agg['shaping_scale'] == shaping]
        for _, row in subset.iterrows():
            print(f"      {row['tramo']:12s}: ratio = {row['ratio_reward_mean']:.3f} ± {row['ratio_reward_std']:.3f}")
    
    # Detectar tendencias
    print("\n🔍 Detección de tendencias:")
    
    tendencias = []
    for shaping in sorted(temporal_agg['shaping_scale'].unique()):
        subset = temporal_agg[temporal_agg['shaping_scale'] == shaping].sort_values('tramo_order')
        ratios = subset['ratio_reward_mean'].values
        
        if len(ratios) < 3:
            continue
        
        # Calcular pendiente (linreg simple)
        x = np.arange(len(ratios))
        slope = np.polyfit(x, ratios, 1)[0]
        
        # Delta first-to-last
        delta = ratios[-1] - ratios[0]
        
        # Clasificar tendencia
        if abs(delta) < 0.05:
            tendencia = 'estable'
            emoji = '⚪'
        elif delta > 0:
            tendencia = 'mejora' if delta > 0.10 else 'leve_mejora'
            emoji = '🟢'
        else:
            tendencia = 'degradación' if delta < -0.10 else 'leve_degradación'
            emoji = '🔴' if delta < -0.10 else '🟡'
        
        print(f"   s = {shaping}: {emoji} {tendencia} (Δ = {delta:+.3f}, slope = {slope:+.4f})")
        
        tendencias.append({
            'shaping_scale': shaping,
            'trend': tendencia,
            'delta': float(delta),
            'slope': float(slope),
            'initial_ratio': float(ratios[0]),
            'final_ratio': float(ratios[-1])
        })
    
    return temporal_agg, tendencias

def temporal_analysis():
    """Análisis temporal completo"""
    
    # Cargar datos
    print("\n📂 Cargando episodios individuales...")
    df = load_episode_data()
    print(f"✅ {len(df)} episodios cargados")
    
    # Calcular ratios temporales
    print("\n⏱️ Calculando ratios por tramos...")
    temporal_df = compute_temporal_ratios(df)
    print(f"✅ {len(temporal_df)} mediciones temporales")
    
    # Analizar patrones
    temporal_agg, tendencias = analyze_temporal_patterns(temporal_df)
    
    # Preparar output
    output = {
        'experiment': 'v8',
        'analysis': 'temporal_learning_curves',
        'date': '2025-12-03',
        'tramos_definition': {
            'exploration': '1-100 episodes',
            'convergence': '101-200 episodes',
            'stability': '201-300 episodes'
        },
        'temporal_ratios_aggregated': temporal_agg.to_dict(orient='records'),
        'trends_by_shaping': tendencias,
        'interpretation': {
            's=0.0': 'Control negativo - esperamos estabilidad en ~1.0',
            's=0.25': 'Shaping leve - posible leve degradación',
            's=0.5': 'Shaping moderado - degradación esperada',
            's=1.0': 'Shaping extremo - over-alignment, ¿súbito o gradual?'
        },
        'key_findings': []
    }
    
    # Análisis específico s=1.0
    s1_trend = next((t for t in tendencias if t['shaping_scale'] == 1.0), None)
    if s1_trend:
        if s1_trend['delta'] < -0.10:
            finding = f"Over-alignment emerge gradualmente: ratio degrada de {s1_trend['initial_ratio']:.3f} → {s1_trend['final_ratio']:.3f} (Δ = {s1_trend['delta']:.3f})"
        else:
            finding = f"Over-alignment súbito desde inicio: ratio estable ~{s1_trend['final_ratio']:.3f} (Δ = {s1_trend['delta']:.3f})"
        
        output['key_findings'].append(finding)
        print(f"\n💡 Hallazgo s=1.0: {finding}")
    
    # Análisis control negativo
    s0_trend = next((t for t in tendencias if t['shaping_scale'] == 0.0), None)
    if s0_trend:
        if abs(s0_trend['delta']) < 0.05:
            finding = f"Control negativo ESTABLE: ratio ~{s0_trend['final_ratio']:.3f} (validación H8.3)"
        else:
            finding = f"⚠️ Control negativo INESTABLE: drift {s0_trend['delta']:+.3f} (posible problema)"
        
        output['key_findings'].append(finding)
        print(f"💡 Hallazgo s=0.0: {finding}")
    
    # Guardar
    output_path = OUTPUT_DIR / "temporal_analysis.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Guardado: {output_path}")
    
    return output

if __name__ == "__main__":
    results = temporal_analysis()
    
    print("\n" + "="*60)
    print("CONCLUSIÓN")
    print("="*60)
    for finding in results['key_findings']:
        print(f"  • {finding}")
    print("="*60)
