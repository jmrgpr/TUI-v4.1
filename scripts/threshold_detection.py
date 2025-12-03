"""
Análisis de Regresión Segmentada - Threshold Detection
Experimento v8: Detección precisa del punto de quiebre s*

Método: Grid search con modelo piecewise, selección AIC
Objetivo: Encontrar s* donde ratio_reward_env cambia de pendiente
Preregistrado en: PREREGISTRO_v8.md §Plan de Análisis Estadístico
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
RESULTS_DIR = Path("results/pgf_v8/resultados")
OUTPUT_DIR = Path("results/pgf_v8/analisis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_data():
    """Cargar todos los CSVs y calcular ratios por config"""
    configs = []
    
    shaping_levels = [0.0, 0.25, 0.5, 1.0]
    spawn_rates = [0.25, 0.40]
    seeds = [42, 123, 456]
    
    for shaping in shaping_levels:
        for spawn in spawn_rates:
            for seed in seeds:
                csv_path = RESULTS_DIR / f"exp8_shaping{shaping}_spawn{spawn}_seed{seed}_episodes.csv"
                
                if not csv_path.exists():
                    print(f"⚠️ Missing: {csv_path.name}")
                    continue
                
                df = pd.read_csv(csv_path)
                
                # Separar PGF y Control
                pgf = df[df['agent_type'] == 'PGF']
                ctrl = df[df['agent_type'] == 'Control']
                
                # Calcular métricas
                pgf_reward = pgf['total_reward_env'].mean()
                ctrl_reward = ctrl['total_reward_env'].mean()
                
                ratio = pgf_reward / ctrl_reward if ctrl_reward > 0 else np.nan
                
                configs.append({
                    'shaping_scale': shaping,
                    'spawn_rate': spawn,
                    'seed': seed,
                    'ratio_reward_env': ratio,
                    'pgf_reward': pgf_reward,
                    'ctrl_reward': ctrl_reward
                })
    
    return pd.DataFrame(configs)

def linear_model(x, y):
    """Modelo lineal simple"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Residual sum of squares
    y_pred = slope * x + intercept
    rss = np.sum((y - y_pred)**2)
    
    # AIC: n*log(RSS/n) + 2*k (k=2 parámetros: slope, intercept)
    n = len(x)
    aic = n * np.log(rss / n) + 2 * 2
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'rss': rss,
        'aic': aic,
        'parameters': 2
    }

def piecewise_model(x, y, breakpoint):
    """Modelo piecewise con quiebre en breakpoint"""
    # Segmento 1: x <= breakpoint
    seg1_mask = x <= breakpoint
    seg2_mask = x > breakpoint
    
    if seg1_mask.sum() < 2 or seg2_mask.sum() < 2:
        # No hay suficientes datos en ambos segmentos
        return None
    
    try:
        # Fit segmento 1 con método robusto
        x1, y1 = x[seg1_mask], y[seg1_mask]
        if len(np.unique(x1)) < 2:
            # No hay variación en x1
            slope1 = 0.0
            intercept1 = np.mean(y1)
        else:
            result1 = stats.linregress(x1, y1)
            slope1, intercept1 = result1.slope, result1.intercept
        
        # Fit segmento 2 con método robusto
        x2, y2 = x[seg2_mask], y[seg2_mask]
        if len(np.unique(x2)) < 2:
            # No hay variación en x2
            slope2 = 0.0
            intercept2 = np.mean(y2)
        else:
            result2 = stats.linregress(x2, y2)
            slope2, intercept2 = result2.slope, result2.intercept
        
        # Calcular RSS total
        y_pred = np.where(x <= breakpoint,
                          slope1 * x + intercept1,
                          slope2 * x + intercept2)
        rss = np.sum((y - y_pred)**2)
        
        # AIC: k=5 parámetros (slope1, intercept1, slope2, intercept2, breakpoint)
        n = len(x)
        if rss <= 0 or n <= 5:
            return None
        
        aic = n * np.log(rss / n) + 2 * 5
        
        return {
            'breakpoint': breakpoint,
            'slope1': slope1,
            'intercept1': intercept1,
            'slope2': slope2,
            'intercept2': intercept2,
            'rss': rss,
            'aic': aic,
            'parameters': 5
        }
    except Exception as e:
        # En caso de error numérico, devolver None
        return None

def grid_search_breakpoint(x, y):
    """Grid search para encontrar mejor breakpoint"""
    # Grid: [0.1, 0.15, 0.2, ..., 0.9]
    candidates = np.arange(0.10, 0.95, 0.05)
    
    results = []
    for bp in candidates:
        result = piecewise_model(x, y, bp)
        if result is not None:
            results.append(result)
    
    if not results:
        return None
    
    # Seleccionar modelo con menor AIC
    best = min(results, key=lambda r: r['aic'])
    return best

def threshold_analysis():
    """Análisis completo de threshold"""
    print("="*60)
    print("THRESHOLD DETECTION - Experimento v8")
    print("="*60)
    
    # Cargar datos
    print("\n📂 Cargando datos...")
    df = load_all_data()
    print(f"✅ {len(df)} configuraciones cargadas")
    
    # Promediar por shaping level (colapsar seeds y spawn_rates)
    df_agg = df.groupby('shaping_scale').agg({
        'ratio_reward_env': ['mean', 'std', 'count']
    }).reset_index()
    df_agg.columns = ['shaping_scale', 'ratio_mean', 'ratio_std', 'n']
    
    print("\n📊 Ratios agregados por shaping level:")
    print(df_agg.to_string(index=False))
    
    # Preparar datos para regresión
    x = df['shaping_scale'].values
    y = df['ratio_reward_env'].values
    
    # Modelo lineal simple
    print("\n📈 Ajustando modelo lineal simple...")
    linear = linear_model(x, y)
    print(f"   Slope: {linear['slope']:.4f}")
    print(f"   R²: {linear['r_squared']:.4f}")
    print(f"   AIC: {linear['aic']:.2f}")
    
    # Modelo piecewise
    print("\n🔍 Buscando breakpoint óptimo...")
    piecewise = grid_search_breakpoint(x, y)
    
    if piecewise is None:
        print("⚠️ No se encontró modelo piecewise válido")
        delta_aic = np.nan
    else:
        print(f"   Breakpoint: s* = {piecewise['breakpoint']:.2f}")
        print(f"   Slope1 (s<s*): {piecewise['slope1']:.4f}")
        print(f"   Slope2 (s>s*): {piecewise['slope2']:.4f}")
        print(f"   AIC: {piecewise['aic']:.2f}")
        
        delta_aic = linear['aic'] - piecewise['aic']
        print(f"\n📉 ΔAIC (linear - piecewise): {delta_aic:.2f}")
        
        if delta_aic > 2:
            print("   ✅ Modelo piecewise SUPERIOR (ΔAIC > 2)")
            print(f"   → Threshold detectado en s* ≈ {piecewise['breakpoint']:.2f}")
        else:
            print("   ⚠️ Evidencia débil para threshold (ΔAIC < 2)")
    
    # Preparar output JSON
    output = {
        'experiment': 'v8',
        'analysis': 'threshold_detection',
        'date': '2025-12-03',
        'data': {
            'n_configs': len(df),
            'shaping_levels': sorted(df['shaping_scale'].unique().tolist()),
            'aggregated_ratios': df_agg.to_dict(orient='records')
        },
        'linear_model': {
            'slope': float(linear['slope']),
            'intercept': float(linear['intercept']),
            'r_squared': float(linear['r_squared']),
            'p_value': float(linear['p_value']),
            'aic': float(linear['aic']),
            'interpretation': 'Modelo simple sin quiebre'
        },
        'piecewise_model': None if piecewise is None else {
            'breakpoint': float(piecewise['breakpoint']),
            'segment1': {
                'slope': float(piecewise['slope1']),
                'intercept': float(piecewise['intercept1']),
                'interpretation': 'Segmento s <= s*'
            },
            'segment2': {
                'slope': float(piecewise['slope2']),
                'intercept': float(piecewise['intercept2']),
                'interpretation': 'Segmento s > s*'
            },
            'aic': float(piecewise['aic']),
            'delta_aic': float(delta_aic),
            'threshold_detected': bool(delta_aic > 2),
            'interpretation': f"Threshold s* = {piecewise['breakpoint']:.2f}" if delta_aic > 2 else "Threshold no concluyente"
        },
        'conclusion': {
            'threshold_exists': bool(piecewise is not None and delta_aic > 2),
            'threshold_value': float(piecewise['breakpoint']) if piecewise is not None else None,
            'evidence_strength': 'strong' if (piecewise is not None and delta_aic > 4) else 'moderate' if (piecewise is not None and delta_aic > 2) else 'weak',
            'summary': f"Threshold detectado en s* ≈ {piecewise['breakpoint']:.2f} con evidencia {'fuerte' if delta_aic > 4 else 'moderada'}" if (piecewise is not None and delta_aic > 2) else "No se detectó threshold claro (modelo lineal suficiente)"
        }
    }
    
    # Guardar
    output_path = OUTPUT_DIR / "threshold_detection.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Guardado: {output_path}")
    
    return output

if __name__ == "__main__":
    results = threshold_analysis()
    
    print("\n" + "="*60)
    print("CONCLUSIÓN")
    print("="*60)
    print(results['conclusion']['summary'])
    print("="*60)
