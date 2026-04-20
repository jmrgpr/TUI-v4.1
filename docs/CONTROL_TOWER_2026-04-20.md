# Control Tower 2026-04-20: Estado del Repo y Plan v12

## 1) Que es este repo
Este repositorio contiene tres capas que deben mantenerse separadas:
- Teoria TUI v4.2 (`TUI/`): marco conceptual y predicciones.
- Simulador (`sim/`): entorno y agentes para probar hipotesis.
- Evidencia experimental (`results/` + `scripts/`): ejecuciones, analisis y cierres.

Principio rector:
- La teoria no se valida por opinion.
- El simulador no valida por si solo.
- Solo los experimentos preregistrados y auditables cuentan como evidencia.

## 2) Estado tecnico actual (auditado)
Fecha de corte: 2026-04-20.

Snapshot cuantitativo (aprox):
- Archivos totales visibles en repo: 1052.
- `results/v11`: 651 archivos.
- `results/v12`: 31 archivos.
- `scripts/`: 154 archivos.
- `sim/`: 50 archivos.
- El mayor volumen fisico local esta en `.venv/` (dependencias), no en evidencia canonica.

### 2.1 Fortalezas
- Pipeline v11 muy maduro y auditable (F0-F8 + RV1/RV2 cerrados).
- Estructura de scripts amplia para consolidacion, analisis y manifiestos.
- Simulador central estable en `sim/prototipo_rl_simbiosis.py`.
- Politica de separacion canonico/raw ya definida en `.gitignore`.

### 2.2 Debilidades
- `README.md` raiz no refleja estado real actual (mezcla historico y codificacion degradada).
- Hay ruido operativo en raiz (archivos de auditoria local y snapshots tecnicos).
- No existe aun una torre de control unica y actualizada para v12 (hasta ahora).

## 3) Estado cientifico actual

### 3.1 Lo que SI esta probado (en este repo)
Base: `results/v11/` y `results/v11/INDEX_SERIE_V11.md`.

- La serie v11 logro un cierre confirmatorio de robustez bajo high-stakes (CFR) en F8, con trazabilidad formal de artefactos.
- Existe evidencia replicable de reduccion de fallo catastrofico en el regimen operacional definido por v11.
- Se cerraron validaciones de reparacion de runner (RV1 fail/no-go, RV2 pass/go), lo que mejora confianza metodologica post-errata.

### 3.2 Lo que NO esta probado
- No esta probado que `pgf_mix` sea mecanismo causal general de inteligencia util (v11 lo trata como knob operacional, no como ley teorica PGF).
- No esta probada universalidad fuera del entorno y protocolos usados.
- No esta probado mecanismo causal completo de TUI/PGF en terminos directos de pendiente de aprendizaje bajo manipulacion limpia de riesgo efectivo.

## 4) Estado v12 actual (real)
Base: `results/v12/`.

- Existe diseno, scaffolding y documentos de control (plan, index, templates).
- Solo hay runner v12 explicito para F2 (`results/v12/F2_redteam/run_F2_redteam_v12.py`).
- No hay evidencia canonicamente versionada de ejecucion completa F0-F6 en v12.
- Faltan reportes v12 esperados (`stats_report_v12`, `f3_pilot_selection_v12`, `f4_preregistered_report_v12`, etc.).

Conclusion:
- v12 esta en estado de "arquitectura de experimento", no de serie cerrada.

## 5) Por que v12 y para que
v12 no es "repetir por repetir". v12 existe para resolver tres huecos:

1. Generalizacion del hallazgo de robustez (arco v12-A):
- Validar que el efecto CFR no es un caso unico de un solo regimen.

2. Test directo de PGF (arco v12-B):
- Pasar de proxy/knob (`pgf_mix`) a prueba causal mas directa del principio (P-PGF-1).

3. Transicion de "simulador" a "mundo":
- Preparar la teoria para escenarios con mas friccion real (mas incertidumbre, retrasos, costo de error, y riesgo operativo).

## 6) Que falta por probar

### 6.1 En TUI (teoria)
- Si el riesgo efectivo manipulado causa cambios robustos en tasa de mejora (no solo en reward total).
- Si el efecto se sostiene en distintos regimenes sin tuning oportunista.
- Si el comportamiento alineado mantiene robustez bajo cambios de entorno y presion adversarial.

### 6.2 En experimentacion
- Cierres fase por fase F0-F6 con preregistro congelado y desviaciones trazadas.
- Manifiestos v12 completos (CSV canonico + hash JSON + reporte estadistico global).
- Repetibilidad inter-maquina (al menos dos ejecuciones limpias comparables).

### 6.3 En "mundo"
- Definir un entorno puente (mas cercano a operacion real) con:
  - observabilidad parcial,
  - retraso de retroalimentacion,
  - costos irreversibles,
  - tradeoff seguridad-rendimiento.

## 7) Decision recomendada desde ahora
No reiniciar desde cero en otro repo.

Ruta recomendada:
- Conservar este repo como continuidad cientifica.
- Rehacer v12 completo de forma limpia y auditada (fase por fase).
- Congelar una linea base reproducible antes de cada fase.

Razon:
- Preserva trazabilidad historica.
- Evita perder comparabilidad con v11.
- Reduce riesgo de "fork metodologico" sin control.

## 8) Plan de accion inmediato (orden)
1. Congelar baseline tecnico v12 (entorno, dependencias, estructura de salida).
2. Ejecutar F0-F2 y cerrar canonicamente cada fase.
3. Ejecutar F3 para seleccionar headroom CFR.
4. Ejecutar F4 confirmatorio H1-only (m=1).
5. Ejecutar F5 para generalizacion con una sola palanca causal.
6. Ejecutar F6 para PGF directo (P-PGF-1).
7. Publicar cierre v12 con manifiestos y reporte global.

## 9) Criterio de exito v12
v12 se considera "cerrado" cuando:
- Hay trazabilidad completa de artefactos por fase.
- Hay al menos un hallazgo confirmatorio replicado y un test PGF directo falsable.
- La evidencia distingue claramente "lo que se observo" de "lo que la teoria afirma".

## 10) Recordatorio de disciplina
- Cambiar una sola palanca causal por fase confirmatoria.
- No mezclar exploratorio con confirmatorio.
- No usar reportes narrativos como sustituto de artefactos canonicamente verificables.
