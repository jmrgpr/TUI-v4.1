# Wrapper simple para consolidar resultados sweep + sota
# Lee archivos y escribe master_combined limpio

import pandas as pd
import glob
from pathlib import Path


def cargar_seguro(path: Path):
    if not path.is_file() or path.stat().st_size == 0:
        print(f"[WARN] Archivo vacío/ausente, se omite: {path}")
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"[WARN] No se pudo leer {path}: {e}")
        return None


def consolidar(input_pattern, output_file, recursive=False):
    files = glob.glob(input_pattern, recursive=recursive)
    dfs = []
    for f in files:
        df = cargar_seguro(Path(f))
        if df is not None:
            dfs.append(df)
    if not dfs:
        print(f"[ERROR] No hay archivos válidos para consolidar en patrón: {input_pattern}")
        return
    master = pd.concat(dfs, ignore_index=True)
    # Filtrar solo runs de 1000 episodios (full)
    if "episodes" in master.columns:
        master = master[master["episodes"] == 1000]
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(output_file, index=False)
    print(f"[OK] Consolidado {len(dfs)} archivos en {output_file} (solo 1000 episodios)")


if __name__ == "__main__":
    consolidar("experimento2-reestructurado/data/sota/**/*.csv", "experimento2-reestructurado/data/master_results_combined.csv", recursive=True)
    consolidar("experimento2-reestructurado/data/sweep/fase2_full/**/*.*csv", "experimento2-reestructurado/data/master_results_clean.csv", recursive=True)
    consolidar("experimento2-reestructurado/data/sweep/fase2_full/*/sweep_tui_*_summary.csv", "experimento2-reestructurado/data/master_results_tui.csv", recursive=False)
