# FASE1_REPORTE_EXHAUSTIVO.md

## Resumen y trazabilidad de resultados (A/B/D/C)

Este reporte consolida los resultados de todas las configuraciones de Fase 1, con trazabilidad total a los archivos CSV, seeds y métricas empleadas. Cada valor numérico está vinculado a su fuente y columna.

| Config | Seed  | Archivo CSV                                                        | success_last_100 | success_rate_total | gate | gate_passed | first_success_episode | convergence_episode |
|--------|-------|---------------------------------------------------------------------|------------------|--------------------|------|-------------|----------------------|--------------------|
|   A    |  42   | config_A_curriculum/curriculum_summary_102250.csv                  | 0.87             | 0.613              | 10.0 | True        | 1                    | -1                 |
|   B    |  13   | config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv | 0.98             | 0.6587             | 10.0 | True        | 199                  | -1                 |
|   D    |  13   | config_D_only_6x6/seeds/seed_0013/only_6x6_summary_20251205_152603.csv    | 0.54             | 0.629              | 20.0 | True        | 21                   | -1                 |
|   C    |  --   | (No hay resultados disponibles para C en disco)                    | --               | --                 | --   | --          | --                   | --                 |

## Definiciones de métricas
- **success_last_100**: Proporción de éxito en los últimos 100 episodios (`success_last_100` en CSV).
- **success_rate_total**: Proporción de éxito en toda la fase (`success_rate_total`).
- **gate**: Umbral de éxito considerado satisfactorio (`gate`).
- **gate_passed**: Si el agente superó el umbral de éxito (`gate_passed`).
- **first_success_episode**: Episodio donde se alcanza el primer éxito (`first_success_episode`).
- **convergence_episode**: Episodio donde se estabiliza el éxito (`convergence_episode`).

## Ejemplo de trazabilidad
Para verificar el valor de `success_last_100` para B/seed 13:
- Archivo: `config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv`
- Columna: `success_last_100`
- Valor: 0.98

## Scripts y reproducibilidad
- Scripts de ejecución: ver `scripts/run_ablation_A_curriculum_baseline.py`, `run_ablation_B_direct_8x8.py`, etc.
- Análisis y gráficos: `python scripts/generar_graficos_fase1.py`
- Preregistro: `../PREREGISTRO_ABLATION_v10.md`

## Notas
- La configuración C (inverse curriculum) no tiene resultados disponibles en disco.
- Todos los valores pueden ser verificados directamente en los archivos CSV listados.

---

*Reporte exhaustivo revisado y actualizado para trazabilidad y reproducibilidad. Revisión: 2025-12-05.*
