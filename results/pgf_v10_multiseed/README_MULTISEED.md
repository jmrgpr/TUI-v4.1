# Multi-Seed Validation - v10_viable Curriculum

**Objetivo**: Validar reproducibilidad del curriculum 4×4→6×6→8×8 bajo economía viable.

**Status**: 🔄 EN PROGRESO

---

## Diseño Experimental

### Seeds Oficiales
```python
SEEDS = [13, 42, 101, 2025, 9999]
```

- **seed=42**: Baseline v10_viable (ya ejecutado, symlink)
- **seeds restantes**: Nuevas ejecuciones con configuración idéntica

### Configuración (Idéntica a v10_viable)

**Economía**:
- `initial_resources`: 8.0
- `step_cost`: -0.15
- `resource_spawn_rate`: 0.40
- `goal_reward`: 20.0

**Hyperparameters**:
- `learning_rate`: 0.001
- `gamma`: 0.99
- `hidden_dim`: 128
- `epsilon_decay`: 0.995
- `batch_size`: 32
- `memory_size`: 10000

**Curriculum**:
- **Fase 1 (4×4)**: 500 eps, epsilon 1.0→0.1, max_steps 24, gate >80%
- **Fase 2 (6×6)**: 1000 eps, epsilon 0.9→0.1, max_steps 50, gate >20%
- **Fase 3 (8×8)**: 1000 eps, epsilon 0.3→0.1, max_steps 42, gate >10%

---

## Criterios de Éxito (Conservadores)

### Gates Aceptables (N=5)

| Fase | Grid | Media Esperada | Rango Aceptable | Criterio Fracaso |
|------|------|----------------|-----------------|------------------|
| 1 | 4×4 | 85% ± 10% | [75%, 95%] | <2 seeds >80% |
| 2 | 6×6 | 50% ± 20% | [30%, 70%] | ≥2 seeds <20% |
| 3 | 8×8 | 70% ± 15% | [55%, 85%] | <3 seeds >60% |

**Notas**:
- 6×6 tiene tolerancia alta (conocida sensibilidad)
- Si 2+ seeds fallan gate fase 2, se considera problema estructural
- Desviación estándar >30% en cualquier fase requiere investigación

---

## Estructura de Archivos

```
pgf_v10_multiseed/
├── README_MULTISEED.md          (este archivo)
├── PREREGISTRO_MULTISEED.md     (hipótesis antes de ejecutar)
├── seeds/
│   ├── seed_0013/
│   │   ├── phase1_4x4_TIMESTAMP.csv
│   │   ├── phase2_6x6_TIMESTAMP.csv
│   │   ├── phase3_8x8_TIMESTAMP.csv
│   │   ├── model_4x4_TIMESTAMP.pth
│   │   ├── model_6x6_TIMESTAMP.pth
│   │   ├── model_8x8_TIMESTAMP.pth
│   │   └── curriculum_summary_TIMESTAMP.csv
│   ├── seed_0042/               (SYMLINK → ../pgf_v10_viable/resultados/)
│   ├── seed_0101/
│   ├── seed_2025/
│   └── seed_9999/
├── analisis_agregado/
│   ├── multiseed_summary.csv    (todos los summaries concatenados)
│   └── multiseed_statistics.csv (media/std/min/max por fase)
├── figuras/
│   ├── boxplot_success_rates_5seeds.png
│   ├── phase2_breakthrough_histogram.png
│   └── transfer_effectiveness_comparison.png
└── REPORTE_MULTISEED.md         (resultados finales, interpretación)
```

---

## Ejecución

### Paso 1: Correr Multi-Seed
```bash
python scripts/run_multiseed_v10.py
```

**Duración estimada**: ~8-10 horas (2500 eps × 4 seeds nuevas)

### Paso 2: Análisis Agregado
```bash
python scripts/analisis_multiseed_v10.py
```

Genera:
- `multiseed_statistics.csv` (media/std por fase)
- Boxplots comparativos
- Distribución breakthrough 6×6

---

## Preguntas a Responder

1. **¿Es seed=42 representativa?**
   - Comparar success rates 42 vs media de otras 4
   - ¿42 está dentro de ±1σ?

2. **¿El breakthrough 6×6 es reproducible?**
   - Distribución episodio breakthrough en 5 seeds
   - ¿Siempre ocurre ~ep 500-700?

3. **¿Transfer 6×6→8×8 es robusto?**
   - ¿Todas las seeds tienen primer éxito <10 eps en 8×8?
   - ¿Convergencia 8×8 siempre más rápida que 6×6?

4. **¿Varianza 6×6 es problema estructural?**
   - ¿Todas las seeds oscilan 50-90% en últimos 500 eps?
   - ¿O algunas convergen establemente >80%?

---

## Contingencias

### Si Multi-Seed Falla (≥2 seeds <gate en fase 2 o 3):

**Opciones**:
1. **Ajuste fino hyperparameters**:
   - Aumentar epsilon_start 6×6 → 0.95
   - Aumentar max_steps 6×6 → 60
   - Reducir epsilon_decay → 0.993

2. **Redefinir gates**:
   - 6×6: gate >15% (más conservador)
   - Pero documentar honestamente limitación

3. **Fase intermedia 5×5**:
   - Suavizar transición 4×4→6×6
   - Curriculum: 4×4→5×5→6×6→8×8

### Si Multi-Seed Funciona:

**v10_viable queda validado como**:
- Baseline reproducible (N=5)
- Curriculum robusto para economía viable
- Listo para ablation study y PGF offline

---

## Estado Actual

- [ ] PREREGISTRO_MULTISEED.md creado
- [ ] Scripts runner/análisis implementados
- [ ] Seed 0013 ejecutada
- [ ] Seed 0101 ejecutada
- [ ] Seed 2025 ejecutada
- [ ] Seed 9999 ejecutada
- [ ] Análisis agregado completado
- [ ] REPORTE_MULTISEED.md generado

**Fecha inicio**: _pendiente_  
**Fecha fin**: _pendiente_

---

## Referencias

- **Baseline**: `results/pgf_v10_viable/`
- **Preregistro baseline**: commit `e099ab9`
- **Script runner**: `scripts/run_multiseed_v10.py`
- **Script análisis**: `scripts/analisis_multiseed_v10.py`
