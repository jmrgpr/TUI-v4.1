# Resultados experimentales: desbloqueo RL/TUI

# Resultados experimentales: auditoría y consistencia

## Configuración crítica usada (impresa en runtime)

Las siguientes cifras se obtuvieron directamente de los archivos generados en las ejecuciones experimentales.

### Baseline Tabular
Fuente: `tabular_easy_log.txt`, episodios 1–500
Reward media últimos 50: 2484.23
Reward máxima: 2701.9
Reward mínima: 1.3
500/500 episodios con reward > 0

### Agente Complejo Patched
Fuente: `patched_seed42_risk0.5_episodes.csv`
Reward media: -59.32
Oscilación entre -35.4 y -106.8 por episodio, sin acercarse a valores positivos.

### Métrica de Recompensa
La columna "Recompensa" en los CSV corresponde a la sumatoria de penalización_por_paso, bonus_meta, bonus_avance, término_riesgo y otros factores por episodio.
Si se detecta algún término inesperado, se documenta aquí.

**Actualizado el 26/11/2025 tras auditoría de logs.**


---

# Plan de tuning del agente complejo

## Objetivo
Lograr que el agente complejo alcance reward media > 0 (ideal > 100) en el entorno easy (3x3, penalizaciones bajas, bonus meta 100), con criterios claros y reproducibles.

## Estrategia

### 1. Simplificación radical del input
- Implementar un modo debug o parámetro `state_mode` en el agente:
	- "coords_only": solo pasa [x, y] como estado.
	- "abstract": pasa el vector completo.
- Comparar ambos modos:
	- Si con (x, y) el DQN aprende y se acerca al tabular → el problema es el vector abstracto.
	- Si ni con (x, y) aprende → el problema es hiperparámetros/arquitectura.

### 2. Tuning de hiperparámetros (uno a la vez)
- Learning Rate: barrer valores {1e-3, 5e-4, 1e-4}.
- Gamma: probar {0.90, 0.95, 0.99}.
- Epsilon/exploración: aumentar exploración inicial y ralentizar el decay.
- Tamaño de red: probar 1–2 capas de 16–64 neuronas (en grid pequeño, menos es más).
- Normalización/clipping: probar reward/100 o tanh(reward) antes de acumular en el target; documentar la transformación usada.

### 3. Diagnóstico de penalizaciones
- Usar modo debug_reward_trace para imprimir términos del reward en 1–2 episodios.
- Añadir columnas al CSV: reward_total, penalizacion_paso, bonus_meta, bonus_avance, term_riesgo, etc.
- Documentar cualquier penalización inesperada en este archivo.

### 4. Documentar cada experimento
- Naming scheme para los experimentos: DQN_easy_xy_lr1e-3_gamma0.95_epsSlow_seed42.csv.
- Añadir tabla resumen en este archivo:

| Experimento | State | LR | Gamma | Eps | Reward media | % episodios > 0 | Comentarios |
|-------------|-------|----|-------|-----|--------------|-----------------|-------------|
| EXP01       | (x,y) |1e-3| 0.95  |eps-decay rápido| ...          | ...            | ...         |

- Medir reward media sobre los últimos N episodios (ej. 100) y confirmar con varias seeds (42, 123, 456).

## Criterio de éxito
- Umbral 1: reward media > 0 consistente.
- Umbral 2: reward media > 100 y tendencia clara de mejora hacia el baseline tabular.
- Validar con al menos 2–3 seeds distintas.
- Reward media primeros 50: 1663.2
- Reward máxima: 2701.9
- Reward mínima: 1.3
- Episodios con reward > 0: 500/500

**Conclusión:** El RL tabular aprende y maximiza el reward en el entorno easy. El entorno y la función de recompensa están correctos.

## Smoke test patched (get_abstract_state con coords)
- Script: `sim/prototipo_rl_simbiosis.py --episodes 50 --seed 42 --risk_scale 0.5 --output_prefix results/smoke_test/patched`
- Penalizaciones bajas, coords añadidas al estado abstracto.
- Reward media (control): -59.32
- Recompensa sigue negativa, aunque el agente ahora "ve" su posición.

**Conclusión:** El parche de visibilidad no es suficiente para que el agente complejo aprenda en el entorno easy. El siguiente paso es revisar hiperparámetros y arquitectura del agente complejo.

**Estado científico:**
- El entorno y la reward están validados.
- El RL tabular funciona con estado informativo.
- El agente complejo requiere ajuste adicional para aprender en el entorno easy.
- Todos los datos y configuraciones han sido auditados y son consistentes.
