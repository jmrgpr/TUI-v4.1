# FASE 1 – Ablation del Curriculum (A/B/D/C)

## Instrucciones
1. Ejecutar cada configuración (A, B, D, C) siguiendo los scripts y setups definidos.
2. Registrar los resultados en los archivos TEMPLATE_RESULTADOS_X.md de cada carpeta.
3. Documentar observaciones, métricas y hallazgos relevantes.
4. Comparar los resultados entre configuraciones para evidenciar el impacto del curriculum y sus variantes.

## Configuraciones
- **A:** Curriculum baseline (4×4 → 6×6 → 8×8)
- **B:** Directo 8×8 (sin curriculum)
- **D:** Solo 6×6 (sin curriculum ni transfer)
- **C:** Curriculum inverso (8×8 → 6×6 → 4×4)

## Criterios de interpretación
- ¿El curriculum mejora la convergencia y el éxito?
- ¿Qué configuración muestra mayor robustez?
- ¿Qué diferencias se observan en las métricas clave?

## Registro y trazabilidad
- Mantener symlinks/copia de los archivos originales.
- Documentar cualquier desviación del protocolo.
- Asegurar reproducibilidad y claridad en la interpretación.
