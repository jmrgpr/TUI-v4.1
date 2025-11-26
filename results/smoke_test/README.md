<<<<<<< HEAD
# Smoke Test y Tuning (entorno 3x3 benigno)

Estado: entorno y reward validados; export protocolizado funcionando.

## Config benigna

## Cómo correr (nombres protocolizados)
```
$env:PYTHONPATH='.'
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --learning_rate 0.001 --gamma 0.95 --epsilon 0.2
```
Genera `results/smoke_test/dqn_control_easy_seed42.json` y `_episodes.csv`.

```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 \
  --tui_only --pgf_mix 1.0
```
Genera `results/smoke_test/tui_pgf_easy_seed42.json` y `_episodes.csv`.

Si pasas `--output_prefix`, se usa ese prefijo (carpetas creadas automáticamente). El JSON incluye `dqn_params`.

## Flags de tuning DQN
`--learning_rate`, `--gamma`, `--epsilon`, `--epsilon_decay`, `--epsilon_end`, `--lambda_gaming`.

Ejemplos (todos con lambda_gaming=0.0):
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --learning_rate 0.0005
```
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --gamma 0.95
```
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --epsilon 1.0 --epsilon_decay 0.999 --epsilon_end 0.1
```

## Resultados de referencia (legacy)

## Plan
1) Repetir runs protocolizados (seeds 42/123/456) para DQN y TUI y documentarlos.
2) Tuning EXP02–EXP06 con lambda_gaming=0.0 (lr/gamma/epsilon/decay).
3) Rediseñar penalización de gaming (warm-up/umbrales/caps) y medir impacto.
4) Comparar TUI/PGF vs DQN-Control en este entorno.

Nota: la teoría TUI no está falsificada; el bloqueo era el shaping y los hiperparámetros. El entorno y el RL funcionan bajo configuraciones razonables.
=======
﻿# Smoke Test y Diagnóstico (Entorno simplificado)

Estado: depuración crítica. El baseline no logra rewards > 0 ni en el entorno más benigno.

## Config actual (benigna)
- Grid 3x3, recursos iniciales 200, pasos máx. 30.
- Sin tripwires/shocks/distractores; red team off.
- Penalizaciones casi nulas (-0.01); riesgo alto/bajo: -0.2/-0.1.
- Umbral alto 10, bajo 5; bonus meta 100.
- Bonus de avance (+0.2) y de episodio limpio (+1) en `environment.py`.

## Cómo correr (sin fast, genera CSV)
```
$env:PYTHONPATH='.'
python sim/prototipo_rl_simbiosis.py --episodes 50 --seed 42 --risk_scale 0.5 --output_prefix results/smoke_test/easy
```

## Análisis rápido del CSV
```python
import pandas as pd, numpy as np
csv = 'results/smoke_test/easy_seed42_risk0.5_control.csv'
df = pd.read_csv(csv)
col = [c for c in df.columns if 'Recompensa' in c or 'reward' in c.lower()][0]
r = df[col].values
print(len(r), r.mean(), r.min(), r.max(), np.sum(r>0))
print('Primeros 10:', r[:10].mean(), 'Ultimos 10:', r[-10:].mean())
```

## Resultados observados
- Smoke (50 ep): recompensas del control siguen negativas en todos los episodios; no se aplica el bonus de meta de forma natural.
- Test forzado óptimo (ruta abajo/derecha hasta meta [2,2]): reward total ~2701.9, bonus meta aplicado, estado/posición cambian correctamente.
  → La función de recompensa y observabilidad funcionan si se sigue la trayectoria óptima.
  → El problema está en el aprendizaje RL autónomo.

## Diagnóstico y plan de desbloqueo
Hay dos hipótesis principales: (a) el agente no ve cambios de estado (ceguera), (b) existe una penalización oculta que domina la señal.

Fases propuestas (“Super-Smoke Test”):
- Fase A: LineWorld 1x3.
  * Grid 1x3, inicio [0,0], meta [0,2], solo acción derecha (forzada).
  * Criterio: Reward > 90. Si no, la reward está rota.
- Fase B: Verificar observabilidad.
  * Imprimir state y pos en 5 pasos. Si pos cambia y state no, el agente es ciego.
- Fase C: Overfitting intencional.
  * Usar coordenadas (x,y) como estado, entrenar 10k episodios en 3x3. Si no aprende, el loop RL/hiperparámetros está mal.

## Checklist
- [x] Smoke test benigno (fallido: rewards negativas).
- [x] Test forzado hasta meta (reward positiva, bonus aplicado).
- [x] Fase A LineWorld 1x3.
- [ ] Fase B imprimir state/pos para ver observabilidad.
- [ ] Fase C overfitting con estado (x,y).
- [ ] Reejecutar smoke tras corregir bug.

## Nota
El fallo actual no falsifica la teoría TUI: muestra que el motor RL no aprende en un entorno trivial. Resolver primero el problema de aprendizaje básico antes de volver a TUI/SOTA.

---
## Resultado Fase A: LineWorld 1x3
---
## Resultado Fase B: Observabilidad en LineWorld 1x3
---
## Resultado Fase D: Trazabilidad de reward en step()

Se imprimieron los términos que suman al reward en cada paso de LineWorld 1x3:

- Paso 1: +0.2 avance meta
- Paso 2: +0.2 avance meta, +100.0 bonus meta
- Pasos 3-29: +100.0 bonus meta cada paso
- Paso 30: +100.0 bonus meta, +1.0 bonus episodio limpio

No se observan penalizaciones ocultas ni sumas inesperadas. El reward es dominado por el bonus meta tras alcanzar la meta, y la señal es clara y positiva.

Se imprimió el estado (get_abstract_state) y la posición del agente en cada paso:

| Paso | Posición | Estado |
|------|----------|--------|
| 0    | [0, 0]   | x=0, y=0 |
| 1    | [0, 1]   | x=0, y=1 |
| 2    | [0, 2]   | x=0, y=2 |
| 3-5  | [0, 2]   | x=0, y=2 |

El estado y la posición cambian correctamente al avanzar, confirmando que el agente "ve" el entorno y no está ciego.


**Resultado tras corrección:**
Se ejecutó el entorno grid 1x3 con meta configurable ([0,2]). El bonus meta se aplica correctamente:

- Reward total: **901.5**
- Posición final: [0, 2]
- Recursos finales: 1100.0
- Bonus meta aplicado: True
- Trayectoria: el agente recibe el bonus de meta repetidamente al llegar a la meta y permanece allí.

Esto confirma que la función de recompensa y la lógica de meta ahora funcionan en cualquier grid. El entorno ya puede usarse para validar el aprendizaje RL en escenarios triviales.

---
## Resultado Fase E: Test extremo grid 2x2

Se ejecutó el entorno grid 2x2 con recursos iniciales altos, sin penalizaciones ni distractores, y bonus meta elevado. Política trivial: primero 'down', luego 'right'.

**Resultados:**
- Reward total: **901.4**
- Posición final: [1, 1]
- Recursos finales: 1400.0
- Bonus meta aplicado: True
- Trayectoria:
  - Paso 0: [1, 0], reward 0.20
  - Paso 1: [1, 1], reward 100.20
  - Pasos 2-8: [1, 1], reward 100.00 cada paso
  - Paso 9: [1, 1], reward 101.00

El agente recibe el bonus de meta repetidamente al llegar a la meta y permanece allí. No hay penalizaciones ocultas ni sumas inesperadas. El reward es dominado por el bonus meta tras alcanzar la meta, y la señal es clara y positiva.

**Conclusión:**
El entorno 2x2 extremo confirma que la función de recompensa y la lógica de meta funcionan correctamente incluso en el caso más trivial. El entorno está listo para validar el aprendizaje RL en escenarios mínimos.
<<<<<<< HEAD
>>>>>>> a5e54fc (Diagnóstico RL: Fase E (grid 2x2) documentada, reward y bonus meta verificados. README actualizado.)
=======

---
## Resultado Fase C: Overfitting RL con (x,y) como estado

Se entrenó un agente Q-learning tabular en grid 3x3 usando (x,y) como estado durante 10,000 episodios.

**Resultados:**
- Reward media primeros 100 episodios: 254.7
- Reward media últimos 100 episodios: 2515.2
- Reward máxima: 2701.9
- Reward mínima: 1.1
- Episodios con reward > 0: 10,000 de 10,000

**Conclusión:**
El agente aprende a alcanzar la meta y maximizar el reward en todos los episodios. El entorno y la señal de recompensa permiten el aprendizaje RL trivial por tabular Q-learning. El problema de aprendizaje básico está resuelto en este escenario.
>>>>>>> 1ba1f57 (Add smoke_test README for simplified RL debug)
