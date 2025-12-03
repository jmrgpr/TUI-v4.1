"""
Análisis de la Curva Goldilocks - Experimento 3 (PGF v6)

Analiza barrido fino de densidades para validar hipótesis de parábola invertida.
Compara modelos (lineal, cuadrático, log, exp) y selecciona mejor con AIC/BIC.

Uso:
    python scripts/analyze_goldilocks_curve.py
"""
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit

# Configuración estética
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 11


def load_experiment_data(results_dir="results/pgf_v6/resultados"):
    """Carga todos los JSON de experimentos v6"""
    data = []
    
    for json_file in Path(results_dir).glob("exp3_*.json"):
        if "summary" in json_file.name:
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            exp = json.load(f)
            
        # Metadata
        config = exp['config']
        results = exp['results']
        
        data.append({
            'filename': json_file.name,
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'D_effective': results['D_effective_mean'],
            'ratio_pgf_control': results['ratio_pgf_control'],
            'mean_reward_pgf': results['mean_reward_pgf'],
            'mean_reward_control': results['mean_reward_control'],
            'n_episodes_pgf': results['n_episodes_pgf'],
            'n_episodes_control': results['n_episodes_control'],
        })
    
    return pd.DataFrame(data)


def detect_outliers(df, threshold=3):
    """Detecta outliers usando Z-score en ratio"""
    z_scores = np.abs(stats.zscore(df['ratio_pgf_control']))
    return z_scores > threshold


def fit_models(x, y):
    """Ajusta múltiples modelos y retorna parámetros + AIC/BIC"""
    n = len(x)
    models = {}
    
    # Modelo 0: Constante (H0 - plano)
    mean_y = np.mean(y)
    rss0 = np.sum((y - mean_y)**2)
    k0 = 1
    aic0 = n * np.log(rss0/n) + 2*k0
    bic0 = n * np.log(rss0/n) + k0*np.log(n)
    models['constant'] = {
        'func': lambda x: mean_y,
        'params': [mean_y],
        'rss': rss0,
        'aic': aic0,
        'bic': bic0,
        'k': k0,
        'equation': f'ratio = {mean_y:.2f}'
    }
    
    # Modelo 1: Lineal (ratio = a + bD)
    coeffs1 = np.polyfit(x, y, 1)
    poly1 = np.poly1d(coeffs1)
    y_pred1 = poly1(x)
    rss1 = np.sum((y - y_pred1)**2)
    k1 = 2
    aic1 = n * np.log(rss1/n) + 2*k1
    bic1 = n * np.log(rss1/n) + k1*np.log(n)
    models['linear'] = {
        'func': poly1,
        'params': coeffs1,
        'rss': rss1,
        'aic': aic1,
        'bic': bic1,
        'k': k1,
        'equation': f'ratio = {coeffs1[0]:.2f}D + {coeffs1[1]:.2f}'
    }
    
    # Modelo 2: Cuadrático (ratio = a + bD + cD²) - GOLDILOCKS
    coeffs2 = np.polyfit(x, y, 2)
    poly2 = np.poly1d(coeffs2)
    y_pred2 = poly2(x)
    rss2 = np.sum((y - y_pred2)**2)
    k2 = 3
    aic2 = n * np.log(rss2/n) + 2*k2
    bic2 = n * np.log(rss2/n) + k2*np.log(n)
    
    # Calcular vértice (máximo si a<0)
    a, b, c = coeffs2
    vertex_x = -b / (2*a) if a != 0 else np.nan
    vertex_y = poly2(vertex_x) if not np.isnan(vertex_x) else np.nan
    
    models['quadratic'] = {
        'func': poly2,
        'params': coeffs2,
        'rss': rss2,
        'aic': aic2,
        'bic': bic2,
        'k': k2,
        'equation': f'ratio = {a:.2f}D² + {b:.2f}D + {c:.2f}',
        'vertex': (vertex_x, vertex_y),
        'is_inverted': a < 0
    }
    
    # Modelo 3: Logarítmico (ratio = a + b*log(D))
    try:
        def log_func(x, a, b):
            return a + b * np.log(x)
        params3, _ = curve_fit(log_func, x, y)
        y_pred3 = log_func(x, *params3)
        rss3 = np.sum((y - y_pred3)**2)
        k3 = 2
        aic3 = n * np.log(rss3/n) + 2*k3
        bic3 = n * np.log(rss3/n) + k3*np.log(n)
        models['logarithmic'] = {
            'func': lambda x: log_func(x, *params3),
            'params': params3,
            'rss': rss3,
            'aic': aic3,
            'bic': bic3,
            'k': k3,
            'equation': f'ratio = {params3[0]:.2f} + {params3[1]:.2f}log(D)'
        }
    except:
        models['logarithmic'] = None
    
    # Modelo 4: Exponencial (ratio = a * exp(bD))
    try:
        def exp_func(x, a, b):
            return a * np.exp(b * x)
        params4, _ = curve_fit(exp_func, x, y, p0=[100, -0.1])
        y_pred4 = exp_func(x, *params4)
        rss4 = np.sum((y - y_pred4)**2)
        k4 = 2
        aic4 = n * np.log(rss4/n) + 2*k4
        bic4 = n * np.log(rss4/n) + k4*np.log(n)
        models['exponential'] = {
            'func': lambda x: exp_func(x, *params4),
            'params': params4,
            'rss': rss4,
            'aic': aic4,
            'bic': bic4,
            'k': k4,
            'equation': f'ratio = {params4[0]:.2f}exp({params4[1]:.2f}D)'
        }
    except:
        models['exponential'] = None
    
    return models


def check_goldilocks_criteria(df_robust, models):
    """Verifica 5 criterios preregistrados para H1 (Goldilocks)"""
    
    # Criterio 1: Correlación significativa
    x = df_robust['D_effective'].values
    y = df_robust['ratio_pgf_control'].values
    r, p = stats.pearsonr(x, y)
    crit1 = abs(r) > 0.5 and p < 0.01
    
    # Criterio 2: Modelo cuadrático gana
    quad = models['quadratic']
    lin = models['linear']
    delta_aic = quad['aic'] - lin['aic']
    crit2 = delta_aic < -4
    
    # Criterio 3: Parábola invertida (a < 0)
    a = quad['params'][0]
    # Bootstrap IC95% para a
    n_boot = 1000
    boot_a = []
    for _ in range(n_boot):
        idx = np.random.choice(len(x), len(x), replace=True)
        boot_x = x[idx]
        boot_y = y[idx]
        boot_coeffs = np.polyfit(boot_x, boot_y, 2)
        boot_a.append(boot_coeffs[0])
    
    a_ci = np.percentile(boot_a, [2.5, 97.5])
    crit3 = a < 0 and a_ci[1] < 0  # IC95% no cruza 0
    
    # Criterio 4: Máximo en rango [0.7, 1.5]
    vertex_x, vertex_y = quad['vertex']
    crit4 = 0.7 <= vertex_x <= 1.5
    
    # Criterio 5: Ratio pico > 95%
    crit5 = vertex_y > 95
    
    criteria = {
        '1_correlation': {'met': crit1, 'value': f'r={r:.3f}, p={p:.4f}', 'threshold': '|r|>0.5, p<0.01'},
        '2_quadratic_wins': {'met': crit2, 'value': f'ΔAIC={delta_aic:.2f}', 'threshold': 'ΔAIC<-4'},
        '3_inverted_parabola': {'met': crit3, 'value': f'a={a:.3f}, IC95%={a_ci}', 'threshold': 'a<0, IC95%<0'},
        '4_maximum_range': {'met': crit4, 'value': f'D*={vertex_x:.3f}', 'threshold': '0.7≤D*≤1.5'},
        '5_peak_ratio': {'met': crit5, 'value': f'ratio(D*)={vertex_y:.2f}%', 'threshold': '>95%'},
    }
    
    n_met = sum(c['met'] for c in criteria.values())
    
    return criteria, n_met


def plot_goldilocks_analysis(df_robust, models, criteria, n_met, output_dir="results/pgf_v6/figuras"):
    """Genera figura completa del análisis Goldilocks"""
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    x = df_robust['D_effective'].values
    y = df_robust['ratio_pgf_control'].values
    
    # Panel 1: Scatter + ajustes
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    
    ax1.scatter(x, y, s=150, alpha=0.6, c='steelblue', edgecolors='black', linewidth=1.5, zorder=3)
    
    x_smooth = np.linspace(x.min(), x.max(), 200)
    
    # Plotear modelos
    colors = {'constant': 'gray', 'linear': 'orange', 'quadratic': 'red', 'logarithmic': 'green', 'exponential': 'purple'}
    for name, model in models.items():
        if model is None:
            continue
        try:
            y_smooth = model['func'](x_smooth) if name != 'constant' else [model['func'](0)] * len(x_smooth)
            ax1.plot(x_smooth, y_smooth, color=colors.get(name, 'black'), 
                    linewidth=2, alpha=0.7, label=f'{name.title()} (AIC={model["aic"]:.1f})')
        except:
            pass
    
    # Marcar vértice si existe
    if 'quadratic' in models and models['quadratic']['is_inverted']:
        vx, vy = models['quadratic']['vertex']
        ax1.scatter([vx], [vy], s=300, marker='*', c='gold', 
                   edgecolors='red', linewidths=3, zorder=5, label=f'Peak: D={vx:.2f}, ratio={vy:.1f}%')
        ax1.axvline(vx, color='red', linestyle=':', linewidth=2, alpha=0.5)
    
    ax1.axhline(100, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Paridad (100%)')
    ax1.set_xlabel('Densidad Efectiva (D)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Ratio PGF/Control (%)', fontsize=14, fontweight='bold')
    ax1.set_title('Curva de Goldilocks: Validación Experimental PGF v6', fontsize=16, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Comparación AIC
    ax2 = fig.add_subplot(gs[0, 2])
    model_names = [name for name, m in models.items() if m is not None]
    aics = [models[name]['aic'] for name in model_names]
    
    bars = ax2.barh(model_names, aics, color=[colors.get(n, 'gray') for n in model_names], alpha=0.7, edgecolor='black')
    ax2.set_xlabel('AIC', fontsize=12, fontweight='bold')
    ax2.set_title('Comparación de Modelos\n(menor AIC = mejor)', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Marcar mejor modelo
    best_idx = np.argmin(aics)
    bars[best_idx].set_color('gold')
    bars[best_idx].set_edgecolor('red')
    bars[best_idx].set_linewidth(3)
    
    # Panel 3: Criterios Goldilocks
    ax3 = fig.add_subplot(gs[1, 2])
    ax3.axis('off')
    
    text = f"✅ CRITERIOS GOLDILOCKS ({n_met}/5)\n\n"
    for i, (crit_name, crit_data) in enumerate(criteria.items(), 1):
        symbol = "✅" if crit_data['met'] else "❌"
        text += f"{symbol} {i}. {crit_name.replace('_', ' ').title()}\n"
        text += f"   Valor: {crit_data['value']}\n"
        text += f"   Umbral: {crit_data['threshold']}\n\n"
    
    ax3.text(0.05, 0.95, text, fontsize=10, verticalalignment='top', 
            family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Panel 4: Distribución de residuos (cuadrático)
    ax4 = fig.add_subplot(gs[2, 0])
    quad_residuals = y - models['quadratic']['func'](x)
    ax4.hist(quad_residuals, bins=15, alpha=0.7, color='steelblue', edgecolor='black')
    ax4.axvline(0, color='red', linestyle='--', linewidth=2)
    ax4.set_xlabel('Residuos', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
    ax4.set_title('Distribución de Residuos\n(Modelo Cuadrático)', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Panel 5: Q-Q plot
    ax5 = fig.add_subplot(gs[2, 1])
    stats.probplot(quad_residuals, dist="norm", plot=ax5)
    ax5.set_title('Q-Q Plot (Normalidad Residuos)', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # Panel 6: Veredicto
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')
    
    if n_met >= 4:
        verdict = "✅ GOLDILOCKS CONFIRMADA"
        color = 'green'
        explanation = "La hipótesis H1 (parábola invertida)\nes SOPORTADA por los datos.\n\nExiste una zona óptima de densidad\ndonde la alineación maximiza\nsu ventaja competitiva."
    elif n_met == 3:
        verdict = "⚠️ EVIDENCIA PARCIAL"
        color = 'orange'
        explanation = "La hipótesis H1 tiene soporte\nmoderado pero no conclusivo.\n\nSe requiere mayor N o\nexperimentos adicionales."
    else:
        verdict = "❌ GOLDILOCKS REFUTADA"
        color = 'red'
        explanation = "La hipótesis H1 NO es soportada\npor los datos.\n\nLa relación ratio(D) no sigue\nuna parábola invertida."
    
    ax6.text(0.5, 0.7, verdict, fontsize=16, fontweight='bold', 
            ha='center', va='center', color=color,
            bbox=dict(boxstyle='round', facecolor=color, alpha=0.2, edgecolor=color, linewidth=3))
    
    ax6.text(0.5, 0.3, explanation, fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    output_path = Path(output_dir) / "goldilocks_full_analysis_v6.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Figura guardada: {output_path}")
    
    plt.show()


def generate_report(df, df_robust, models, criteria, n_met, output_dir="results/pgf_v6/reportes"):
    """Genera reporte markdown con todos los resultados"""
    
    report = f"""# Experimento 3: Análisis de la Curva Goldilocks (PGF v6)

**Fecha análisis**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Datos analizados**: {len(df)} configuraciones ({len(df_robust)} robustos)  
**Outliers detectados**: {len(df) - len(df_robust)}

---

## 1. Resumen de Datos

### Configuraciones Ejecutadas
- **Densidades probadas**: {sorted(df['spawn_rate'].unique())}
- **Seeds por densidad**: {sorted(df['seed'].unique())}
- **Episodios por agente**: {df['n_episodes_pgf'].iloc[0]} PGF + {df['n_episodes_control'].iloc[0]} Control

### Estadísticas Generales (Robustos)
"""
    
    # Tabla por densidad
    report += "\n| Densidad | N | Ratio medio | Std | D_eff medio |\n"
    report += "|----------|---|-------------|-----|-------------|\n"
    
    for sr in sorted(df_robust['spawn_rate'].unique()):
        subset = df_robust[df_robust['spawn_rate'] == sr]
        report += f"| {sr} | {len(subset)} | {subset['ratio_pgf_control'].mean():.2f}% | {subset['ratio_pgf_control'].std():.2f} | {subset['D_effective'].mean():.3f} |\n"
    
    # Modelos ajustados
    report += "\n---\n\n## 2. Comparación de Modelos\n\n"
    report += "| Modelo | Ecuación | AIC | BIC | RSS |\n"
    report += "|--------|----------|-----|-----|-----|\n"
    
    for name, model in models.items():
        if model is None:
            continue
        report += f"| {name.title()} | `{model['equation']}` | {model['aic']:.2f} | {model['bic']:.2f} | {model['rss']:.2f} |\n"
    
    # Mejor modelo
    best_model = min([(n, m) for n, m in models.items() if m is not None], key=lambda x: x[1]['aic'])
    report += f"\n**Mejor modelo (menor AIC)**: **{best_model[0].title()}**\n"
    
    # Si es cuadrático, reportar vértice
    if best_model[0] == 'quadratic':
        vx, vy = best_model[1]['vertex']
        report += f"\n**Máximo detectado**: D* = {vx:.3f}, ratio(D*) = {vy:.2f}%\n"
        if best_model[1]['is_inverted']:
            report += "**Forma**: Parábola invertida ✅ (cuadrático negativo)\n"
    
    # Criterios Goldilocks
    report += "\n---\n\n## 3. Verificación de Criterios Goldilocks\n\n"
    report += f"**Criterios cumplidos**: {n_met}/5\n\n"
    
    for i, (crit_name, crit_data) in enumerate(criteria.items(), 1):
        symbol = "✅" if crit_data['met'] else "❌"
        report += f"{symbol} **{i}. {crit_name.replace('_', ' ').title()}**\n"
        report += f"   - Valor observado: `{crit_data['value']}`\n"
        report += f"   - Umbral preregistrado: `{crit_data['threshold']}`\n\n"
    
    # Veredicto
    report += "\n---\n\n## 4. Veredicto Final\n\n"
    
    if n_met >= 4:
        report += "### ✅ HIPÓTESIS GOLDILOCKS CONFIRMADA\n\n"
        report += "La hipótesis H1 (parábola invertida con máximo en D intermedia) es **SOPORTADA** por los datos experimentales.\n\n"
        report += "**Implicaciones**:\n"
        report += "1. Existe una **zona Goldilocks** donde la alineación maximiza su ventaja\n"
        report += "2. El costo de alineación NO escala linealmente con recursos\n"
        report += "3. Ambientes extremos (escasez/abundancia) dificultan diferenciación\n\n"
        report += "**Recomendación**: Paper para Nature Machine Intelligence / Science Robotics\n"
    elif n_met == 3:
        report += "### ⚠️ EVIDENCIA PARCIAL\n\n"
        report += "La hipótesis H1 tiene **soporte moderado** pero no conclusivo.\n\n"
        report += "**Recomendación**: Experimento adicional con mayor N o paper NeurIPS/ICLR con caveats\n"
    else:
        report += "### ❌ HIPÓTESIS GOLDILOCKS NO CONFIRMADA\n\n"
        report += "La hipótesis H1 NO es soportada por los datos. La relación ratio(D) no sigue parábola invertida.\n\n"
        report += "**Recomendación**: Explorar formas funcionales alternativas o paper metodológico\n"
    
    # Guardar reporte
    output_path = Path(output_dir) / "REPORTE_EXPERIMENTO_3.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Reporte guardado: {output_path}")


def main():
    print("="*80)
    print("📊 ANÁLISIS EXPERIMENTO 3 - CURVA GOLDILOCKS (PGF v6)")
    print("="*80 + "\n")
    
    # Cargar datos
    print("📁 Cargando datos experimentales...")
    df = load_experiment_data()
    print(f"✓ {len(df)} configuraciones cargadas\n")
    
    # Detectar outliers
    print("🔍 Detectando outliers...")
    outliers = detect_outliers(df)
    df_robust = df[~outliers].copy()
    print(f"✓ {outliers.sum()} outliers detectados")
    print(f"✓ {len(df_robust)} configuraciones robustas\n")
    
    if outliers.sum() > 0:
        print("⚠️  Outliers detectados:")
        print(df[outliers][['spawn_rate', 'seed', 'ratio_pgf_control', 'D_effective']])
        print()
    
    # Ajustar modelos
    print("📈 Ajustando modelos...")
    x = df_robust['D_effective'].values
    y = df_robust['ratio_pgf_control'].values
    
    models = fit_models(x, y)
    print(f"✓ {sum(m is not None for m in models.values())} modelos ajustados\n")
    
    # Verificar criterios Goldilocks
    print("✅ Verificando criterios Goldilocks (preregistrados)...")
    criteria, n_met = check_goldilocks_criteria(df_robust, models)
    print(f"✓ {n_met}/5 criterios cumplidos\n")
    
    # Generar visualización
    print("🎨 Generando visualización completa...")
    plot_goldilocks_analysis(df_robust, models, criteria, n_met)
    
    # Generar reporte
    print("\n📝 Generando reporte markdown...")
    generate_report(df, df_robust, models, criteria, n_met)
    
    # Resumen final
    print("\n" + "="*80)
    print("🏁 ANÁLISIS COMPLETO")
    print("="*80)
    print(f"Criterios Goldilocks: {n_met}/5")
    
    if n_met >= 4:
        print("✅ VEREDICTO: GOLDILOCKS CONFIRMADA")
    elif n_met == 3:
        print("⚠️  VEREDICTO: EVIDENCIA PARCIAL")
    else:
        print("❌ VEREDICTO: GOLDILOCKS REFUTADA")
    
    print("\nVer:")
    print("  - Figura: results/pgf_v6/figuras/goldilocks_full_analysis_v6.png")
    print("  - Reporte: results/pgf_v6/reportes/REPORTE_EXPERIMENTO_3.md")
    print("="*80)


if __name__ == "__main__":
    main()
