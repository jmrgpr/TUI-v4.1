# Indice maestro de resultados (`results/`)

Este indice ordena resultados sin eliminar historico.

## Clasificacion operativa

- **Canonico**: resultados finales por fase/serie que sustentan reportes y conclusiones.
- **Trabajo**: corridas intermedias necesarias para analisis iterativo.
- **Temporal**: archivos de depuracion, pruebas ad-hoc o artefactos auxiliares.

## Reglas de ubicacion

1. Los resultados canonicos deben quedar en la carpeta de fase/serie correspondiente.
2. Los temporales no deben mezclarse con cierres oficiales.
3. Todo resultado usado en un reporte debe ser rastreable a script y commit.

## Convenciones de nombre sugeridas

- `F<fase>_<tipo>_<version>.csv`
- `F<fase>_<tipo>_<version>.md`
- `<serie>_<fase>_<seed|batch>_<variant>.csv`

## Minimo de metadatos para artefacto canonico

- fase o experimento de origen
- fecha de generacion
- script/comando usado
- parametros clave (risk, budget, seed, variante)

## Nota de gobernanza

No se borra historico existente. Este indice aplica desde ahora para mejorar orden y auditoria en `main`.
