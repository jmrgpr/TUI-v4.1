# Protocolo de commits cientificos en `main`

Objetivo: mantener trazabilidad clara en una rama unica (`main`) sin perder rigor.

## Plantilla minima (obligatoria)

Cada commit de trabajo cientifico debe responder:

1. **Objetivo**: que se busca validar o corregir.
2. **Hipotesis o razon tecnica**: por que este cambio importa.
3. **Alcance**: modulos, scripts, fases o documentos afectados.
4. **Ejecucion**: comando(s) o procedimiento reproducible.
5. **Salida esperada**: artefactos que deben generarse o actualizarse.
6. **Criterio de cierre**: GO/NO-GO, PASS/FAIL o estado parcial.

## Formato recomendado de mensaje

`<PREFIJO>: <accion breve>`

Ejemplos:

- `F9: piloto CFR high-risk con budget calibrado`
- `RV: validar invariantes tras fix de lifecycle`
- `ANALYSIS: rerun bootstrap no parametrico con master limpio`
- `DOCS: cierre de fase y sintesis v11 -> v12`

## Checklist pre-commit

- [ ] El cambio conserva compatibilidad con estructura del repo.
- [ ] Existe trazabilidad entre codigo y salida.
- [ ] Los archivos pesados no esenciales no entran al repo.
- [ ] Se actualizaron notas de fase/reportes cuando aplica.
- [ ] El mensaje de commit usa prefijo y explica el "por que".

## Regla de oro

Si un tercero no puede reconstruir "que se hizo, por que y con que resultado" leyendo commits + docs, el commit no esta listo.
