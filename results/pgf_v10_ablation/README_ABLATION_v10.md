# Plan de Ablation v10

Este documento describe el protocolo, objetivos y estructura de los experimentos de ablation para cerrar la familia v10.

## Objetivo
Evidencia fuerte de la importancia del curriculum y sus componentes (shaping, transfer, etc.), con conexión clara a PGF/TUI y trazabilidad total.

## Estructura
- **Bloque A:** Núcleo v10 (curriculum vs directo vs 6x6 vs inverso)
- **Bloque B:** Ablation por componente, mínima, combinada, hiperparámetros
- **Bloque C:** Ablation TUI/PGF (run_ablation_quick.py)

## Layout de carpetas
Ver estructura en el README principal.

## Trazabilidad
- Preregistro, resultados por carpeta, reportes interpretando cada variante.
- v10_viable intocable como baseline.

## Estado
Preparado para ejecución ordenada y registro de resultados.

## Estado Fase 2 – Ablation de Componentes (8×8)
- Baseline (RL puro): 84% ± 2.6% (3 seeds) – robusto.
- +Regularización: 94.7% ± 4.0% – mejora y más estable.
- +RewardExtra: 56% ± 30.3% – peor e inestable.
- +Shaping (PGF como reward): 0% en las 3 seeds – colapso total.
- Curriculum como componente aislado: solo seed 101 completa 4×4→6×6→8×8; seeds 13 y 42 fallan el gate en 4×4 (experimento abortado según preregistro).

Conclusión:
- Incluir regularización en el stack estable.
- No adoptar reward_extra.
- Descartar PGF como reward directo (shaping) en v10; usar PGF solo como métrica offline.
- Curriculum es útil pero frágil; documentar gates/abortos por seed.
