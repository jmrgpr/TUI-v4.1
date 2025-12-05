# FASE1_DOCUMENTACION_REPRODUCIBILIDAD.md

## Protocolo de reproducibilidad – Fase 1

Este documento detalla los pasos, comandos y rutas exactas para reproducir todos los experimentos y análisis de la Fase 1.

### 1. Clonado y entorno
```bash
git clone <repo_url>
cd TUI-v4.1
conda env create -f environment.yml
conda activate tui-v4.1
```

### 2. Ejecución de experimentos por configuración
- **A:**
  ```bash
  python scripts/run_ablation_A_curriculum_baseline.py --seed 42
  ```
- **B:**
  ```bash
  python scripts/run_ablation_B_direct_8x8.py --seed 13
  ```
- **D:**
  ```bash
  python scripts/run_ablation_D_only_6x6.py --seed 13
  ```
- **C:**
  (No hay resultados disponibles para C; si se generan, documentar aquí)

### 3. Ubicación de resultados
- **A:** `results/pgf_v10_ablation/config_A_curriculum/curriculum_summary_102250.csv`
- **B:** `results/pgf_v10_ablation/config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv`
- **D:** `results/pgf_v10_ablation/config_D_only_6x6/seeds/seed_0013/only_6x6_summary_20251205_152603.csv`
- **C:** (sin resultados)

### 4. Análisis y generación de gráficos
```bash
python scripts/generar_graficos_fase1.py
```
- Salidas: `plots/FASE1/` (tablas y PNGs)

### 5. Referencias y preregistro
- Preregistro: `results/pgf_v10_ablation/PREREGISTRO_ABLATION_v10.md`
- Plantillas de resultados: `TEMPLATE_RESULTADOS_X.md` en cada config

### 6. Notas de seguridad y limpieza
- No ejecutar comandos de borrado masivo sin respaldo.
- No existen rutas `plots/FASE1/` si no se ha ejecutado el script de gráficos.

---

*Protocolo revisado y actualizado para reproducibilidad y trazabilidad. Revisión: 2025-12-05.*
