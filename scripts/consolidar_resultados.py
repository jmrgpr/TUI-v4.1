import pandas as pd
from glob import glob
import os

# 1. Buscar todos los CSV relevantes en la carpeta de resultados
csv_files = glob(os.path.join('results', '*.csv'))
frames = []
for file in csv_files:
    df = pd.read_csv(file)
    # 2. Normalizar columna seed
    if 'seed' in df.columns:
        df['seed'] = df['seed'].fillna(-1).astype(int)
    else:
        df['seed'] = -1
    # 3. Añadir columnas faltantes si no existen
    for col in ['risk_level', 'red_team', 'robustez', 'flexibilidad']:
        if col not in df.columns:
            df[col] = None
    # 4. Añadir columna source_file para trazabilidad
    df['source_file'] = os.path.basename(file)
    frames.append(df)

# 5. Concatenar y guardar master
master = pd.concat(frames, ignore_index=True)
master.to_csv(os.path.join('results', 'master_results_consolidated.csv'), index=False)

print('Consolidación completada. Archivo generado: results/master_results_consolidated.csv')
