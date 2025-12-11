# F0_baseline — Protocolo v11

**Propósito:**
Validar la instrumentación y pipeline completo bajo condiciones controladas (baseline), con todas las métricas mecánicas y científicas del protocolo v11.

**Diseño experimental:**
- Entorno: SimbiosisEnv
- Agentes: control, simbiosis, dqn_control
- Grid sizes: 8x8 y 16x16
- Risk scale: low
- Semilla: 42
- Episodios: 100 por configuración
- Métricas: Todas las del protocolo v11, incluyendo risk_effective y surprise
- Exportación: JSON y CSV por episodio, con columnas informativas

**Metadatos:**
- Protocolo: v11
- Commit git: 0290b03ae6acefb3d9a85793ab410c3ac8badeb4
- Fecha: 2025-12-10
- Configuración global: ver metadata.json
- Scripts usados: sim/prototipo_rl_simbiosis.py, sim/runner.py
- Comandos de lanzamiento: ver metadata.json

**Notas:**
- Los datos crudos se guardan en `raw/`, los análisis en `analysis/`.
- Los archivos de resultados incluyen agente, grid, riesgo, semilla y protocolo en el nombre (por ejemplo: `grid8_risklow_seed42_v11.json` y `grid8_risklow_seed42_v11_episodes.csv` bajo `raw/`).
- Este README y el metadata.json garantizan trazabilidad y reproducibilidad científica.
