# Checklist de cierre de fase (serie v11/v12+)

Usar este checklist antes de marcar una fase como cerrada.

## 1) Metodo y preregistro

- [ ] Existe preregistro o justificacion equivalente.
- [ ] Se documentaron desviaciones (si hubo) con motivo.
- [ ] El criterio GO/NO-GO esta explicitado.

## 2) Ejecucion y datos

- [ ] El runner/script de fase esta versionado.
- [ ] Los outputs canonicos existen y tienen naming consistente.
- [ ] Se separaron artefactos temporales de resultados finales.

## 3) Analisis

- [ ] Se ejecuto analisis preregistrado (o se justifico cambio).
- [ ] Se verificaron metricas clave e invariantes.
- [ ] Se validaron tablas/resumenes contra dataset canonico.

## 4) Documentacion

- [ ] `INDEX` de la serie/fase actualizado.
- [ ] Reporte de cierre actualizado (`*_CLOSURE_REPORT.md`).
- [ ] `README` de fase refleja estado real.

## 5) Reproducibilidad

- [ ] Comandos de reproduccion documentados.
- [ ] Dependencias/entorno referenciados.
- [ ] Integridad de artefactos finales (hash/manifiesto) cuando aplica.

## 6) Gobernanza

- [ ] Decision final de cierre validada por el arquitecto.
- [ ] Mensaje de commit de cierre usa prefijo adecuado (`F#:` o `DOCS:`).
