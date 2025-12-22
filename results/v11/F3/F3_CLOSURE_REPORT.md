# F3_CLOSURE_REPORT (v11)

**Fecha:** 2025-12-22  
**Fase:** F3  
**Repositorio:** TUI-v4.1  

## Objetivo del cierre
Dejar F3 en estado **auditable y peer-review proof**: trazabilidad de datos (CSV + hashes), verificabilidad de derivados desde JSON (hashes sin versionar JSON), y análisis preregistrado publicado con control de error familiar.

## Artefactos canónicos (citas exactas)

### Datos y trazabilidad
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis
- Reporte preregistrado F3 (family primaria Holm-Bonferroni M=6): `results/v11/data/f3_preregistered_report_v11.md`
- Tabla preregistrada F3 (incluye pooled y sensibilidad por grid): `results/v11/data/f3_preregistered_stats_v11.csv`
- Chequeos de integridad/truncamiento (F3): `results/v11/data/f3_integrity_report_v11.md`
- Power analysis (diagnóstico basado en varianza observada): `results/v11/data/f3_power_analysis_v11.md` y `results/v11/data/f3_power_analysis_v11.csv`

### Reconsolidación y descriptivos globales
- Master reconsolidado desde episodios: `results/master_results_clean.csv`
- Descriptivos globales (incluye F3 como fase separada): `results/v11/data/stats_report_v11.md`
- Tabla de descriptivos (incluye F3 como fase separada): `results/v11/data/stats_summary_v11.csv`

## Confirmaciones mínimas (checklist)
- Los outputs de F3 están separados por condición (evita mezcla F1/F2 dentro de F3):
  - `results/v11/F3/F1_highrisk/`
  - `results/v11/F3/F2_redteam/`
- Los CSV organizados de F3 están versionados en GitHub; los JSON de runs no se versionan por tamaño y se auditan mediante hashes (manifiesto extendido).
- El análisis preregistrado de F3 se ejecuta desde `scripts/f3_preregistered_analysis_v11.py` y publica las salidas citadas.

## Nota técnica sobre el “delta 0” en la ablación
En `results/v11/data/f3_preregistered_report_v11.md`, la ablación `pgf_mix=0.2` vs `pgf_mix=0.0` sobre `reward_env_total` reporta Δ≈0.
Esto no implica que `pgf_mix` no se haya aplicado: el sanity check del reporte preregistrado muestra que `reward_total` sí cambia (shaping) mientras que `reward_env_total` permanece invariante por pares (misma condición/grid/seed).

## Alcance de inferencia (importante para peer review)
- F3 evalúa `pgf_mix` como **operacionalización** (shaping lineal) y su impacto en `reward_env_total`; no pretende “probar/refutar” PGF como principio teórico general.
- Un p-value grande por sí solo no demuestra nulidad; aquí, la evidencia clave del resultado nulo en `reward_env_total` es la **invariancia por pares** (todas las diferencias m0.2−m0.0 son exactamente 0) y la confirmación de trayectorias ambientales idénticas vía hash de `reward_env_evol` en JSON (con `pgf_mix` correcto en config).

## Desviaciones del preregistro
Las desviaciones (si existen) deben registrarse **antes** de análisis completo en:
- `results/v11/F3/F3_DEVIATIONS_LOG_v11.md`

Estado al cierre: **sin desviaciones registradas** (ver log).
