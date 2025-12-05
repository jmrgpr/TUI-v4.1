"""
RUNNER ABLATION A: Curriculum baseline (solo referencia, no reentrenar)


Este script solo copia o referencia los resultados de v10_viable en la carpeta de ablation A.
No ejecuta entrenamiento, solo asegura trazabilidad y registro.
"""

<<<<<<< HEAD
from pathlib import Path
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from run_curriculum_complete_viable import (
    VIABLE_DIR,
    ABLATION_A_DIR,
)

        shutil.copy2(f, ABLATION_A_DIR / f.name)
    for f in VIABLE_DIR.glob("curriculum_summary_*.csv"):
        shutil.copy2(f, ABLATION_A_DIR / f.name)
    print("\nOK. Archivos copiados. Baseline listo para comparación.")
    print(f"\nResultados baseline en: {ABLATION_A_DIR}")

if __name__ == "__main__":
    main()
