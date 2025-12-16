import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Ruta base de resultados
base = Path('results/v11/F2_redteam')

# Ejemplo: cargar todos los CSV de control en grid8
def cargar_csvs_agente_grid(agente, grid):
    carpeta = base / f'grid{grid}/riskhigh/{agente}'
    csvs = list(carpeta.glob('*.csv'))
    dfs = [pd.read_csv(f) for f in csvs]
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

# Cargar y mostrar ejemplo para control, grid8
df = cargar_csvs_agente_grid('control', 8)
print(df.head())

# Estadísticas descriptivas
if not df.empty:
    print(df.groupby('Agente').agg(['mean', 'std', 'min', 'max']))
    # Visualización rápida
    df.boxplot(column='Recompensa', by='Agente')
    plt.title('Distribución de recompensa por agente')
    plt.suptitle('')
    plt.show()
else:
    print('No hay datos para analizar.')
