# PREREGISTRO – Ablation por Componentes (Serie v10)

**Proyecto:** TUI-v4.1 – PGF / Gridworld RL  
**Serie:** v10 – Economía viable + curriculum  
**Fase:** 2 – Ablation por componentes (shaping, reward extra, curriculum, transfer, regularización)  
**Archivo:** `results/pgf_v10_ablation/PREREGISTRO_ABLATION_COMPONENTES_v10.md`  
**Fecha:** 2025-12-08  
**Autor:** José M. Rivera García

---

## 1. Contexto

Esta Fase 2 se apoya en:

- **v10_viable**: experimento curriculum 4×4 → 6×6 → 8×8 con seed 42, economía v10 estable, gates superados y documentados en `results/pgf_v10_viable/`.
- **Fase 1 – Multi-seed y Ablation núcleo v10 (A/B/C/D)**:  
  - Multi-seed sobre el pipeline curriculum original (robustez N>1).  
  - Ablation A/B/C/D centrada en **estructura de entrenamiento** (curriculum vs 8×8 directo, only 6×6, curriculum inverso).

En esta Fase 2 queremos aislar el efecto de **componentes específicos del sistema de recompensa y del agente**:

- Shaping basado en PGF (EvaluatorPGF / PGF_Bruto).
- Reward extra por recursos.
- Curriculum (4×4 → 6×6 → 8×8) como estructura de entrenamiento.
- Transfer learning (inicializar 8×8 desde un checkpoint).
- Regularización (L2 / dropout en el DQN).

La meta es cerrar la familia v10 con una **historia clara y honesta** de qué componentes ayudan, cuáles son neutros y cuáles complican o empeoran el aprendizaje.

---

## 2. Alcance de esta Fase

**Incluye:**

- Experimentos controlados ejecutados con  
  `scripts/run_ablation_componentes_v10.py`.
- Un **baseline Fase 2** bien definido (RL puro en 8×8) y variantes que añaden **exactamente un componente** cada una.
- 3 seeds por configuración (N=3) para tener señal estadística sin explotar el cómputo.

**No incluye (queda fuera de este preregistro):**

- Cambios en la arquitectura del agente más allá de activar/desactivar regularización básica (L2/dropout).
- Cambios en la economía (recursos, costos, spawn, goal_reward) respecto a la economía v10.
- Cambios de entorno (sólo se usa el grid de recursos/riesgos ya definido).
- Los sweeps TUI/PGF de `scripts/experimentos_previos/run_ablation_quick.py` (eso se documenta en un preregistro aparte para la Fase “PGF en el loop”).

---

## 3. Definición del Baseline Fase 2 (Control)

El **baseline experimental de Fase 2** debe ser coherente con la **Config B – Direct 8×8 RL puro** utilizada en Fase 1, pero formalizado dentro del runner de componentes.

### 3.1. Entorno y economía

- `environment_v2.ResourceDensityEnv`
- `grid_size = 8`
- Economía v10 (misma que en v10_viable / Fase 1):
  - `initial_resources = 8.0`
  - `step_cost = -0.15`
  - `resource_spawn_rate = 0.40`
  - `goal_reward = 20.0`
  - Mismo modelo de tripwires / shocks / distractores que en v10_viable.

### 3.2. Agente DQN (igual que en v10_viable)

Parámetros importados de `scripts/run_curriculum_complete_viable.py`:

- `LEARNING_RATE`
- `GAMMA`
- `EPSILON_START`
- `EPSILON_MIN`
- `EPSILON_DECAY`
- `BATCH_SIZE`
- `MEMORY_SIZE`
- `HIDDEN_DIM`

Sin modificaciones en esta Fase (no se hará tuning fino de estos valores aquí; eso queda para sweeps de hiperparámetros específicos).

### 3.3. Flags de componentes (baseline limpio)

El runner `run_ablation_componentes_v10.py` se define de modo que, para la variante `baseline` (y alias `minimal`), los flags internos sean:

- `shaping = False`  
  → **No** se añade PGF_Bruto al reward del environment.
- `reward_extra = False`  
  → **No** se añade bono extra de recursos al reward.
- `curriculum = False`  
  → Entrenamiento directo en 8×8 (sin 4×4 ni 6×6).
- `transfer = False`  
  → No se inicializan pesos desde checkpoints; el agente empieza desde cero.
- `regularization = False`  
  → Sin L2 (weight_decay = 0.0) y sin dropout (dropout = 0.0).

### 3.4. Episodios y gates

- `episodes = 1500` por experimento, siguiendo el ajuste validado en Fase 1 para 8×8 directo.
- Gate principal en 8×8:
  - `gate_8x8 = 0.10` → Al menos 10% de éxito en los últimos 100 episodios.
- Si un baseline no alcanza el gate en una seed aislada, se revisa en contexto de las 3 seeds (ver criterios en sección 6).

---

## 4. Componentes a ablar y variantes definidas

Sobre el baseline descrito (RL puro), se definen las siguientes **variantes** en el runner:

### 4.1. Lista de variantes

1. `baseline` (alias: `minimal`)
   - RL puro en 8×8.
   - Todos los flags en False: `shaping`, `reward_extra`, `curriculum`, `transfer`, `regularization`.

2. `with_shaping` (alias: `shaping`)
   - Igual que baseline, pero:
     - `shaping = True`
     - `reward_extra = False`
     - `curriculum = False`
     - `transfer = False`
     - `regularization = False`
   - Se activa `EvaluatorPGF` y se suma `PGF_Bruto` al reward del environment (con la escala y parámetros definidos en el script).

3. `with_rewardextra` (alias: `rewardextra`)
   - Igual que baseline, pero:
     - `reward_extra = True`
     - `shaping = False`
   - Se añade un bono por recolección de recursos (`shaping_resource_bonus`) cuando `info['resource_collected']`/`info['resource_value']` lo indiquen.

4. `with_curriculum` (alias: `curriculum`)
   - Mismo reward que baseline (sin shaping ni reward_extra).
   - Pero:
     - `curriculum = True`
   - El runner usa la lógica de curriculum: 4×4 → 6×6 → 8×8, con gates por fase coherentes con v10_viable. El análisis principal sigue siendo el desempeño final en 8×8.

5. `with_transfer` (alias: `transfer`)
   - Mismo reward que baseline, sin curriculum.
   - Pero:
     - `transfer = True`
     - Se pasa un `--transfer_checkpoint` apuntando a un `.pth` entrenado previamente (por ejemplo un buen modelo 6×6).
   - Evalúa el efecto de inicializar el agente con un policy pre-entrenado antes de 8×8.

6. `with_regularization` (alias: `regularization`)
   - Igual que baseline, pero:
     - `regularization = True`
     - `weight_decay` y `dropout` se activan con valores suaves (ej. `weight_decay = 1e-5`, `dropout = 0.10`).
   - Evalúa si la regularización estabiliza la política o reduce “crashes” después del breakthrough.

7. Variantes `hyper_*` (barridos de hiperparámetros)
   - `hyper_lr_*`, `hyper_gamma_*`, `hyper_batch_*`, etc., interpretadas por `parse_hyper_variant`.
   - Estas variantes usan el baseline como punto de partida y **solo** cambian el hiperparámetro indicado.

---

## 5. Diseño experimental

### 5.1. Seeds

Para esta Fase se usarán **3 seeds por variante**:

```
SEEDS = [42, 13, 101]
```

Justificación:
- 42: seed histórica del proyecto (v10_viable, Fase 1).
- 13 y 101: semillas adicionales para capturar variabilidad razonable sin disparar el costo computacional.

### 5.2. Configuraciones a ejecutar

Para cada variante principal:

- baseline
- with_shaping
- with_rewardextra
- with_curriculum
- with_transfer (solo si se dispone de checkpoint estable conocido)
- with_regularization

Se ejecutará:
```
python scripts/run_ablation_componentes_v10.py \
    --variant <variant> \
    --seed <seed>
```
Donde `<seed> ∈ {42, 13, 101}`.  
Los episodios por defecto se fijan en 1500; si se especifica `--episodes` se documentará explícitamente en el reporte.

### 5.3. Métricas por run

Para cada combinación (variant, seed) se almacenarán:

- `success_rate_total`
- `success_last_100`
- `first_success_episode`
- `convergence_episode`
- `mean_reward_last_100`
- `overhead_vs_manhattan` (si aplica)
- Log de eventos relevantes (tripwires/shocks/recursos) si está instrumentado.

### 5.4. Agregación

Para cada variante se computará, sobre las 3 seeds:

- Media y desviación estándar de:
  - `success_last_100`
  - `first_success_episode`
  - `convergence_episode`
  - `mean_reward_last_100`
- Rango (min, max) para visualizar varianza.
- Boxplots y/o barplots comparando baseline vs variantes.

---

## 6. Hipótesis y criterios de interpretación

### 6.1. Hipótesis por componente

**H0 (baseline):** RL puro en 8×8, 1500 episodios, gate 10% coherente con Config B/Fase 1.  
**H1 (shaping PGF):** `with_shaping` ≥ baseline en `success_last_100`, breakthrough más rápido.  
**H2 (reward extra):** Puede estabilizar o sesgar a recolección; observar `mean_reward_last_100` y patrones de overhead.  
**H3 (curriculum):** `with_curriculum` igual o superior a baseline y menor varianza entre seeds.  
**H4 (transfer):** `with_transfer` reduce `first_success_episode`; éxito final similar.  
**H5 (regularización):** L2+dropout suaves no degradan el success y podrían reducir oscilaciones.

### 6.2. Criterios de éxito/fracaso

Fase 2 se considera completada cuando:
- Hay comparativa (CSV + gráficas) baseline vs cada variante.
- Cada componente se clasifica como beneficioso, neutro o perjudicial.
- Se redacta un reporte en `results/pgf_v10_ablation/REPORTE_ABLATION_v10.md` (o sección equivalente) con tablas, figuras y discusión de limitaciones (N=3, sensibilidad a seeds, interacciones no cubiertas).

---

## 7. Compromisos metodológicos

- No cambiar a posteriori definiciones de baseline/variantes aquí descritas ni las seeds `[42, 13, 101]`.  
- Mantener 1500 episodios por experimento salvo fallo técnico grave (documentado y repetido).  
- Cualquier cambio en reward (PGF_Bruto, reward_extra), lógica de curriculum o carga de checkpoints se aplicará en código antes de nuevos runs y se documentará con fecha en este archivo o en uno nuevo.

---

## 8. Relación con v11 y resto de Serie v10

- No se tomarán decisiones de v11 hasta cerrar v10_viable, completar Fase 1 (multi-seed + ablation A/B/C/D) y esta Fase 2.  
- Los resultados de Fase 2 decidirán qué componentes (shaping, reward extra, curriculum, transfer, regularización) son candidatos por defecto en v11 o se dejan como optativos/descartados.

---

Fin del preregistro – Fase 2: Ablation por Componentes (v10).  
Este documento se considera “ley experimental” para todos los runs ejecutados con `scripts/run_ablation_componentes_v10.py` en la Serie v10.
