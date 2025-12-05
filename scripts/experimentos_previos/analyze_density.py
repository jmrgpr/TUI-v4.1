"""
Análisis estadístico de Experimento 2: Validación de Hipótesis de Densidad-Riesgo (H-DR)

Calcula:
- D_efectiva para cada configuración
- Ajuste de modelos (v4.1 vs v4.3)
- AIC/BIC, R², IC95% con bootstrap
- Genera figuras

Uso:
    python scripts/analyze_density.py
"""
import sys
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
from sklearn.utils import resample

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_experiment_results(results_dir="results/pgf_v5/resultados"):
    """
    Carga todos los resultados de Experimento 2.
    
    Returns:
        DataFrame con columnas: config, spawn_rate, seed, ratio, D_effective, etc.
    """
    results_dir = Path(results_dir)
    data = []
    
    for json_file in results_dir.glob("exp2_*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        data.append({
            'config': json_file.stem,
            'spawn_rate': result['config']['spawn_rate'],
            'seed': result['config']['seed'],
            'grid_size': result['config']['grid_size'],
            'episodes': result['config']['episodes'],
            'ratio_pgf_control': result['results']['ratio_pgf_control'],
            'D_effective': result['results']['D_effective_mean'],
            'mean_reward_pgf': result['results']['mean_reward_pgf'],
            'mean_reward_control': result['results']['mean_reward_control'],
            'p_acceso': result['density_metrics']['p_acceso_mean'],
            'tau_consumo': result['density_metrics']['tau_consumo_mean'],
        })
    
    df = pd.DataFrame(data)
    print(f"✓ Cargados {len(df)} resultados de {results_dir}")
    return df


def model_v4_1(D, a):
    """Modelo v4.1: ratio es constante (no depende de D)"""
    return a * np.ones_like(D)


def model_v4_3(D, kappa, D0):
    """Modelo v4.3: ratio ∝ 1/(D + D0)"""
    return kappa / (D + D0)


def model_v4_3_log(D, kappa, D0):
    """Modelo alternativo: ratio ∝ 1/log(D + D0)"""
    return kappa / np.log(D + D0)


def compute_aic(residuals, n_params, n_samples):
    """Calcula AIC (Akaike Information Criterion)"""
    rss = np.sum(residuals**2)
    aic = n_samples * np.log(rss / n_samples) + 2 * n_params
    return aic


def compute_bic(residuals, n_params, n_samples):
    """Calcula BIC (Bayesian Information Criterion)"""
    rss = np.sum(residuals**2)
    bic = n_samples * np.log(rss / n_samples) + n_params * np.log(n_samples)
    return bic


def bootstrap_fit(model, D, ratio, n_bootstrap=10000):
    """
    Bootstrap para estimar IC95% de parámetros.
    
    Returns:
        dict con mean y CI95 de cada parámetro
    """
    bootstrap_params = []
    
    for _ in range(n_bootstrap):
        # Resample
        indices = resample(range(len(D)), replace=True)
        D_sample = D[indices]
        ratio_sample = ratio[indices]
        
        try:
            params, _ = curve_fit(model, D_sample, ratio_sample, maxfev=10000)
            bootstrap_params.append(params)
        except:
            continue
    
    bootstrap_params = np.array(bootstrap_params)
    
    # Calcular estadísticas
    if len(bootstrap_params) > 0:
        means = np.mean(bootstrap_params, axis=0)
        ci_lower = np.percentile(bootstrap_params, 2.5, axis=0)
        ci_upper = np.percentile(bootstrap_params, 97.5, axis=0)
        
        return {
            'means': means,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
        }
    else:
        return None


def analyze_hypothesis(df):
    """
    Análisis completo de la Hipótesis de Densidad-Riesgo (H-DR).
    
    H0: ratio es independiente de D_effective
    H1: ratio ∝ 1/(D_effective + D0)
    """
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE HIPÓTESIS DE DENSIDAD-RIESGO (H-DR)")
    print("="*80)
    
    # Datos
    D = df['D_effective'].values
    ratio = df['ratio_pgf_control'].values
    n_samples = len(D)
    
    print(f"\nDatos: {n_samples} configuraciones")
    print(f"Rango D_effective: [{D.min():.3f}, {D.max():.3f}]")
    print(f"Rango ratio: [{ratio.min():.2f}%, {ratio.max():.2f}%]")
    
    # 1. Correlación de Pearson
    r, p_value = pearsonr(D, ratio)
    print(f"\n📈 Correlación de Pearson:")
    print(f"   r = {r:.3f}, p = {p_value:.4f}")
    
    if r < -0.8:
        print("   ✅ Correlación fuerte negativa (H-DR confirmada preliminarmente)")
    elif r < -0.6:
        print("   ⚠️ Correlación moderada negativa (H-DR con evidencia parcial)")
    else:
        print("   ❌ Correlación débil (H-DR no confirmada)")
    
    # 2. Ajuste de modelos
    print(f"\n🔬 Ajuste de Modelos:")
    
    models = {
        'v4.1 (constante)': (model_v4_1, 1),
        'v4.3 (1/(D+D0))': (model_v4_3, 2),
        'v4.3b (1/log(D+D0))': (model_v4_3_log, 2),
    }
    
    results = {}
    
    for name, (model, n_params) in models.items():
        try:
            # Ajustar modelo
            params, _ = curve_fit(model, D, ratio, maxfev=10000)
            predictions = model(D, *params)
            residuals = ratio - predictions
            
            # R²
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((ratio - np.mean(ratio))**2)
            r2 = 1 - (ss_res / ss_tot)
            
            # AIC / BIC
            aic = compute_aic(residuals, n_params, n_samples)
            bic = compute_bic(residuals, n_params, n_samples)
            
            # Bootstrap IC95%
            bootstrap_result = bootstrap_fit(model, D, ratio, n_bootstrap=1000)
            
            results[name] = {
                'params': params,
                'r2': r2,
                'aic': aic,
                'bic': bic,
                'bootstrap': bootstrap_result,
            }
            
            print(f"\n   {name}:")
            print(f"      Parámetros: {params}")
            print(f"      R² = {r2:.3f}")
            print(f"      AIC = {aic:.1f}")
            print(f"      BIC = {bic:.1f}")
            
            if bootstrap_result:
                print(f"      IC95%: {bootstrap_result['ci_lower']} - {bootstrap_result['ci_upper']}")
        
        except Exception as e:
            print(f"\n   {name}: Error en ajuste - {e}")
            results[name] = None
    
    # 3. Comparación de modelos
    print(f"\n🏆 Comparación de Modelos (ΔAIC respecto a v4.1):")
    
    aic_v4_1 = results['v4.1 (constante)']['aic']
    
    for name, result in results.items():
        if result and name != 'v4.1 (constante)':
            delta_aic = result['aic'] - aic_v4_1
            print(f"   {name}: ΔAIC = {delta_aic:.1f}", end="")
            
            if delta_aic < -4:
                print(" ✅ Mejora sustancial")
            elif delta_aic < -2:
                print(" ⚠️ Mejora moderada")
            else:
                print(" ❌ Sin mejora")
    
    # 4. Criterios de éxito
    print(f"\n✅ CRITERIOS DE ÉXITO (Preregistrados):")
    
    r2_v4_3 = results['v4.3 (1/(D+D0))']['r2'] if results['v4.3 (1/(D+D0))'] else 0
    delta_aic_v4_3 = (results['v4.3 (1/(D+D0))']['aic'] - aic_v4_1) if results['v4.3 (1/(D+D0))'] else 0
    
    criteria = {
        'R² > 0.75': r2_v4_3 > 0.75,
        'r < -0.8': r < -0.8,
        'p < 0.05': p_value < 0.05,
        'ΔAIC < -4': delta_aic_v4_3 < -4,
        'ratio_max/ratio_min > 2.5': (ratio.max() / ratio.min()) > 2.5 if ratio.min() > 0 else False,
    }
    
    for criterion, passed in criteria.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {criterion}")
    
    # Veredicto
    n_passed = sum(criteria.values())
    print(f"\n{'='*80}")
    if n_passed >= 4:
        print("🎉 HIPÓTESIS H-DR CONFIRMADA FUERTEMENTE")
        print("   → TUI v4.3 es un upgrade validado")
        print("   → Publicable en Nature Machine Intelligence / Science Robotics")
    elif n_passed >= 3:
        print("⚠️ HIPÓTESIS H-DR CON EVIDENCIA PARCIAL")
        print("   → TUI v4.3 es plausible pero requiere más datos")
        print("   → Publicable en NeurIPS/ICLR con caveats")
    else:
        print("❌ HIPÓTESIS H-DR REFUTADA")
        print("   → La densidad NO explica el valle 4x4")
        print("   → Buscar explicación alternativa (layout, topología, etc.)")
    print("="*80 + "\n")
    
    return results, criteria


def generate_figures(df, results, output_dir="results/pgf_v5/figuras"):
    """Genera figuras para el paper"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    D = df['D_effective'].values
    ratio = df['ratio_pgf_control'].values
    
    # Figura 1: Scatter + fit de v4.3
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Scatter por spawn_rate
    for spawn_rate in df['spawn_rate'].unique():
        mask = df['spawn_rate'] == spawn_rate
        ax.scatter(
            df[mask]['D_effective'],
            df[mask]['ratio_pgf_control'],
            s=150,
            alpha=0.7,
            label=f'spawn_rate={spawn_rate}'
        )
    
    # Fit de v4.3
    if results['v4.3 (1/(D+D0))']:
        D_range = np.linspace(D.min(), D.max(), 100)
        params = results['v4.3 (1/(D+D0))']['params']
        predictions = model_v4_3(D_range, *params)
        
        ax.plot(D_range, predictions, 'r-', lw=3, label=f'TUI v4.3: ratio ∝ 1/(D+D₀)', zorder=10)
        
        # IC95% si está disponible
        bootstrap = results['v4.3 (1/(D+D0))']['bootstrap']
        if bootstrap:
            pred_lower = model_v4_3(D_range, *bootstrap['ci_lower'])
            pred_upper = model_v4_3(D_range, *bootstrap['ci_upper'])
            ax.fill_between(D_range, pred_lower, pred_upper, alpha=0.2, color='red')
    
    ax.set_xlabel('Densidad Efectiva de Recursos ($D_{efectiva}$)', fontsize=14)
    ax.set_ylabel('Ratio PGF/Control (%)', fontsize=14)
    ax.set_title('Ley de Densidad-Riesgo: Validación Experimental', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    fig_path = output_dir / "density_law_validated.png"
    plt.savefig(fig_path, dpi=300)
    print(f"✓ Guardado: {fig_path}")
    
    # Figura 2: Comparación de modelos (AIC)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    model_names = list(results.keys())
    aics = [results[name]['aic'] if results[name] else np.nan for name in model_names]
    
    bars = ax.bar(model_names, aics, color=['blue', 'green', 'orange'])
    ax.set_ylabel('AIC (menor = mejor)', fontsize=14)
    ax.set_title('Comparación de Modelos: AIC', fontsize=16, fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    
    fig_path = output_dir / "model_comparison_aic.png"
    plt.savefig(fig_path, dpi=300)
    print(f"✓ Guardado: {fig_path}")
    
    plt.close('all')


def main():
    """Ejecuta análisis completo"""
    print("\n" + "="*80)
    print("🔬 ANÁLISIS DE EXPERIMENTO 2: VALIDACIÓN DE HIPÓTESIS H-DR")
    print("="*80 + "\n")
    
    # Cargar datos
    df = load_experiment_results()
    
    if len(df) == 0:
        print("❌ No se encontraron resultados. Ejecuta primero: python scripts/run_experiment_2_density.py")
        return
    
    # Análisis estadístico
    results, criteria = analyze_hypothesis(df)
    
    # Generar figuras
    generate_figures(df, results)
    
    # Guardar reporte
    report_path = Path("results/pgf_v5/reportes/REPORTE_EXPERIMENTO_2.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Reporte Experimento 2: Validación de Hipótesis H-DR\n\n")
        f.write("## Resultados\n\n")
        f.write(f"- **Configuraciones analizadas:** {len(df)}\n")
        f.write(f"- **Correlación r(D, ratio):** {pearsonr(df['D_effective'], df['ratio_pgf_control'])[0]:.3f}\n")
        f.write(f"- **R² (modelo v4.3):** {results['v4.3 (1/(D+D0))']['r2']:.3f}\n")
        f.write(f"- **Criterios cumplidos:** {sum(criteria.values())}/5\n\n")
        f.write("## Veredicto\n\n")
        if sum(criteria.values()) >= 4:
            f.write("✅ **HIPÓTESIS H-DR CONFIRMADA**\n")
        elif sum(criteria.values()) >= 3:
            f.write("⚠️ **EVIDENCIA PARCIAL**\n")
        else:
            f.write("❌ **HIPÓTESIS REFUTADA**\n")
    
    print(f"✓ Reporte guardado: {report_path}")


if __name__ == "__main__":
    main()
