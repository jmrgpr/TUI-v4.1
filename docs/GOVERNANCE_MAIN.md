# Governance en `main` (TUI-v4.1)

Este proyecto opera con gobernanza centralizada en `main`.
La autoridad de arquitectura y decision final de cambios recae en Jose Manuel.

## Principios

1. `main` es la rama de trabajo y de verdad operativa.
2. No se elimina historial cientifico ni evidencia previa.
3. Todo cambio debe mantener trazabilidad reproducible (codigo -> datos -> reporte).
4. El rigor metodologico tiene prioridad sobre velocidad.
5. Los resultados oficiales se distinguen de artefactos temporales.

## Reglas de cambio

- Todo commit debe declarar su tipo y objetivo cientifico/tecnico.
- Todo experimento nuevo debe tener:
  - preregistro o justificacion explicita,
  - script de ejecucion reproducible,
  - salida verificable (CSV/JSON/MD),
  - nota de cierre (GO/NO-GO o estado parcial).
- Los cambios de documentos de publicacion deben indicar version y fecha.
- No se reescribe historial de `main` salvo instruccion explicita del arquitecto.

## Convencion de prefijos de commit

Usar uno de estos prefijos al inicio del mensaje:

- `F#:` fase experimental (ej. `F9:`)
- `RV:` repair validation
- `PREREG:` preregistro
- `ANALYSIS:` analisis estadistico o metodologico
- `DOCS:` documentacion, reportes, narrativa cientifica
- `INFRA:` tooling, CI/CD, dependencias, configuracion
- `DATA:` consolidacion/versionado de datasets y outputs canonicos
- `HOTFIX:` correccion urgente con impacto operativo

## Politica de evidencia

- Los resultados canonicos deben tener identificador de fase/serie.
- Cuando aplique, incluir manifiesto de integridad (hashes) para artefactos finales.
- Los resultados temporales o voluminosos deben ir a area no canonica o externa, dejando referencia en el repo.

## Decision y autoridad

- Arquitecto del proyecto: Jose Manuel.
- El agente ejecuta y propone; la decision final de direccion y publicacion la toma el arquitecto.
