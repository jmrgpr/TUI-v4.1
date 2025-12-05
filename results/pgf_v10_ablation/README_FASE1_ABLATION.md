

# FASE 1 – Ablation del Curriculum (A/B/D/C)

## Instrucciones detalladas
1. Ejecutar cada configuración (A, B, D, C) usando los scripts en `scripts/` y especificando la semilla. Ejemplo:
   - `python scripts/run_ablation_A_curriculum_baseline.py --seed 42`
   - `python scripts/run_ablation_B_direct_8x8.py --seed 13`
2. Los resultados se guardan en subcarpetas por configuración y semilla, en archivos CSV como `*_summary_*.csv` o `phase*.csv`.
3. Registrar observaciones y métricas en los archivos `TEMPLATE_RESULTADOS_X.md` de cada carpeta.
4. Comparar los resultados entre configuraciones usando los scripts de análisis y los reportes generados.
5. Para análisis y gráficos: `python scripts/generar_graficos_fase1.py` (salidas en `plots/FASE1/`).
6. Preregistro: ver `../PREREGISTRO_ABLATION_v10.md`.

## Tabla resumen de seeds, rutas y métricas
| Config | Seed  | Ruta CSV                                                                 | Ejemplo de métrica (success_last_100) |
|--------|-------|-------------------------------------------------------------------------|---------------------------------------|
|   A    |  42   | config_A_curriculum/curriculum_summary_102250.csv                       | 0.87                                  |
|   B    |  13   | config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv | 0.98                                  |
|   D    |  13   | config_D_only_6x6/seeds/seed_0013/only_6x6_summary_20251205_152603.csv  | 0.54                                  |
|   C    |  --   | (No hay resultados disponibles para C en disco)                         | --                                    |

## Definición de métricas y criterios
| Métrica               | Columna en CSV         | Definición científica y uso |
|-----------------------|------------------------|----------------------------|
| Éxito total           | success_rate_total     | Proporción de episodios exitosos en toda la fase |
| Éxito últimos 100     | success_last_100       | Proporción de éxito en los últimos 100 episodios |
| Gate (%)              | gate                   | Umbral de éxito considerado satisfactorio (valor de referencia) |
| Gate pasado           | gate_passed            | Si el agente superó el umbral de éxito (True/False) |
| Primer éxito          | first_success_episode  | Episodio donde se alcanza el primer éxito |
| Convergencia          | convergence_episode    | Episodio donde se estabiliza el éxito (o -1 si no converge) |

**Criterio de convergencia:** Se considera convergencia cuando la métrica `success_last_100` se estabiliza por encima del umbral `gate` durante al menos 100 episodios consecutivos.

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 de la seed 13 en Directo 8×8:
  - Archivo: `config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv`
  - Columna: `success_last_100`

## Advertencia sobre configuración C
- Actualmente **no existen archivos de resultados para la configuración C (inverse curriculum)** en disco. Si se generan en el futuro, deben añadirse a la tabla y documentarse aquí.

## Registro y trazabilidad
- Mantener symlinks/copia de los archivos originales.
- Documentar cualquier desviación del protocolo.
- Asegurar reproducibilidad y claridad en la interpretación.
- Referenciar siempre los archivos CSV y scripts usados para cada métrica.
- Enlazar a preregistro y scripts relevantes.

---

*Este README ha sido revisado para trazabilidad, claridad y profesionalismo científico. Revisión: 2025-12-05. Integración final de seeds, rutas, métricas y definiciones.*
