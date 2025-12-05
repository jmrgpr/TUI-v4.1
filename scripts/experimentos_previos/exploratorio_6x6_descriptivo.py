"""
Análisis exploratorio rápido: Grid 6x6 (exploratorio_6x6)
- Medias y desviaciones estándar de reward y tripwires por shaping
- Solo resumen tabular, sin ANOVA ni figuras
"""
import pandas as pd
from pathlib import Path
import numpy as np

EXPLORATORIO_DIR = Path("results/pgf_v8/resultados")

# Buscar todos los CSVs
csvs = list(EXPLORATORIO_DIR.glob("*.csv"))
if not csvs:
    print("No se encontraron archivos CSV en exploratorio_6x6.")
    exit(1)

data = []
for csv_path in csvs:
    df = pd.read_csv(csv_path)
    # Extraer shaping_scale del archivo o columna
    if 'shaping_scale' in df.columns:
        shaping = df['shaping_scale'].iloc[0]
    else:
        # Extraer del nombre de archivo
        try:
            shaping = float([s for s in csv_path.stem.split('_') if s.startswith('shaping')][0].replace('shaping',''))
        except Exception:
            shaping = np.nan
    
    # Extraer spawn_rate (densidad)
    if 'spawn_rate' in df.columns:
        spawn = df['spawn_rate'].iloc[0]
    else:
        try:
            spawn = float([s for s in csv_path.stem.split('_') if s.startswith('spawn')][0].replace('spawn',''))
        except Exception:
            spawn = np.nan
    
    # Extraer seed
    if 'seed' in df.columns:
        seed = df['seed'].iloc[0]
    else:
        try:
            seed = int([s for s in csv_path.stem.split('_') if s.startswith('seed')][0].replace('seed',''))
        except Exception:
            seed = np.nan
    
    # PGF y Control
    for agent in ['PGF', 'Control']:
        sub = df[df['agent_type']==agent]
        data.append({
            'shaping': shaping,
            'spawn': spawn,
            'seed': seed,
            'agent': agent,
            'n': len(sub),
            'reward_env_mean': sub['total_reward_env'].mean(),
            'reward_env_std': sub['total_reward_env'].std(),
            'tripwires_mean': sub['tripwires_triggered'].mean(),
            'tripwires_std': sub['tripwires_triggered'].std(),
            'success_rate': sub['goal_reached'].mean()
        })

summary = pd.DataFrame(data)

# Agregar por shaping y agente (promediando seeds y densidades)
agg = summary.groupby(['shaping', 'agent']).agg({
    'reward_env_mean': 'mean',
    'reward_env_std': 'mean',
    'tripwires_mean': 'mean',
    'tripwires_std': 'mean',
    'success_rate': 'mean',
    'n': 'sum'
}).reset_index()

# Mostrar tabla resumen
print("\n=== RESUMEN EXPLORATORIO v8 (agregado por shaping) ===\n")
print(agg.pivot(index='shaping', columns='agent', values=['reward_env_mean','tripwires_mean','success_rate']))

# Guardar CSV resumen
summary.to_csv(EXPLORATORIO_DIR/"resumen_descriptivo.csv", index=False)
print(f"\nResumen guardado en: {EXPLORATORIO_DIR/'resumen_descriptivo.csv'}")
