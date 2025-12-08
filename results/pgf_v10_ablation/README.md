# Carpeta de resultados de ablation v10

Esta carpeta contiene todos los experimentos, reportes y análisis de la ablation v10. Cada subcarpeta documenta una variante o componente.


**Nota:**
- La regularización (dropout y L2) está desactivada por defecto en todas las variantes para igualar el baseline v10 (Config B). La variante `noregularization` también la desactiva explícitamente.
- El shaping utiliza `EvaluatorPGF` (confirmar si es exactamente el baseline de Config B).
- Por defecto, transfer y curriculum están desactivados (igual que Config B). Solo se activa curriculum en la variante `curriculum` y transfer si se pasa un checkpoint explícitamente.

No eliminar ni ignorar: toda la trazabilidad y reproducibilidad depende de esta estructura.