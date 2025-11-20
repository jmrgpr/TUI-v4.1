# Sugerencias concretas para el simulador (TUI v4.1/v4.2)

Guía breve y accionable para extender el simulador con los elementos propuestos
(IPG, tripwires, anti-oráculo, validación estadística y visualización). Cada
punto menciona rutas y ganchos existentes para acelerar la implementación.

## 1) Configuración reproducible y trazabilidad
- Centralizar semillas, horizontes, penalizaciones y rutas de salida en una
  **config dataclass** como `SimulationConfig` (`sim/examples/simbiosis_suggestion_template.py`).
- Guardar cada corrida en JSON/YAML junto con la configuración usada para
  auditoría rápida (p. ej., `results/run_<timestamp>.json`).

## 2) Bundle causal e IPG auditable
- Reusar `CausalMetricsBundle` como capa de acumulación de métricas (alineación,
  penalización de riesgo, brecha de propósito) y exponer métodos de resumen con
  medias + IC bootstrap.
- Conectar este bundle dentro del entorno real (e.g., `SimbiosisEnv`) en vez del
  bucle sintético del ejemplo.

## 3) Tripwires multi-horizonte
- En `TripwireMonitor.record`, añadir reglas específicas del dominio: detección
  de anomalías de recursos, divergencia entre proxy y IPG o cambios abruptos en
  la política.
- Persistir eventos (step, métrica, acción) para graficar y activar políticas de
  contención (ej.: congelar aprendizaje o reducir tasa de exploración).

## 4) Anti-oráculo pragmático / OPE
- Extender `AntiOracleGate.approve` para usar estimadores doubly-robust
  + bound inferior (LCB). Recomendado: biblioteca OPE de RLlib o implementación
  propia en `sim/metrics/ope_*.py`.
- Gatear despliegues offline: sólo permitir políticas con LCB positivo y
  varianza acotada.

## 5) Validación estadística
- Función `bootstrap_ci` ya ilustra percentiles 5-95; moverla a un módulo
  compartido (p. ej., `sim/metrics/bootstrap.py`) y añadir pruebas en
  `test/metrics/test_bootstrap.py`.
- Incluir pruebas de significancia (t-test/Mann–Whitney) para comparar agentes o
  configuraciones; reportar p-values y tamaños de efecto en los resúmenes.

## 6) Visualización publicable
- Generar curvas de IPG, brecha de propósito y eventos de tripwire usando
  matplotlib/plotly desde `scripts/` o `notebooks/`.
- Exportar automáticamente PNG/PDF para los reportes (folder `results/`).

## 7) Extensión de dominios y agentes
- Añadir entornos adicionales (biológicos/artificiales) en `sim/envs/` con
  interfaces homogéneas; incluir parámetros de riesgo y propósito en la
  observación.
- Incluir agentes de referencia (PPO/A2C) en `sim/agents/` para comparativas
  SOTA y validar que las métricas respondan correctamente a políticas diversas.

## 8) Automatización y CI
- Crear suites unitarias/integración para métricas, tripwires y gating en
  `test/`. Priorizar rutas críticas: bootstrap, OPE, detección de gaming.
- Añadir job de CI que ejecute lint + pruebas rápidas + generación de artefactos
  ligeros (tablas/JSON) para detectar regresiones de métricas.

## 9) Documentación bilingüe y ejemplos
- Mantener comentarios ES/EN dentro del código (ver plantilla actual) para que
  otros asistentes en VS Code puedan continuar sin ambigüedades.
- Proveer uno o más notebooks con ejemplos reproducibles (usar el bucle de
  `simbiosis_suggestion_template.py` como base) que muestren configuraciones,
  gráficos y uso del anti-oráculo.
