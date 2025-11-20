import glob
import pandas as pd
import os

def merge_summaries(summary_folder, output_file):
    """
    Une todos los archivos *_summary.csv en un solo resumen global.
    """
    summary_files = glob.glob(os.path.join(summary_folder, '*_summary.csv'))
    dfs = [pd.read_csv(f) for f in summary_files]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(output_file, index=False)
    print(f"Resumen global guardado en: {output_file}")

if __name__ == "__main__":
    merge_summaries('results/fase2', 'results/fase2_global_summary.csv')
