"""
ANÁLISIS MULTI-SEED: Estadísticas agregadas v10_multiseed
===========================================================

Analiza resultados de 5 seeds y genera:
- Estadísticas descriptivas (media, std, min, max)
- Boxplots comparativos
- Distribución breakthrough 6×6
- Comparación transfer learning

Detecta si seed=42 es representativa o outlier.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

MULTISEED_DIR = ROOT / "results" / "pgf_v10_multiseed"
SEEDS = [13, 42, 101, 2025, 9999]

# ============================================================================
# FUNCIONES DE ANÁLISIS
# ============================================================================

def load_all_summaries():
    """Carga curriculum_summary.csv de cada seed."""
    print("📊 Cargando summaries de 5 seeds...")
    
    data = []
    for seed in SEEDS:
        seed_dir = MULTISEED_DIR / "seeds" / f"seed_{seed:04d}"
        
        # Buscar archivo summary (puede tener timestamp)
        summary_files = list(seed_dir.glob("curriculum_summary_*.csv"))
        
        if not summary_files:
            print(f"⚠️  Seed {seed}: No se encontró curriculum_summary")
            continue
        
        # Tomar el más reciente si hay varios
        summary_path = max(summary_files, key=lambda p: p.stat().st_mtime)
        
        try:
            df = pd.read_csv(summary_path)
            
<<<<<<< HEAD
            # Detectar formato: baseline v10_viable vs multi-seed
            if 'seed' not in df.columns:
                # Formato baseline: phase, success_rate, last_100, gate_passed, first_success
                # Convertir a formato multi-seed
                n_rows = len(df)
                df_converted = pd.DataFrame({
                    'seed': [int(seed)] * n_rows,
                    'phase': df['phase'].values,
                    'grid_size': df['phase'].map({'4x4': 4, '6x6': 6, '8x8': 8}).values,
                    'episodes': [-1] * n_rows,
                    'success_rate_total': df['success_rate'].values,
                    'success_last_100': df['last_100'].values,
                    'gate': df['phase'].map({'4x4': 80.0, '6x6': 20.0, '8x8': 10.0}).values,
                    'gate_passed': df['gate_passed'].values,
                    'first_success_episode': df['first_success'].values,
                    'convergence_episode': [-1] * n_rows
                })
                df = df_converted
=======
            # Asegurar columna seed
            if 'seed' not in df.columns:
                df['seed'] = seed
>>>>>>> 61e07a7 (Fase 0: Roadmap v10 completo - Estructura multi-seed/ablation/PGF offline)
            
            data.append(df)
            print(f"   ✅ Seed {seed}: {len(df)} fases cargadas")
        
        except Exception as e:
            print(f"   ❌ Seed {seed}: Error leyendo {summary_path.name} - {e}")
    
    if not data:
        raise ValueError("No se pudieron cargar datos de ninguna seed")
    
    df_all = pd.concat(data, ignore_index=True)
    print(f"\n✅ Total registros: {len(df_all)}")
    
    return df_all


def compute_statistics(df):
    """Calcula estadísticas descriptivas por fase."""
    print("\n📈 Calculando estadísticas agregadas...")
    
    stats = []
    
    for phase in ['4x4', '6x6', '8x8']:
        phase_data = df[df['phase'] == phase]
        
        if len(phase_data) == 0:
            print(f"⚠️  Fase {phase}: Sin datos")
            continue
        
        grid_size = phase_data['grid_size'].iloc[0]
        gate = phase_data['gate'].iloc[0]
        
        stats.append({
            'phase': phase,
            'grid_size': int(grid_size),
            'gate_threshold': gate,
            'n_seeds': len(phase_data),
<<<<<<< HEAD
            'success_mean': phase_data['success_last_100'].mean() * 100,  # Convertir fracción → %
            'success_std': phase_data['success_last_100'].std() * 100,
            'success_min': phase_data['success_last_100'].min() * 100,
            'success_max': phase_data['success_last_100'].max() * 100,
=======
            'success_mean': phase_data['success_last_100'].mean(),
            'success_std': phase_data['success_last_100'].std(),
            'success_min': phase_data['success_last_100'].min(),
            'success_max': phase_data['success_last_100'].max(),
>>>>>>> 61e07a7 (Fase 0: Roadmap v10 completo - Estructura multi-seed/ablation/PGF offline)
            'first_success_mean': phase_data['first_success_episode'].mean(),
            'first_success_std': phase_data['first_success_episode'].std(),
            'convergence_mean': phase_data['convergence_episode'].mean(),
            'convergence_std': phase_data['convergence_episode'].std(),
            'seeds_passed_gate': phase_data['gate_passed'].sum()
        })
    
    df_stats = pd.DataFrame(stats)
    
    # Mostrar resultados
    print("\n" + "="*70)
    print("ESTADÍSTICAS MULTI-SEED (N=5)")
    print("="*70)
    
    for _, row in df_stats.iterrows():
        print(f"\n{row['phase'].upper()} ({int(row['grid_size'])}×{int(row['grid_size'])})")
        print(f"  Gate: >{row['gate_threshold']:.0f}%")
        print(f"  Success (últimos 100): {row['success_mean']:.1f}% ± {row['success_std']:.1f}%")
        print(f"  Rango: [{row['success_min']:.1f}%, {row['success_max']:.1f}%]")
        print(f"  Primer éxito: ep {row['first_success_mean']:.0f} ± {row['first_success_std']:.0f}")
        print(f"  Convergencia: ep {row['convergence_mean']:.0f} ± {row['convergence_std']:.0f}")
        print(f"  Seeds que pasaron gate: {int(row['seeds_passed_gate'])}/{int(row['n_seeds'])}")
    
    return df_stats


def analyze_seed42_representativeness(df):
    """Verifica si seed=42 es representativa o outlier."""
    print("\n" + "="*70)
    print("ANÁLISIS: ¿Es seed=42 representativa?")
    print("="*70)
    
    for phase in ['4x4', '6x6', '8x8']:
        phase_data = df[df['phase'] == phase]
        
        if len(phase_data) < 2:
            continue
        
        seed42_data = phase_data[phase_data['seed'] == 42]
        others_data = phase_data[phase_data['seed'] != 42]
        
        if len(seed42_data) == 0:
            print(f"\n{phase}: Seed 42 no disponible")
            continue
        
    seed42_success = seed42_data['success_last_100'].iloc[0]
    mean_others = others_data['success_last_100'].mean()
    std_others = others_data['success_last_100'].std()
        
        # Z-score
        z_score = (seed42_success - mean_others) / std_others if std_others > 0 else 0
        
        is_outlier = abs(z_score) > 2.0
        
        print(f"\n{phase.upper()}:")
        print(f"  Seed 42: {seed42_success:.1f}%")
        print(f"  Otras 4 seeds: {mean_others:.1f}% ± {std_others:.1f}%")
        print(f"  Z-score: {z_score:.2f}")
        
        if is_outlier:
            print(f"  ⚠️  OUTLIER (|z| > 2.0)")
        elif abs(z_score) > 1.0:
            print(f"  ⚡ Ligeramente alejada")
        else:
            print(f"  ✅ Representativa")


def plot_boxplots(df, output_dir):
    """Boxplots de success rate por fase."""
    print("\n🎨 Generando boxplots...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Preparar datos
    phases = ['4x4', '6x6', '8x8']
    data_plot = []
    labels = []
    gate_lines = []
    
    for phase in phases:
        phase_data = df[df['phase'] == phase]
        
        if len(phase_data) == 0:
            continue
        
        data_plot.append(phase_data['success_last_100'].values)
        
        grid = phase_data['grid_size'].iloc[0]
        labels.append(f'{phase.upper()}\n({int(grid)}×{int(grid)})')
        
        gate = phase_data['gate'].iloc[0]
        gate_lines.append(gate)
    
    # Boxplot
    bp = ax.boxplot(data_plot, labels=labels, patch_artist=True, widths=0.6)
    
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    # Gates
    colors = ['green', 'orange', 'red']
    for i, (gate, color) in enumerate(zip(gate_lines, colors)):
        ax.axhline(gate, color=color, linestyle='--', alpha=0.5, linewidth=2)
        ax.text(i+1.3, gate, f'Gate {gate:.0f}%', fontsize=9, color=color, va='center')
    
    ax.set_ylabel('Success Rate (Last 100 Episodes) %', fontsize=12)
    ax.set_title('Multi-Seed Validation (N=5): Success Rate Distribution', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    ax.set_ylim(0, 105)
    
    plt.tight_layout()
    
    output_path = output_dir / "boxplot_success_rates_5seeds.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ {output_path.name}")


def plot_breakthrough_distribution(df, output_dir):
    """Histograma de episodio breakthrough en 6×6."""
    print("🎨 Generando distribución breakthrough 6×6...")
    
    phase6_data = df[df['phase'] == '6x6']
    
    if len(phase6_data) == 0:
        print("   ⚠️  No hay datos de fase 6×6")
        return
    
    # Episodio de convergencia como proxy de breakthrough
    convergence_eps = phase6_data['convergence_episode'].dropna()
    
    if len(convergence_eps) == 0:
        print("   ⚠️  No hay datos de convergencia 6×6")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(convergence_eps, bins=10, color='steelblue', alpha=0.7, edgecolor='black')
    
    mean_conv = convergence_eps.mean()
    ax.axvline(mean_conv, color='red', linestyle='--', linewidth=2, label=f'Media: {mean_conv:.0f}')
    
    ax.set_xlabel('Episodio de Convergencia', fontsize=12)
    ax.set_ylabel('Frecuencia (N seeds)', fontsize=12)
    ax.set_title('Distribución Breakthrough 6×6 (N=5 seeds)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    output_path = output_dir / "phase2_breakthrough_histogram.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ {output_path.name}")


def plot_transfer_effectiveness(df, output_dir):
    """Scatter: primer éxito por fase y seed."""
    print("🎨 Generando análisis transfer learning...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    phases = ['4x4', '6x6', '8x8']
    colors = ['green', 'orange', 'red']
    
    for phase, color in zip(phases, colors):
        phase_data = df[df['phase'] == phase]
        
        if len(phase_data) == 0:
            continue
        
        seeds = phase_data['seed']
        first_success = phase_data['first_success_episode']
        
        ax.scatter(seeds, first_success, label=phase.upper(), color=color, s=100, alpha=0.7)
    
    ax.set_xlabel('Seed', fontsize=12)
    ax.set_ylabel('Episodio Primer Éxito', fontsize=12)
    ax.set_title('Transfer Learning Effectiveness: Primer Éxito por Fase', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_xticks(SEEDS)
    ax.grid(alpha=0.3)
    ax.set_yscale('log')  # Escala log para mejor visualización
    
    plt.tight_layout()
    
    output_path = output_dir / "transfer_effectiveness_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ {output_path.name}")


def generate_report(df_stats, df_all):
    """Genera reporte markdown con conclusiones."""
    print("\n📝 Generando reporte final...")
    
    report_lines = [
        "# REPORTE MULTI-SEED VALIDATION",
        "",
        f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Seeds**: {SEEDS}",
        f"**N**: 5",
        "",
        "---",
        "",
        "## Resultados Agregados",
        "",
        "| Fase | Grid | Gate | Success Mean ± Std | Rango | Seeds Pasaron |",
        "|------|------|------|-------------------|-------|---------------|"
    ]
    
    for _, row in df_stats.iterrows():
        report_lines.append(
            f"| {row['phase'].upper()} | {int(row['grid_size'])}×{int(row['grid_size'])} | "
            f">{row['gate_threshold']:.0f}% | **{row['success_mean']:.1f}% ± {row['success_std']:.1f}%** | "
            f"[{row['success_min']:.1f}%, {row['success_max']:.1f}%] | "
            f"{int(row['seeds_passed_gate'])}/{int(row['n_seeds'])} |"
        )
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Interpretación",
        "",
        "### Hipótesis H1: Success Rates Reproducibles",
        ""
    ])
    
    # Evaluar H1
    h1_passed = True
    for _, row in df_stats.iterrows():
        phase = row['phase']
        mean = row['success_mean']
        gate = row['gate_threshold']
        n_passed = row['seeds_passed_gate']
        n_total = row['n_seeds']
        
        if phase == '4x4' and (mean < 75 or n_passed < 4):
            h1_passed = False
        elif phase == '6x6' and (mean < 30 or n_passed < 3):
            h1_passed = False
        elif phase == '8x8' and (mean < 55 or n_passed < 3):
            h1_passed = False
    
    if h1_passed:
        report_lines.append("✅ **VALIDADA**: Las success rates son reproducibles en N=5 seeds.")
    else:
        report_lines.append("❌ **RECHAZADA**: Alta variabilidad, curriculum no robusto.")
    
    report_lines.extend([
        "",
        "### Hipótesis H2: Breakthrough 6×6 Reproducible",
        ""
    ])
    
    phase6 = df_all[df_all['phase'] == '6x6']
    if len(phase6) > 0:
        conv_mean = phase6['convergence_episode'].mean()
        conv_std = phase6['convergence_episode'].std()
        
        if 400 <= conv_mean <= 700 and conv_std < 200:
            report_lines.append(f"✅ **VALIDADA**: Breakthrough ocurre en ~ep {conv_mean:.0f} ± {conv_std:.0f}")
        else:
            report_lines.append(f"⚠️ **PARCIAL**: Breakthrough variable (ep {conv_mean:.0f} ± {conv_std:.0f})")
    
    report_lines.extend([
        "",
        "### Hipótesis H3: Transfer 6×6→8×8 Superior",
        ""
    ])
    
    phase6 = df_all[df_all['phase'] == '6x6']
    phase8 = df_all[df_all['phase'] == '8x8']
    
    if len(phase6) > 0 and len(phase8) > 0:
        conv6_mean = phase6['convergence_episode'].mean()
        conv8_mean = phase8['convergence_episode'].mean()
        first8_mean = phase8['first_success_episode'].mean()
        
        if conv8_mean < conv6_mean and first8_mean < 20:
            report_lines.append(f"✅ **VALIDADA**: 8×8 converge en {conv8_mean:.0f} eps vs 6×6 en {conv6_mean:.0f} eps")
        else:
            report_lines.append(f"❌ **RECHAZADA**: Transfer no claramente superior")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Conclusión",
        "",
        f"**Estado v10_viable**: ",
        ""
    ])
    
    # Conclusión final
    if h1_passed:
        report_lines.append("✅ **BASELINE VALIDADA** - Curriculum reproducible, proceder con ablation/PGF")
    else:
        report_lines.append("⚠️ **BASELINE FRÁGIL** - Requiere ajustes antes de ablation")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Archivos Generados",
        "",
        "- `multiseed_summary.csv` (datos completos)",
        "- `multiseed_statistics.csv` (estadísticas)",
        "- `boxplot_success_rates_5seeds.png`",
        "- `phase2_breakthrough_histogram.png`",
        "- `transfer_effectiveness_comparison.png`",
        ""
    ])
    
    return "\n".join(report_lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*70)
    print("ANÁLISIS MULTI-SEED: v10_viable Curriculum (N=5)")
    print("="*70)
    
    # Crear directorios
    analisis_dir = MULTISEED_DIR / "analisis_agregado"
    figuras_dir = MULTISEED_DIR / "figuras"
    analisis_dir.mkdir(exist_ok=True)
    figuras_dir.mkdir(exist_ok=True)
    
    # Cargar datos
    df_all = load_all_summaries()
    
    # Estadísticas
    df_stats = compute_statistics(df_all)
    
    # Representatividad seed=42
    analyze_seed42_representativeness(df_all)
    
    # Guardar CSVs
    print("\n💾 Guardando datos agregados...")
    df_all.to_csv(analisis_dir / "multiseed_summary.csv", index=False)
    df_stats.to_csv(analisis_dir / "multiseed_statistics.csv", index=False)
    print(f"   ✅ {analisis_dir}/multiseed_summary.csv")
    print(f"   ✅ {analisis_dir}/multiseed_statistics.csv")
    
    # Generar figuras
    plot_boxplots(df_all, figuras_dir)
    plot_breakthrough_distribution(df_all, figuras_dir)
    plot_transfer_effectiveness(df_all, figuras_dir)
    
    # Reporte final
    report = generate_report(df_stats, df_all)
    report_path = MULTISEED_DIR / "REPORTE_MULTISEED.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Reporte generado: {report_path.name}")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS MULTI-SEED COMPLETADO")
    print("="*70)
    print(f"\n📂 Resultados en: {MULTISEED_DIR}")
    print(f"\n📊 Estadísticas: {analisis_dir}/")
    print(f"🎨 Figuras: {figuras_dir}/")
    print(f"📄 Reporte: {report_path.name}")


if __name__ == "__main__":
    main()
