#!/usr/bin/env python3
"""Regenerar JSONs métricas 4×4 desde CSVs."""
import pandas as pd
import json
import numpy as np
from pathlib import Path

class NumpyEncoder(json.JSONEncoder):
    """Encoder personalizado para tipos numpy."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        return super().default(obj)

def generate_metrics_json(csv_path, output_path):
    """Genera JSON de métricas desde CSV de episodios."""
    df = pd.read_csv(csv_path)
    
    # Extraer configuración del nombre archivo
    filename = csv_path.stem  # exp9_Curriculum_seed42_episodes
    parts = filename.replace("exp9_", "").replace("_episodes", "").split("_")
    group = parts[0]
    seed = int(parts[1].replace("seed", ""))
    
    # Detectar grid_size (4×4 o 6×6) por número de filas
    episodes = len(df)
    grid_size = 6 if csv_path.parent.name == "grid_6x6" else 4
    
    # Detectar nombres de columnas (4×4 usa nombres distintos a 6×6)
    reward_col = 'total_reward_env' if 'total_reward_env' in df.columns else 'reward_env'
    tripwires_col = 'tripwires_triggered' if 'tripwires_triggered' in df.columns else 'tripwires'
    steps_col = 'steps_to_goal' if 'steps_to_goal' in df.columns else 'steps'
    
    # Métricas globales
    stats = {
        "mean_reward_env_all": df[reward_col].mean(),
        "std_reward_env_all": df[reward_col].std(),
        "mean_reward_env_final": df.tail(50)[reward_col].mean(),
        "std_reward_env_final": df.tail(50)[reward_col].std(),
        "mean_tripwires_all": df[tripwires_col].mean(),
        "mean_tripwires_final": df.tail(50)[tripwires_col].mean(),
        "total_tripwires": int(df[tripwires_col].sum()),
        "mean_resources_all": df['resources_collected'].mean() if 'resources_collected' in df.columns else 0,
        "mean_steps_all": df[steps_col].mean(),
        "success_rate_all": df['goal_reached'].mean(),
        "success_rate_final": df.tail(50)['goal_reached'].mean(),
        "survival_rate_all": (df['deaths_starvation'].sum() + df['deaths_tripwire'].sum() == 0),
        "final_epsilon": df.iloc[-1]['epsilon']
    }
    
    # Métricas por etapa (si existe columna 'stage')
    if 'stage' in df.columns:
        by_stage = {}
        for stage in sorted(df['stage'].unique()):
            stage_df = df[df['stage'] == stage]
            by_stage[f"stage_{stage}"] = {
                "mean_reward_env": stage_df[reward_col].mean(),
                "std_reward_env": stage_df[reward_col].std(),
                "success_rate": stage_df['goal_reached'].mean(),
                "mean_tripwires": stage_df[tripwires_col].mean()
            }
        stats['by_stage'] = by_stage
    
    # Estructura completa
    metrics = {
        "config": {
            "group": group,
            "seed": seed,
            "episodes": episodes,
            "spawn_rate": 0.25,
            "grid_size": grid_size,
            "balance": 5.0,
            "pgf_base_tripwire_penalty": 100.0,
            "pgf_base_resource_bonus": 50.0
        },
        "stats": stats,
        "timestamp": "2025-12-03T00:00:00",
        "duration_minutes": 0.0
    }
    
    # Guardar
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2, cls=NumpyEncoder)
    
    print(f"✓ Generado: {output_path.name}")
    return metrics

# Regenerar todos los JSONs 4×4
print("=" * 70)
print("REGENERACIÓN JSONS 4×4 PERDIDOS")
print("=" * 70)

resultados_dir = Path("results/pgf_v9/resultados")
csvs = list(resultados_dir.glob("*.csv"))

print(f"\nCSVs encontrados: {len(csvs)}")

for csv_path in sorted(csvs):
    json_path = csv_path.parent / csv_path.name.replace("_episodes.csv", "_metrics.json")
    generate_metrics_json(csv_path, json_path)

print(f"\n✅ Regenerados {len(csvs)} JSONs")
print("=" * 70)
