import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import glob
import os

def cargar_csvs_agente_grid(agente, grid, base_path=None):
    if base_path is None:
        base_path = Path(__file__).parent.parent
    carpeta = Path(base_path) / f'grid{grid}/riskhigh/{agente}'
    csvs = list(carpeta.glob('*.csv'))
    dfs = []
    for f in csvs:
        try:
            dfs.append(pd.read_csv(f))
        except Exception as e:
            print(f'Error leyendo {f}: {e}')
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def main():
    # Cargar y mostrar ejemplo para control, grid8
    df = cargar_csvs_agente_grid('control', 8)
    print(df.head())
    # Estadísticas descriptivas
    if not df.empty:
        print(df.groupby('Agente').agg(['mean', 'std', 'min', 'max']))
        # Visualización rápida
        try:
            df.boxplot(column='Recompensa', by='Agente')
            plt.title('Distribución de recompensa por agente')
            plt.suptitle('')
            plt.show()
        except Exception as e:
            print(f'Error en visualización: {e}')
    else:
        print('No hay datos para analizar.')

if __name__ == "__main__":
    main()
