# PREREGISTRO_ABLATION_COMPONENTES_v10.md

## Preregistro Fase 2 – Ablation por Componentes y Hiperparámetros (v10)

**Fecha:** 2025-12-05

## Objetivo
Descomponer el aporte de cada componente del agente v10 (shaping, curriculum, transfer, reward extra, regularización, hiperparámetros) mediante variantes controladas y análisis comparativo.

## Variantes a ejecutar (prioridad y definición)
- **component_minimal:** Solo lo esencial (control negativo). Sin shaping, sin transfer, sin curriculum, sin reward extra, sin regularización. Solo goal_reward + step_cost.
- **component_noshaping:** Igual a Config B pero sin reward shaping intermedio. Solo goal_reward final.
- **hyperparam_sweep:** Sweep de learning rate (lr=0.0005, 0.001, 0.005), gamma, batch size.
- **component_notransfer:** Igual a Config B pero sin transfer learning (menos prioritario).
- **component_combined:** Combinaciones (ej. sin shaping + sin regularización, sin epsilon decay).
- **component_norewardextra:** Solo si Config B usa rewards extra (verificar código).
- **component_noregularization:** Solo si Config B usa dropout/L2 (verificar código).

**Nota importante:** Por defecto, la regularización (dropout y weight_decay/L2) está desactivada en todas las variantes para igualar el baseline v10 (Config B). La variante `noregularization` también la desactiva explícitamente.

Por defecto, transfer y curriculum están desactivados (igual que Config B). Solo se activa curriculum en la variante `curriculum` y transfer si se pasa un checkpoint explícitamente.

**Shaping:** Se utiliza `EvaluatorPGF` como función de shaping baseline, igual que en v10. Confirmar que los campos de `info` en el entorno son compatibles.

**Curriculum/Transfer:** El runner F2 solo ejecuta 8x8 directo; el flag curriculum no activa fases multi-grid y transfer solo carga checkpoint si se pasa explícitamente. Si se requiere ablation real de curriculum/transfer, se debe implementar wiring multi-fase.

## Seeds por variante
- 2 seeds por variante (13, 42).

## Presupuesto de episodios
- 1000 episodios por variante y seed (ajustable según resultados preliminares).
- Grid: 8x8 (coherente con Config B).

## Métricas y criterios de interpretación
- **success_last_100:** Éxito últimos 100 episodios.
- **success_rate_total:** Éxito total.
- **first_success_episode:** Primer éxito.
- **convergence_episode:** Convergencia.
- **gate/gate_passed:** Umbral y superación.
- **Comparativa:** Si quitar un componente reduce el éxito >20% respecto a Config B, se considera crítico.

### Criterios de exclusión
- Si una variante no converge tras 1000 episodios, se documenta como tal.

## Estructura de carpetas
```
results/pgf_v10_ablation/
├── component_minimal/
│   ├── seeds/seed_0013/
│   └── seeds/seed_0042/
├── component_noshaping/
│   └── ...
├── component_notransfer/
├── component_combined/
├── hyperparam_sweep/
│   ├── lr_0005/
│   ├── lr_001/
│   └── lr_005/
└── analisis_comparativo/
	├── ablation_comparison_F2.csv
	└── graficos_F2.png
```

## Protocolo de ejecución
1. Documentar variantes, seeds y parámetros en este preregistro antes de correr.
2. Ejecutar variantes prioritarias:
   - component_minimal (control negativo)
   - component_noshaping
   - hyperparam_sweep (LR)
3. Guardar resultados por variante y seed en su carpeta correspondiente.
4. Consolidar resultados en analisis_comparativo/ablation_comparison_F2.csv
5. Analizar impacto de cada componente y sensibilidad a hiperparámetros.

## Decisión rápida de ejecución
- Opción 1: Mínimo viable (1 seed, 3 variantes)
- Opción 2: Completo (2 seeds, 3 variantes × 3 LR)
- Opción 3: Inteligente (adaptar según primeros resultados)

## Notas
- No modificar scripts ni resultados de Fase 1 ni baseline v10_viable.
- Documentar cualquier desviación o hallazgo inesperado.
- Mantener trazabilidad y reproducibilidad total.

---

*Preregistro científico para Fase 2 de ablation v10. Revisado, expandido y fijado antes de ejecución (2025-12-05).* 
