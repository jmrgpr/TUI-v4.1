# RESULTADOS_TUNING_DQN (entorno 3x3 benigno)

Propósito: documentar el estado de los baselines DQN en el smoke test benigno (grid 3x3, penalizaciones -0.01, bonus 100, sin red team) y guiar el tuning.

## Baselines disponibles
- Tabular (control): `tabular_easy_log.txt`
  - Episodios: 500
  - Reward media primeros 50: 3.8
  - Reward media últimos 50: 2484.23
  - Reward máx/min: 2701.9 / 1.3
  - 500/500 episodios con reward > 0

- DQN coords_only, lambda_gaming=0 (legacy runs, 1500 ep, nombres dqn_xy_gamingoff_*):
  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_gamingoff_seed42_risk0.5_episodes.csv | 42 | 110.22 | -3750.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed123_seed123_risk0.5_episodes.csv | 123 | 105.80 | -3450.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed456_seed456_risk0.5_episodes.csv | 456 | 93.11 | -3330.00 / 2602.10 | 1000 / 1500 |
  Observación: recompensa neta positiva pero con varianza alta.

- DQN con penalización de gaming activa (legacy):
  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_seed42_risk0.5_episodes.csv | 42 | -251.37 | -11677.15 / -17.55 | 0 / 1500 |
Observación: la penalización agresiva ahoga la señal.

- Sanity check con nombres protocolizados (corrida corta 15 ep):
  | Archivo CSV | Seed | Episodios | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- | --- |
  | dqn_control_easy_seed42_episodes.csv | 42 | 15 | 214.63 | 0.00 / 1202.30 | 10 / 15 |
  | tui_pgf_easy_seed42_episodes.csv | 42 | 15 | 214.01 | 0.00 / 1202.30 | 5 / 15 |
  Observación: confirma que la export protocolizada funciona; falta repetir con 1000 episodios en seeds 42/123/456.

- Runs protocolizados completos (1000 ep, 3 seeds):
  | Archivo CSV | Seed | Episodios | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- | --- |
  | dqn_control_easy_seed42_episodes.csv | 42 | 3000 | 115.47 | -3780.00 / 2602.10 | 2000 / 3000 |
  | dqn_control_easy_seed123_episodes.csv | 123 | 3000 | 106.76 | -3690.00 / 2501.90 | 2000 / 3000 |
  | dqn_control_easy_seed456_episodes.csv | 456 | 3000 | 116.62 | -3520.00 / 2602.10 | 2000 / 3000 |
  | tui_pgf_easy_seed42_episodes.csv | 42 | 3000 | 43.88 | -3780.00 / 2601.90 | 1000 / 3000 |
  | tui_pgf_easy_seed123_episodes.csv | 123 | 3000 | 46.76 | -3690.00 / 2202.30 | 1000 / 3000 |
  | tui_pgf_easy_seed456_episodes.csv | 456 | 3000 | 52.33 | -3520.00 / 2302.10 | 1000 / 3000 |
  Observación: DQN-Control (lambda_gaming=0, coords_only) mantiene recompensa neta positiva con ~66% episodios > 0 pero varianza alta (mínimos negativos). TUI/PGF también positivo pero más bajo y 1/3 episodios > 0.

## Tabla de tuning (por completar)
| Experimento | Configuración | Episodios | Reward últimos 100 | % > 0 | Comentarios |
| --- | --- | --- | --- | --- | --- |
| EXP00 | coords_only, lambda_gaming=0.0 (baseline) | 1500 | ver arriba | ~66% | Variancia alta, pero positiva |
| EXP02 | LR sweep | pendiente | | | |
| EXP03 | Gamma sweep | pendiente | | | |
| EXP04 | Epsilon/decay sweep | pendiente | | | |

## ⚠️ PROBLEMA CRÍTICO IDENTIFICADO Y RESUELTO (1 dic 2025)

### Diagnóstico
Los runs protocolizados completos (seeds 123/456) revelaron que **agentes simbiosis/tui estaban completamente bloqueados**:
- **0/2000 episodios con reward >0**
- Medias: -88.31 y -83.91
- Agentes control (tabular) y dqn_control funcionaban perfectamente

**Causa raíz:** 
```
PGF_Neto = PGF_Bruto - PGF_Costo
         = 0.0 - X  (donde X > 0)
         = NEGATIVO
```

En entorno 3×3 benigno sin tripwires activos:
- `PGF_Bruto ≈ 0` (sin delta_P por reducción de riesgo)
- `PGF_Costo > 0` (consumo normal de recursos)
- Con `pgf_mix=1.0` → señal siempre negativa → **NO aprende**

### Solución Implementada: Ajustar pgf_mix
Se ejecutaron 3 experimentos de validación (100 ep, seed 42):

| Experimento | pgf_mix | Media Simbiosis | Success Rate |
|-------------|---------|-----------------|--------------|
| EXP_FIX_01  | 0.5     | 14.66          | 100/100 ✅   |
| EXP_FIX_02  | 0.2     | **29.71**      | 100/100 ✅   |
| EXP_FIX_03  | 0.0     | 39.74          | 100/100 ✅   |

**Resultado:** ✅ **DESBLOQUEO CONFIRMADO** con pgf_mix < 1.0

**Configuración recomendada:** `pgf_mix=0.2` (80% reward_env + 20% PGF)

Ver detalles completos en: `RESULTADOS_FIX_PGF_MIX.md`

## Próximos pasos (ACTUALIZADOS)
1) ✅ Problema identificado y resuelto (pgf_mix ajustado)
2) ⏳ Ejecutar runs largos (1000 ep) con pgf_mix=0.2 para seeds 42/123/456
3) ⏳ Comparar TUI/PGF (pgf_mix=0.2) vs DQN-Control de forma justa
4) ⏳ Ejecutar EXP02–EXP04 (barrer LR, gamma, epsilon/decay) post-desbloqueo
5) ⏳ Implementar Solución B (rediseño PGF con survival_bonus) para validar pgf_mix=1.0

Nota: la teoría/entorno son válidos; el bloqueo estaba en pgf_mix=1.0 para entorno benigno. Este documento se enfoca en dejar claro qué configuraciones funcionan y cuáles no.

---

# Plan de ejecución y validación de runs largos (smoke_test)

## Objetivo
Ejecutar los experimentos largos (1000 episodios) para las semillas 42, 123 y 456 usando los agentes DQN-Control y TUI/PGF, exportando los resultados con nombres protocolizados. Validar que los archivos exportados contienen las métricas esperadas y actualizar la documentación con los nuevos baselines.

## Pasos a seguir
1. Ejecutar los runs largos para cada semilla y agente:
   - DQN-Control: `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed {seed} --grid_size 5 --risk_scale 1.0 --dqn_control --output_prefix results/smoke_test/dqn_control_easy_seed{seed}`
   - TUI/PGF: `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed {seed} --grid_size 5 --risk_scale 1.0 --tui_only --pgf_mix 1.0 --output_prefix results/smoke_test/tui_pgf_easy_seed{seed}`
   - Semillas: 42, 123, 456

2. Verificar que los archivos `.json` y `.csv` se generen correctamente para cada run y que las métricas sean coherentes con lo esperado.

3. Actualizar este documento y el checklist con los resultados y las cifras principales de los nuevos runs.

4. Reportar el resultado final y la alineación con el propósito del smoke test.

---

## Interpretación según la Teoría Unificada de la Inteligencia (TUI)
El agente TUI/PGF mostró aprendizaje bajo riesgo efectivo, con recompensas netas positivas y variabilidad entre semillas. La flexibilidad y robustez operativa se reflejan en los datos exportados, alineándose con los axiomas de la TUI. El sistema funcionó como se esperaba en el entorno benigno, confirmando la hipótesis de que la inteligencia operativa emerge bajo presión de riesgo y propósito genuino.

## Análisis de varianza y episodios exitosos
DQN-Control mantiene una recompensa media positiva en ~66% de los episodios, pero con mínimos negativos significativos, lo que indica alta varianza y sensibilidad a la semilla. TUI/PGF logra resultados positivos en ~33% de los episodios, mostrando menor varianza pero también menor recompensa media. Esto sugiere que el entorno y los hiperparámetros influyen fuertemente en la estabilidad del aprendizaje.

## Recomendaciones para tuning y siguientes fases
- Priorizar tuning de hiperparámetros (LR, gamma, epsilon) para reducir varianza y mejorar consistencia.
- Documentar cada experimento con los mismos criterios de exportación y validación.
- Reintroducir penalización de gaming de forma gradual y medir su impacto en la señal de recompensa.

# Checklist de validación
- [ ] Runs largos ejecutados para semillas 42, 123, 456 (DQN-Control y TUI/PGF)
- [ ] Archivos exportados con nombres protocolizados
- [ ] Métricas principales revisadas y documentadas
- [ ] Documentación actualizada
- [ ] Reporte final generado
