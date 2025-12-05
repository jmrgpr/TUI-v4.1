# PREREGISTRO_ABLATION_COMPONENTES_v10.md

## Preregistro Fase 2 – Ablation por Componentes y Hiperparámetros (v10)

**Fecha:** 2025-12-05

### Objetivo
Descomponer el aporte de cada componente del agente v10 (shaping, curriculum, transfer, reward extra, regularización, hiperparámetros) mediante variantes controladas y análisis comparativo.

### Variantes a ejecutar
- **component_minimal:** agente con solo lo esencial (sin shaping, sin transfer, sin curriculum, sin reward extra, sin regularización).
- **component_noshaping:** igual a v10 pero sin shaping.
- **component_notransfer:** igual a v10 pero sin transfer learning.
- **component_nocurriculum:** igual a v10 pero sin curriculum.
- **component_norewardextra:** igual a v10 pero sin reward extra.
- **component_noregularization:** igual a v10 pero sin regularización.
- **component_combined:** combinaciones de las anteriores.
- **hyperparam_sweep:** barrido de hiperparámetros (ej. learning rate, gamma, batch size).

### Seeds por variante
- 2 seeds por variante (ejemplo: 13, 42).

### Presupuesto de episodios
- 1000 episodios por variante y seed (ajustable según resultados preliminares).

### Métricas y criterios de interpretación
- **success_last_100:** éxito últimos 100 episodios.
- **success_rate_total:** éxito total.
- **first_success_episode:** primer éxito.
- **convergence_episode:** convergencia.
- **gate/gate_passed:** umbral y superación.
- **Comparativa:** Si quitar un componente reduce el éxito >20% respecto a v10, se considera crítico.

### Criterios de exclusión
- Si una variante no converge tras 1000 episodios, se documenta como tal.

### Estructura de carpetas
- results/pgf_v10_ablation/component_minimal/
- results/pgf_v10_ablation/component_noshaping/
- results/pgf_v10_ablation/component_notransfer/
- results/pgf_v10_ablation/component_nocurriculum/
- results/pgf_v10_ablation/component_norewardextra/
- results/pgf_v10_ablation/component_noregularization/
- results/pgf_v10_ablation/component_combined/
- results/pgf_v10_ablation/hyperparam_sweep/
- results/pgf_v10_ablation/analisis_comparativo/

### Notas
- No modificar scripts ni resultados de Fase 1 ni baseline v10_viable.
- Documentar cualquier desviación o hallazgo inesperado.

---

*Preregistro científico para Fase 2 de ablation v10. Revisado y fijado antes de ejecución.*
