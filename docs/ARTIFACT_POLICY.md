# Politica de artefactos pesados en `main`

Objetivo: evitar crecimiento descontrolado del repo sin perder trazabilidad cientifica.

## Que si va al repo

- Codigo fuente y scripts reproducibles.
- Reportes de cierre y documentacion metodologica.
- CSV/JSON canonicos de tamano razonable para auditoria.
- Manifiestos de integridad (hashes) y metadatos.

## Que debe evitarse en `main`

- Binarios pesados repetitivos por corrida (raw masivo).
- Duplicados de artefactos exportados (mismo contenido, otro formato).
- Logs extensos temporales y checkpoints intermedios.

## Regla practica de tamano

- Si un archivo individual supera ~25 MB, evaluar almacenamiento externo.
- Si un conjunto por fase supera ~150 MB, dejar en externo y versionar manifiesto + resumen.

## Flujo recomendado

1. Ejecutar corrida local.
2. Conservar en repo solo salida canonica y resumen.
3. Guardar artefactos voluminosos en almacenamiento externo/release.
4. Publicar en repo:
   - referencia del paquete externo,
   - hash SHA256,
   - comando de reproduccion.

## Beneficio

Mantiene `main` auditable, liviano y sostenible para peer review.
