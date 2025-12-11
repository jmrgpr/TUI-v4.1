# Reporte Final — Experimento F0 (Protocolo v11)

## 1. Introducción

Este documento resume el análisis científico y los hallazgos principales del experimento F0 bajo el protocolo v11, siguiendo los más altos estándares de trazabilidad y reproducibilidad. El objetivo es validar la instrumentación, el pipeline y la capacidad del sistema para distinguir entre agentes y condiciones experimentales en entornos de bajo riesgo.

## 2. Datos y configuración experimental

- **Fuente de datos:**
  - `results/v11/F0_baseline/raw/grid8_risklow_seed42_v11.json/csv`
  - `results/v11/F0_baseline/raw/grid16_risklow_seed42_v11.json/csv`
- **Episodios:** 100 por agente y grid
- **Agentes:** control, simbiosis (TUI/PGF), dqn_control
- **Grids:** 8×8 y 16×16
- **Riesgo:** risk_scale=0.5, risk_level=low
- **Protocolo:** v11
- **Semilla:** 42

## 3. Métricas clave analizadas

- Recompensa ambiental (avg_reward)
- Flexibilidad (avg_flex)
- Robustez (avg_robust)
- Acción óptima (avg_q_opt)
- IPG (Índice Prudencial Global)
- Utilidad proxy y humana (u_proxy, u_humans)
- risk_effective_mean
- surprise_mean
- PGF_Bruto_Avg, PGF_Costo_Avg

## 4. Resultados principales

### Grid 8×8, riesgo bajo

- **Control:**
  - avg_reward ≈ -18.84
  - avg_flex = 0.50, avg_robust = 1.00, avg_q_opt ≈ 0.842
  - IPG ≈ 0.668
  - u_proxy ≈ -0.624, u_humans ≈ 0.763
  - risk_effective_mean ≈ 0.336, surprise_mean = 0.0
- **Simbiosis (TUI/PGF):**
  - avg_reward ≈ +14.61
  - avg_flex = 0.50, avg_robust ≈ 0.991, avg_q_opt ≈ 0.847
  - IPG ≈ 0.668
  - u_proxy ≈ -0.766, u_humans ≈ 0.773
  - risk_effective_mean ≈ 0.349, surprise_mean = 0.0
- **DQN-Control:**
  - avg_reward ≈ -24.08
  - avg_flex = 0.50, avg_robust ≈ 0.989, avg_q_opt ≈ 0.845
  - IPG ≈ 0.668
  - u_proxy ≈ -0.768, u_humans ≈ 0.773
  - risk_effective_mean ≈ 0.348, surprise_mean = 0.0

### Grid 16×16, riesgo bajo

- **Control:**
  - avg_reward ≈ -21.19
  - avg_flex = 0.50, avg_robust ≈ 0.999, avg_q_opt ≈ 0.842
  - IPG ≈ 0.503
  - u_proxy ≈ -0.706, u_humans ≈ 0.773
  - risk_effective_mean ≈ 0.250, surprise_mean = 0.0
- **Simbiosis (TUI/PGF):**
  - avg_reward ≈ +15.12
  - avg_flex = 0.50, avg_robust ≈ 0.991, avg_q_opt ≈ 0.847
  - IPG ≈ 0.668
  - u_proxy ≈ -0.745, u_humans ≈ 0.773
  - risk_effective_mean ≈ 0.265, surprise_mean = 0.0
- **DQN-Control:**
  - avg_reward ≈ -24.08
  - avg_flex = 0.50, avg_robust ≈ 0.989, avg_q_opt ≈ 0.845
  - IPG ≈ 0.668
  - u_proxy ≈ -0.745, u_humans ≈ 0.773
  - risk_effective_mean ≈ 0.263, surprise_mean = 0.0

## 5. Lectura crítica y hallazgos

- Ningún agente dispara tripwires ni shocks (surprise_mean = 0.0), validando la seguridad y calibración del entorno.
- Simbiosis (TUI/PGF) logra recompensa ambiental positiva y estable en ambos grids, sin sacrificar flexibilidad, robustez ni acción óptima.
- risk_effective_mean es similar entre agentes dentro de cada grid; la ventaja de simbiosis no proviene de “jugar con el riesgo”.
- El IPG del control se degrada al escalar el grid, mientras que simbiosis y DQN-Control lo mantienen alto.
- Los proxies muestran la clásica misalineación reward ambiental vs utilidad humana, que el protocolo v11 busca visibilizar.
- El sistema de métricas mecánicas (risk_effective, surprise) funciona correctamente y no es explotado por los agentes.

## 6. Conclusión

- El experimento F0 valida la instrumentación, el pipeline y la capacidad del sistema para distinguir entre agentes y condiciones de forma robusta y trazable.
- Simbiosis (TUI/PGF) demuestra ventajas claras en reward y estabilidad sin aumentar el riesgo ni las sorpresas.
- El sistema de logging y métricas cumple con los requisitos de reproducibilidad y trazabilidad científica.

## 7. Próximos pasos sugeridos

- Ejecutar F1 con risk_scale alto o red_team activado para estresar el sistema y observar el comportamiento bajo condiciones adversas.
- Analizar la aparición de sorpresas y cambios en risk_effective bajo escenarios de mayor riesgo.

---

_Reporte generado automáticamente a partir del análisis notebook y revisión científica._
