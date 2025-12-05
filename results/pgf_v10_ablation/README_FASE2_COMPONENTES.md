# README_FASE2_COMPONENTES.md

## FASE 2 – Ablation por Componentes y Hiperparámetros (v10)

### Objetivo
Analizar el aporte individual y combinado de los componentes del agente v10 (shaping, curriculum, transfer, reward extra, regularización, hiperparámetros) mediante variantes controladas.

### Variantes y estructura
- **component_minimal/**: agente mínimo (sin shaping, transfer, curriculum, reward extra, regularización)
- **component_noshaping/**: sin shaping
- **component_notransfer/**: sin transfer
- **component_nocurriculum/**: sin curriculum
- **component_norewardextra/**: sin reward extra
- **component_noregularization/**: sin regularización
- **component_combined/**: combinaciones
- **hyperparam_sweep/**: barrido de hiperparámetros
- **analisis_comparativo/**: tablas y comparativas F2

### Ejecución
Ejemplo de comando para cada variante:
```bash
python scripts/run_ablation_componentes_v10.py --variant minimal --seed 13
python scripts/run_ablation_componentes_v10.py --variant noshaping --seed 42
python scripts/run_ablation_componentes_v10.py --variant hyper_lr_0005 --seed 13
```

### Resultados
- Los resultados de cada variante y seed se guardan en la subcarpeta correspondiente, en archivos CSV con el formato estándar del proyecto.
- Consolidar los resultados en `analisis_comparativo/ablation_comparison_F2.csv`.

### Métricas y criterios
- **success_last_100**: éxito últimos 100 episodios
- **success_rate_total**: éxito total
- **first_success_episode**: primer éxito
- **convergence_episode**: convergencia
- **gate/gate_passed**: umbral y superación

### Interpretación
- Si quitar un componente reduce el éxito >20% respecto a v10, se considera crítico.
- Documentar cualquier hallazgo inesperado o desviación del protocolo.

### Referencias
- Preregistro: `PREREGISTRO_ABLATION_COMPONENTES_v10.md`
- Runner: `scripts/run_ablation_componentes_v10.py`
- Plantillas: `TEMPLATE_RESULTADOS_VARIANTE.md` en cada subcarpeta

---

*README de Fase 2 generado para trazabilidad y reproducibilidad. Revisión: 2025-12-05.*
