"""
Generar figuras para experimento v10_viable
Curriculum completo 4×4 → 6×6 → 8×8
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuración estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Cargar datos
df4 = pd.read_csv('results/pgf_v10_viable/resultados/phase1_4x4_20251205_102250.csv')
df6 = pd.read_csv('results/pgf_v10_viable/resultados/phase2_6x6_20251205_102250.csv')
df8 = pd.read_csv('results/pgf_v10_viable/resultados/phase3_8x8_20251205_102250.csv')

# Crear directorio figuras si no existe
import os
os.makedirs('results/pgf_v10_viable/figuras', exist_ok=True)

# ============================================================================
# FIGURA 1: Success Rate por Fase (ventanas móviles 100 eps)
# ============================================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
fig.suptitle('Success Rate Evolution - Curriculum Learning', fontsize=16, fontweight='bold')

# Función para calcular ventanas móviles
def rolling_success(df, window=100):
    return df['success'].rolling(window=window, min_periods=1).mean() * 100

# 4×4
axes[0].plot(range(1, len(df4)+1), rolling_success(df4, 100), 
             linewidth=2, color='#2ecc71', label='Success Rate (100-ep window)')
axes[0].axhline(y=80, color='red', linestyle='--', linewidth=1.5, label='Gate: 80%')
axes[0].fill_between(range(1, len(df4)+1), 0, rolling_success(df4, 100), 
                      alpha=0.3, color='#2ecc71')
axes[0].set_title('Phase 1: 4×4 Grid (Baseline)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Success Rate (%)', fontsize=12)
axes[0].set_ylim(0, 105)
axes[0].legend(loc='lower right')
axes[0].grid(True, alpha=0.3)
axes[0].text(450, 95, f'Final: {df4.iloc[-100:].success.mean()*100:.1f}%', 
             fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

# 6×6
axes[1].plot(range(1, len(df6)+1), rolling_success(df6, 100), 
             linewidth=2, color='#3498db', label='Success Rate (100-ep window)')
axes[1].axhline(y=20, color='red', linestyle='--', linewidth=1.5, label='Gate: 20%')
axes[1].axvline(x=587, color='orange', linestyle=':', linewidth=2, alpha=0.7, label='Breakthrough: ep 587')
axes[1].fill_between(range(1, len(df6)+1), 0, rolling_success(df6, 100), 
                      alpha=0.3, color='#3498db')
axes[1].set_title('Phase 2: 6×6 Grid (Transfer Learning from 4×4)', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Success Rate (%)', fontsize=12)
axes[1].set_ylim(0, 105)
axes[1].legend(loc='lower right')
axes[1].grid(True, alpha=0.3)
axes[1].text(900, 75, f'Final: {df6.iloc[-100:].success.mean()*100:.1f}%', 
             fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

# 8×8
axes[2].plot(range(1, len(df8)+1), rolling_success(df8, 100), 
             linewidth=2, color='#e74c3c', label='Success Rate (100-ep window)')
axes[2].axhline(y=10, color='red', linestyle='--', linewidth=1.5, label='Gate: 10%')
axes[2].axvline(x=157, color='orange', linestyle=':', linewidth=2, alpha=0.7, label='Convergence: ep 157')
axes[2].fill_between(range(1, len(df8)+1), 0, rolling_success(df8, 100), 
                      alpha=0.3, color='#e74c3c')
axes[2].set_title('Phase 3: 8×8 Grid (Transfer Learning from 6×6)', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Episode', fontsize=12)
axes[2].set_ylabel('Success Rate (%)', fontsize=12)
axes[2].set_ylim(0, 105)
axes[2].legend(loc='lower right')
axes[2].grid(True, alpha=0.3)
axes[2].text(900, 95, f'Final: {df8.iloc[-100:].success.mean()*100:.1f}%', 
             fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='#ffcccb', alpha=0.7))

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig1_success_rate_evolution.png', dpi=300, bbox_inches='tight')
print("✅ Figura 1 guardada: fig1_success_rate_evolution.png")
plt.close()

# ============================================================================
# FIGURA 2: Comparación Rewards
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Ventanas móviles rewards
def rolling_rewards(df, window=100):
    return df['rewards'].rolling(window=window, min_periods=1).mean()

x4 = range(1, len(df4)+1)
x6 = range(len(df4)+1, len(df4)+len(df6)+1)
x8 = range(len(df4)+len(df6)+1, len(df4)+len(df6)+len(df8)+1)

ax.plot(x4, rolling_rewards(df4, 100), linewidth=2, color='#2ecc71', label='4×4 (baseline)')
ax.plot(x6, rolling_rewards(df6, 100), linewidth=2, color='#3498db', label='6×6 (transfer)')
ax.plot(x8, rolling_rewards(df8, 100), linewidth=2, color='#e74c3c', label='8×8 (transfer)')

ax.axvline(x=500, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=1500, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.text(250, 40, 'Phase 1\n4×4', ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.text(1000, 40, 'Phase 2\n6×6', ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.text(2000, 40, 'Phase 3\n8×8', ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='#ffcccb', alpha=0.5))

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_title('Average Reward Evolution - Complete Curriculum', fontsize=16, fontweight='bold')
ax.set_xlabel('Cumulative Episode', fontsize=12)
ax.set_ylabel('Average Reward (100-ep window)', fontsize=12)
ax.legend(loc='lower right', fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig2_rewards_evolution.png', dpi=300, bbox_inches='tight')
print("✅ Figura 2 guardada: fig2_rewards_evolution.png")
plt.close()

# ============================================================================
# FIGURA 3: Steps Efficiency
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Solo éxitos
exitos4 = df4[df4['success'] == 1]
exitos6 = df6[df6['success'] == 1]
exitos8 = df8[df8['success'] == 1]

# Boxplot
data_steps = [exitos4['steps'], exitos6['steps'], exitos8['steps']]
bp = ax.boxplot(data_steps, labels=['4×4', '6×6', '8×8'], patch_artist=True,
                medianprops=dict(color='red', linewidth=2),
                boxprops=dict(facecolor='lightblue', alpha=0.7))

# Manhattan distances (promedio)
manhattan = [6, 10, 14]
ax.plot([1, 2, 3], manhattan, 'ro--', linewidth=2, markersize=10, label='Manhattan Distance (optimal)')

# Promedios
promedios = [exitos4['steps'].mean(), exitos6['steps'].mean(), exitos8['steps'].mean()]
ax.plot([1, 2, 3], promedios, 'gs-', linewidth=2, markersize=10, label='DQN Average')

# Overhead factors
for i, (prom, manh) in enumerate(zip(promedios, manhattan)):
    overhead = prom / manh
    ax.text(i+1, prom + 2, f'{overhead:.2f}×', ha='center', fontsize=11, fontweight='bold')

ax.set_title('Steps Efficiency - Successful Episodes Only', fontsize=16, fontweight='bold')
ax.set_xlabel('Grid Size', fontsize=12)
ax.set_ylabel('Steps', fontsize=12)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig3_steps_efficiency.png', dpi=300, bbox_inches='tight')
print("✅ Figura 3 guardada: fig3_steps_efficiency.png")
plt.close()

# ============================================================================
# FIGURA 4: Resources Finales
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Histogramas superpuestos
ax.hist(exitos4['resources'], bins=20, alpha=0.6, color='#2ecc71', label='4×4', density=True)
ax.hist(exitos6['resources'], bins=20, alpha=0.6, color='#3498db', label='6×6', density=True)
ax.hist(exitos8['resources'], bins=20, alpha=0.6, color='#e74c3c', label='8×8', density=True)

# Medias
ax.axvline(exitos4['resources'].mean(), color='#2ecc71', linestyle='--', linewidth=2, 
           label=f'4×4 mean: {exitos4["resources"].mean():.2f}')
ax.axvline(exitos6['resources'].mean(), color='#3498db', linestyle='--', linewidth=2, 
           label=f'6×6 mean: {exitos6["resources"].mean():.2f}')
ax.axvline(exitos8['resources'].mean(), color='#e74c3c', linestyle='--', linewidth=2, 
           label=f'8×8 mean: {exitos8["resources"].mean():.2f}')

ax.set_title('Final Resources Distribution - Successful Episodes', fontsize=16, fontweight='bold')
ax.set_xlabel('Final Resources', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig4_resources_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Figura 4 guardada: fig4_resources_distribution.png")
plt.close()

# ============================================================================
# FIGURA 5: Breakthrough 6×6 Detallado
# ============================================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('Phase 2 (6×6) Breakthrough Analysis', fontsize=16, fontweight='bold')

# Success rate con ventana pequeña
axes[0].plot(range(1, len(df6)+1), rolling_success(df6, 50), 
             linewidth=1.5, color='#3498db', alpha=0.7, label='50-ep window')
axes[0].plot(range(1, len(df6)+1), rolling_success(df6, 100), 
             linewidth=2, color='darkblue', label='100-ep window')
axes[0].axvline(x=587, color='red', linestyle='--', linewidth=2, label='Breakthrough (ep 587)')
axes[0].axhspan(0, 20, alpha=0.1, color='red', label='Below gate')
axes[0].axhspan(20, 100, alpha=0.1, color='green')
axes[0].set_ylabel('Success Rate (%)', fontsize=12)
axes[0].set_ylim(0, 105)
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Rewards
axes[1].plot(range(1, len(df6)+1), rolling_rewards(df6, 50), 
             linewidth=1.5, color='orange', alpha=0.7, label='Avg Reward (50-ep window)')
axes[1].axvline(x=587, color='red', linestyle='--', linewidth=2, label='Breakthrough (ep 587)')
axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[1].set_xlabel('Episode', fontsize=12)
axes[1].set_ylabel('Average Reward', fontsize=12)
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

# Anotaciones zonas
axes[0].text(250, 90, 'Exploration\n(0-2%)', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
axes[0].text(600, 90, 'Breakthrough\n(20-96%)', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
axes[0].text(850, 90, 'Consolidation\n(48-94%)', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig5_breakthrough_6x6.png', dpi=300, bbox_inches='tight')
print("✅ Figura 5 guardada: fig5_breakthrough_6x6.png")
plt.close()

# ============================================================================
# FIGURA 6: Comparación Final (Barras)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('Final Performance Comparison', fontsize=16, fontweight='bold')

phases = ['4×4', '6×6', '8×8']
colors = ['#2ecc71', '#3498db', '#e74c3c']

# Success rates
success_total = [df4['success'].mean()*100, df6['success'].mean()*100, df8['success'].mean()*100]
success_last100 = [df4.iloc[-100:]['success'].mean()*100, 
                   df6.iloc[-100:]['success'].mean()*100, 
                   df8.iloc[-100:]['success'].mean()*100]

axes[0].bar(phases, success_total, color=colors, alpha=0.6, label='Total')
axes[0].bar(phases, success_last100, color=colors, alpha=1.0, label='Last 100 eps')
axes[0].set_ylabel('Success Rate (%)', fontsize=12)
axes[0].set_title('Success Rates', fontsize=13, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')
for i, (tot, last) in enumerate(zip(success_total, success_last100)):
    axes[0].text(i, last + 3, f'{last:.1f}%', ha='center', fontsize=11, fontweight='bold')

# Rewards (solo éxitos)
rewards = [exitos4['rewards'].mean(), exitos6['rewards'].mean(), exitos8['rewards'].mean()]
axes[1].bar(phases, rewards, color=colors, alpha=0.8)
axes[1].set_ylabel('Average Reward', fontsize=12)
axes[1].set_title('Rewards (Successful Episodes)', fontsize=13, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')
for i, r in enumerate(rewards):
    axes[1].text(i, r + 1, f'{r:.2f}', ha='center', fontsize=11, fontweight='bold')

# Steps (solo éxitos)
steps = [exitos4['steps'].mean(), exitos6['steps'].mean(), exitos8['steps'].mean()]
axes[2].bar(phases, steps, color=colors, alpha=0.8, label='DQN')
axes[2].plot(phases, manhattan, 'ro--', linewidth=2, markersize=10, label='Manhattan (optimal)')
axes[2].set_ylabel('Average Steps', fontsize=12)
axes[2].set_title('Steps Efficiency (Successful Episodes)', fontsize=13, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3, axis='y')
for i, (s, m) in enumerate(zip(steps, manhattan)):
    overhead = s / m
    axes[2].text(i, s + 1, f'{s:.1f}\n({overhead:.2f}×)', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('results/pgf_v10_viable/figuras/fig6_final_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Figura 6 guardada: fig6_final_comparison.png")
plt.close()

print("\n" + "="*80)
print("✅ TODAS LAS FIGURAS GENERADAS EXITOSAMENTE")
print("="*80)
print("Ubicación: results/pgf_v10_viable/figuras/")
print("\nFiguras generadas:")
print("  1. fig1_success_rate_evolution.png   - Evolución success rate por fase")
print("  2. fig2_rewards_evolution.png        - Evolución rewards curriculum completo")
print("  3. fig3_steps_efficiency.png         - Efficiency steps vs Manhattan")
print("  4. fig4_resources_distribution.png   - Distribución recursos finales")
print("  5. fig5_breakthrough_6x6.png         - Análisis detallado breakthrough 6×6")
print("  6. fig6_final_comparison.png         - Comparación final 3 fases")
