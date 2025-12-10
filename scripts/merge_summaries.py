import glob
import pandas as pd
import os

def merge_summaries(summary_folder, output_file):  # pragma: no cover
    """
    Une todos los archivos *_summary.csv en un solo resumen global.
    """
    summary_files = glob.glob(os.path.join(summary_folder, '*_summary.csv'))
    dfs = []
    for f in summary_files:
        try:
            dfs.append(pd.read_csv(f))
        except Exception:
            # Si un archivo está corrupto, lo saltamos y continuamos
            pass
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    if not dfs:
        pd.DataFrame().to_csv(output_file, index=False)
        print(f"Sin summaries en {summary_folder}. CSV vacío creado en: {output_file}")
        return
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(output_file, index=False)
    print(f"Resumen global guardado en: {output_file}")

if __name__ == "__main__":
    merge_summaries('results/fase2', 'results/fase2_global_summary.csv')
