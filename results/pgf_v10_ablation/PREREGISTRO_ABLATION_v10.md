# Preregistro Ablation v10

**Fecha:** 2025-12-05
**Responsable:** jmrgpr

## Objetivo
Demostrar, con evidencia fuerte y trazabilidad, la importancia del curriculum y sus componentes (shaping, transfer, etc.) en el desempeño RL, y conectar los resultados con PGF/TUI.

## Preguntas principales
- ¿Hace falta curriculum o 8×8 aprende solo?
- ¿El 6×6 es realmente el crisol?
- ¿El orden del curriculum importa?
- ¿Qué aporta cada componente (shaping, transfer, reward extra, regularización)?
- ¿El éxito depende de tuning fino de hiperparámetros?
- ¿PGF/TUI mejora estabilidad, prudencia, eficiencia?

## Diseño experimental
### FASE 1 – Núcleo v10
- A: Curriculum baseline (symlink a v10_viable)
- B: 8×8 directo, sin curriculum, N=3 seeds
- D: solo 6×6 (crisol)
- C: curriculum inverso (opcional)

### FASE 2 – Ablation por componente / mínima / combinada / hiperparámetros
- Minimal: sin shaping/transfer/extra
- Componentes: noshaping, nocurriculum, notransfer, norewardextra, noregularization
- Combinadas: sin shaping + sin curriculum, etc.
- Hyperparam sweep: LR, gamma, batch size

### FASE 3 – Ablation TUI/PGF
- tui_only, tui_pgf_light, tui_pgf_heavy
- Seeds: [42, 123, 456]
- Risk scales: [0.5, 1.0, 1.5, 2.0, 3.0]
- 200 episodios por combinación

## Criterios de éxito e interpretación
- Comparar success_last_100, breakthrough, robustez, sensibilidad.
- Documentar resultados y narrativa en reportes por carpeta.
- Mantener v10_viable intocable como baseline.

## Trazabilidad
- Carpeta y reporte por variante.
- Preregistro, resultados, análisis y conclusiones documentados antes de avanzar a v11.
