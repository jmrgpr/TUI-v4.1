# Preregistro F2_redteam v11

**Fecha:** 2025-12-15
**Protocolo:** v11
**Experimento:** F2 – Red Team y Ataques Adversariales

## Objetivo
Evaluar la resiliencia y alineación de TUI/Simbiosis, Control clásico y DQN-Control frente a ataques adversariales explícitos (red team) bajo condiciones de riesgo alto.

## Diseño Experimental
- **Agentes:** control, simbiosis, dqn_control
- **Grids:** 8×8, 16×16
- **Seeds:** 42, 101, 13, 7, 99
- **Episodios:** 200 por configuración
- **Parámetros globales:**
  - risk_scale = 1.2
  - risk_level = high
  - red_team = True
  - pgf_mix = 0.2
- **Ataques:**
  - Reward hacking
  - Distributional shift
  - Gaming de métricas mecánicas
- **Comandos de lanzamiento:**
  ```
  python -m sim.prototipo_rl_simbiosis --episodes 200 --seed <SEED> --grid_size <GRID> --risk_scale 1.2 --risk_level high --red_team --dqn_control --pgf_mix 0.2 --output_prefix results/v11/F2_redteam/raw/grid<GRID>_riskhigh_r1p2_seed<SEED>_v11
  ```

## Criterios de éxito (GO/NO-GO)
- El experimento es reproducible y trazable.
- Se detecta y documenta el impacto de los ataques en las métricas clave.
- Simbiosis mantiene robustez y alineación superior frente a los ataques.

## Trazabilidad y Documentación
- Resultados crudos y organizados por agente, grid y seed.
- Scripts y comandos archivados.
- Análisis y reportes en `analysis/`.

## Equipo responsable
- jmrgpr

---

**Este preregistro debe ser validado antes de ejecutar el experimento.**
