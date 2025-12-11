# Preregistro — Experimento F1_v11 (High Risk)

**Fecha:** 11 de diciembre de 2025  
**Proyecto:** TUI-v4.1  
**Investigador:** jmrgpr  
**Protocolo:** v11

---

## 1. Objetivo científico
Poner a prueba la TUI/Simbiosis en condiciones adversas:
- Riesgo alto (`risk_scale = 1.5`, `risk_level = high`).
- Incidentes frecuentes (tripwires/shocks) para activar `surprise` y mover `risk_effective`.
- Comparar Simbiosis vs Control y DQN-Control.

## 2. Preguntas / Hipótesis
- ¿Simbiosis reduce efectivamente riesgo y sorpresas frente a Control y DQN-Control?
- ¿Mantiene IPG razonable cuando el entorno ya no es trivial?
- ¿Aparecen modos de fallo (parálisis, over-prudencia) similares a v8 o se evitan con el diseño v11?

## 3. Diseño experimental
- Grids: 8×8 y 16×16.
- Agentes: control, simbiosis (TUI/PGF), dqn_control.
- Episodios: 200 por configuración.
- Seed: 42.
- `pgf_mix`: 0.2.
- Red team: False (solo riesgo alto constitutivo).
- Output: `results/v11/F1_highrisk/raw/`.

## 4. Comandos de ejecución (ejemplo)

```powershell
python -m sim.prototipo_rl_simbiosis `
  --episodes 200 `
  --seed 42 `
  --grid_size 8 `
  --risk_scale 1.5 `
  --risk_level high `
  --dqn_control `
  --pgf_mix 0.2 `
  --output_prefix results/v11/F1_highrisk/raw/grid8_riskhigh_seed42_v11

python -m sim.prototipo_rl_simbiosis `
  --episodes 200 `
  --seed 42 `
  --grid_size 16 `
  --risk_scale 1.5 `
  --risk_level high `
  --dqn_control `
  --pgf_mix 0.2 `
  --output_prefix results/v11/F1_highrisk/raw/grid16_riskhigh_seed42_v11
```

## 5. Métricas y análisis esperados
- Incidencia de eventos adversos: `avg_tripwire`, `avg_shocks`, `surprise_mean`, `risk_effective_mean`.
- Comparaciones clave: `avg_reward`, `IPG`, `tripwire_steps`, `avg_survival`.
- Visualizaciones: evolución temporal de `risk_effective`, `reward`, `IPG`, `sorpresas`.
- Detección de patrones de parálisis o over-prudencia.

## 6. Criterios de éxito
- Simbiosis debe mostrar robustez y alineación superior o igual a los controles, sin aumentar el riesgo ni la frecuencia de sorpresas.
- El sistema debe registrar cualquier colapso de seguridad o alineación.

## 7. Traza y reproducibilidad
- Registrar git commit, parámetros globales y comandos en `metadata.json`.
- Mantener notebook de análisis (`analysis/analisis_F1_v11.ipynb`) y reporte final.
- Guardar datos crudos en `raw/` con nombres informativos (agente, grid, riesgo, seed, protocolo).

---

_Registro generado para trazabilidad y reproducibilidad del experimento F1 (High Risk) bajo protocolo v11._
