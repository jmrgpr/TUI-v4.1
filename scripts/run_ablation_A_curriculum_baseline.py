"""
RUNNER ABLATION A: Curriculum baseline (solo referencia, no reentrenar)


Este script solo copia o referencia los resultados de v10_viable en la carpeta de ablation A.
No ejecuta entrenamiento, solo asegura trazabilidad y registro.
"""

<<<<<<< HEAD
<<<<<<< HEAD
from pathlib import Path
=======
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from run_curriculum_complete_viable import (
    VIABLE_DIR,
    ABLATION_A_DIR,
)

<<<<<<< HEAD
=======
def main() -> None:
    print("=" * 70)
    print("ABLATION A: Curriculum baseline (solo referencia)")
    print("=" * 70)
    print(f"Copiando archivos de {VIABLE_DIR} a {ABLATION_A_DIR}")
    ABLATION_A_DIR.mkdir(parents=True, exist_ok=True)
    # Copiar todos los phase*_*.csv y curriculum_summary_*.csv
    for f in VIABLE_DIR.glob("phase*_*.csv"):
>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
        shutil.copy2(f, ABLATION_A_DIR / f.name)
    for f in VIABLE_DIR.glob("curriculum_summary_*.csv"):
        shutil.copy2(f, ABLATION_A_DIR / f.name)
    print("\nOK. Archivos copiados. Baseline listo para comparación.")
    print(f"\nResultados baseline en: {ABLATION_A_DIR}")
<<<<<<< HEAD
=======

>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)

if __name__ == "__main__":
    main()
