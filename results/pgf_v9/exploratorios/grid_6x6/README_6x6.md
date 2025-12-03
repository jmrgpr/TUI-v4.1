# 🔬 Exploratorio v9: Grid 6×6

**Grid Size**: 6×6 (36 celdas)  
**Objetivo**: Validar que curriculum learning generaliza a mayor complejidad espacial  
**Status**: 📋 CONDICIONAL (ejecutar si v9 4×4 éxito)  
**Fecha**: 3 diciembre 2025

---

## 🎯 Justificación

### Contexto v8 Exploratorio

**Hallazgo previo** (v8 exploratorio 6×6):
- Patrón cualitativo **idéntico** a 4×4
- s=0.0 → paridad (~0.99)
- s=1.0 → over-alignment (~0.30-0.40)

**Limitación**: v8 exploratorio se ejecutó con código **pre-fixes v8.0.1** (death flags incompletos)

### Pregunta Exploratoria

> ¿Curriculum learning mantiene efectividad en grid 6×6 con código v8.0.1+ (death flags robustos)?

---

## 📐 Complejidad 6×6 vs 4×4

| Aspecto | 4×4 | 6×6 | Factor |
|---------|-----|-----|--------|
| **Celdas** | 16 | 36 | 2.25× |
| **Manhattan dist** | 6 steps | 10 steps | 1.67× |
| **Caminos posibles** | ~20 | ~252 | 12.6× |
| **Tripwires (spawn=0.25)** | ~4 | ~9 | 2.25× |
| **Recursos (spawn=0.25)** | ~4 | ~9 | 2.25× |
| **Tiempo/episodio** | ~0.5s | ~1.0s | 2× |

**Implicación**: Complejidad espacial ~12× mayor, pero aún manejable para DQN 2×64.

---

## 🔬 Diseño Experimental

### Configuración

```python
GRID_SIZE = 6
SPAWN_RATE = 0.25  # ~9 tripwires, ~9 recursos
BALANCE = 5.0      # Balanced economy
EPISODES_PER_CONFIG = 300

# Grupos (idénticos v9 4×4)
grupos = ["Curriculum", "DirectoS1", "ControlS0"]
seeds = [42, 123, 456]

# Curriculum (mismo protocolo 4×4)
etapas_curriculum = [
    {"scale": 0.0,  "episodes": range(0, 75)},
    {"scale": 0.25, "episodes": range(75, 150)},
    {"scale": 0.5,  "episodes": range(150, 225)},
    {"scale": 1.0,  "episodes": range(225, 300)}
]
```

**Total**: 3 grupos × 3 seeds = 9 configs, 2,700 episodios

**Tiempo estimado**: ~20 minutos

---

## 📊 Hipótesis Exploratorias

### H_6x6_1: Generalización de Efectividad

> En 6×6, Curriculum alcanzará ratio_final significativamente mayor que DirectoS1, con magnitud ≥ que en 4×4.

**Predicción**:
```
Δ_4x4 = ratio_curriculum - ratio_directo ≈ 0.40 (esperado)
Δ_6x6 ≥ Δ_4x4

Interpretación: Ventaja se mantiene o amplifica
```

### H_6x6_2: Replicación Patrón Temporal

> Degradación gradual (NO súbita) se replica en 6×6.

**Predicción**:
```
Ratios por etapa (6×6):
  Etapa 1 (s=0.0):  ~0.98
  Etapa 2 (s=0.25): ~0.80-0.85
  Etapa 3 (s=0.5):  ~0.70-0.75
  Etapa 4 (s=1.0):  ~0.65-0.70
```

### H_6x6_3: Prudencia Mantenida

> Curriculum reducirá tripwires ≥20% vs ControlS0 en 6×6.

---

## 📁 Outputs

### Archivos Generados

```
grid_6x6/
├── resultados/
│   ├── exp9_6x6_Curriculum_seed42_episodes.csv
│   ├── exp9_6x6_Curriculum_seed42_metrics.json
│   ├── exp9_6x6_DirectoS1_seed42_episodes.csv
│   ├── exp9_6x6_DirectoS1_seed42_metrics.json
│   ├── exp9_6x6_ControlS0_seed42_episodes.csv
│   ├── exp9_6x6_ControlS0_seed42_metrics.json
│   └── ... (18 archivos total: 9 CSVs + 9 JSONs)
├── analisis/
│   ├── curriculum_effectiveness_6x6.json
│   └── comparison_4x4_vs_6x6.json
└── figuras/
    ├── fig1_learning_curves_6x6.png
    ├── fig2_barplot_ratios_6x6.png
    └── fig3_comparison_4x4_vs_6x6.png
```

### Análisis Comparativo 4×4 vs 6×6

**Archivo**: `comparison_4x4_vs_6x6.json`

**Métricas**:
```json
{
  "ratio_curriculum": {
    "4x4": [TBD],
    "6x6": [TBD],
    "delta": [TBD],
    "interpretation": "¿Se mantiene o amplifica?"
  },
  "ventaja_sobre_directo": {
    "4x4": [TBD],
    "6x6": [TBD],
    "effect_size_4x4": [TBD],
    "effect_size_6x6": [TBD]
  },
  "transfer_efficiency": {
    "4x4": [TBD],
    "6x6": [TBD],
    "interpretation": "¿Retención empeora con complejidad?"
  }
}
```

---

## 🎯 Criterios de Éxito

### Escenario 1: Generalización Exitosa ✅

```
6x6 Curriculum:  ratio_final ≥ 0.70, ventaja ≥ 0.40 sobre DirectoS1
4x4 Curriculum:  ratio_final ≥ 0.70, ventaja ≥ 0.40 sobre DirectoS1

Conclusión: Curriculum ROBUSTO a complejidad espacial
```

### Escenario 2: Amplificación 🟢

```
6x6 ventaja > 4x4 ventaja (ej: 0.50 vs 0.40)

Conclusión: Curriculum MÁS efectivo en entornos complejos
Mecanismo: Directo s=1.0 colapsa más en 6×6, curriculum adapta mejor
```

### Escenario 3: Degradación Parcial ⚠️

```
6x6 Curriculum: ratio_final ≈ 0.55 (vs 0.75 en 4×4)
Ventaja mantiene pero reduce: 0.25 (vs 0.40 en 4×4)

Conclusión: Curriculum ayuda pero MENOS efectivo en mayor complejidad
Posible causa: DQN 2×64 alcanza límite capacidad
```

### Escenario 4: Falla Completa ❌

```
6x6 Curriculum ≈ DirectoS1 (ambos ~0.35)

Conclusión: Curriculum NO generaliza a 6×6
Diagnóstico: Problema arquitectural (red pequeña) o duración etapas insuficiente
```

---

## 📊 Visualizaciones

### Figura 1: Learning Curves 6×6

**Tipo**: Line plot (episodios × ratio)  
**Líneas**: Curriculum, DirectoS1, ControlS0  
**Comparación**: Panel lado-a-lado con 4×4

### Figura 2: Barplot Comparativo

**Tipo**: Barplot grouped  
**X**: Grid size (4×4, 6×6)  
**Y**: Ratio final  
**Grupos**: Curriculum, DirectoS1, ControlS0

### Figura 3: Scatter Safety-Reward 6×6

**Tipo**: Scatter 2D  
**X**: Safety score  
**Y**: Reward env  
**Puntos**: Por grupo (etapa final 250-300)

---

## 🔗 Valor para Paper

**Si generaliza exitosamente**:

> "Curriculum learning efectiveness persists in spatially complex environments (6×6 grid, 12× more paths than 4×4). Effect size maintained or amplified (d_4x4=1.5, d_6x6=1.7), demonstrating robustness of staged alignment approach."

**Sección Methods**:

> "To validate spatial generalization, we replicated v9 protocol in 6×6 grids (36 cells, Manhattan distance 10 steps, ~9 tripwires). All other parameters held constant (spawn=0.25, balance=5.0, curriculum stages 0.0→0.25→0.5→1.0)."

---

## 📝 Notas de Implementación

### Adaptación Código

**Cambios mínimos** en `run_experiment_9_curriculum.py`:

```python
# Parámetro adicional
parser.add_argument('--grid_size', type=int, default=4, 
                    choices=[4, 6, 8],
                    help='Grid size (4x4, 6x6, or 8x8)')

# Ajustar entorno
env = ResourceDensityEnv(
    grid_size=args.grid_size,  # ← Único cambio crítico
    resource_spawn_rate=spawn_rate,
    balance=5.0,
    step_cost=-0.2,
    goal_reward=1.0
)

# Outputs etiquetados
csv_filename = f"exp9_{args.grid_size}x{args.grid_size}_{group}_seed{seed}_episodes.csv"
```

**Validación**:
- Verificar que tripwires generados ≈ 9 (36 × 0.25)
- Verificar que camino óptimo libre ≈ 13% (1-0.25)^10

---

**FIN README 6×6**

**Status**: 📋 CONDICIONAL (post v9 4×4)  
**Prioridad**: ALTA (si tiempo permite)  
**Tiempo**: ~20 minutos
