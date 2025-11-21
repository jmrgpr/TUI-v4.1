
# scripts/

Utilidades y scripts auxiliares para el proyecto TUI-v4.1. / Utilities and helper scripts for the TUI-v4.1 project.

- `consolidate_results.py`: recorre las carpetas de resultados (`results/sweep/fase2`, `results/sota`, `artifacts/phase2`, `reports/phase2`) y consolida todos los CSV en `results/master_results.csv` con columnas estándar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total, filename). Detecta seeds y algoritmos por ruta/nombre. / Traverses results folders and consolidates all CSVs into `results/master_results.csv` with standardized columns and metadata. Detects seeds and algorithms by path/name.

- `run_full_experiment.py`: automatiza el pipeline experimental completo, alineado con el protocolo científico y checklist preflight. / Automates the full experimental pipeline, aligned with the scientific protocol and preflight checklist.
  1) Barridos PGF (default y tuning) para seeds 42/123/456 con 200 episodios. / PGF sweeps (default and tuning) for seeds 42/123/456 with 200 episodes.
  2) Re-run de la mejor config (tuning) con 500 episodios. / Re-run of best config (tuning) with 500 episodes.
  3) Comparativo SOTA (`run_sota_comparison.py`). / SOTA comparison (`run_sota_comparison.py`).
  4) Consolidación de resultados (`consolidate_results.py`). / Results consolidation (`consolidate_results.py`).
  Uso: `python scripts/run_full_experiment.py`.

- `merge_summaries.py`: utilidades de combinación de resúmenes (ver script). / Summary merging utilities (see script).
- `fix.py`: script archivado desde la raíz para organización. / Archived script for organization.

### Criterios científicos y operativos / Scientific and operational criteria

- Objetivo: Comparar TUI+PGF vs SOTA bajo riesgo, evaluando robustez, reproducibilidad y trazabilidad. / Objective: Compare TUI+PGF vs SOTA under risk, evaluating robustness, reproducibility, and traceability.
- Definición cuantitativa de “competitivo o superior”: PGF_neto medio dentro de 1 desviación estándar del mejor SOTA en ≥30% de riesgos, o superior si excede con p<0.05 (Holm-Bonferroni). / Quantitative definition of "competitive or superior": mean PGF_neto within 1 standard deviation of best SOTA in ≥30% of risks, or superior if exceeds with p<0.05 (Holm-Bonferroni).
- Error crítico: fallo que impide producir el CSV maestro o invalida la comparabilidad (ej.: falta de seeds, riesgos incompletos, crash en un agente). / Critical error: failure that prevents producing the master CSV or invalidates comparability (e.g., missing seeds, incomplete risks, agent crash).

#### Checklist preflight (antes de correr batch grande) / Preflight checklist (before running big batch)
- Plan firmado y documentado. / Signed and documented plan.
- Pipeline automático listo. / Automatic pipeline ready.
- Rutas limpias, sin hardcoding. / Clean paths, no hardcoding.
- Smoke test previo con 1 seed × 1 riesgo × pocos episodios. / Prior smoke test with 1 seed × 1 risk × few episodes.
- CSV maestro verificado. / Master CSV verified.
- Baselines SOTA incluyen default + tuned light. / SOTA baselines include default + light tuning.
- Guardado de top-k configs PGF. / Saving top-k PGF configs.
- Repo sincronizado y limpio. / Repo synchronized and clean.
