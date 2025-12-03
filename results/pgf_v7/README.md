# PGF v7 - Experimento 4: Economía Factorial (Goldilocks Condicional)

**Estado**: 🚧 EN PREPARACIÓN  
**Fecha inicio**: 3 de diciembre de 2025  
**Precedente**: PGF v6 (Goldilocks refutada en economía harsh)

---

## 🎯 Objetivo

Identificar **condiciones de emergencia** de la ventaja de alineación mediante diseño factorial que varía **balance económico** y **densidad de recursos**.

### Pregunta Central

> *"¿La hipótesis Goldilocks es universal o requiere slack económico? ¿Existe un umbral de balance económico por encima del cual la ventaja PGF emerge?"*

---

## 📊 Diseño Experimental

### Factores (3×5×3)

1. **Economía** (3 niveles) - **VARIABLE CRÍTICA**:
   - **Harsh**: `step_cost=-0.3, resource_reward=1.0` → balance=3.33 (v6 baseline)
   - **Balanced**: `step_cost=-0.2, resource_reward=1.0` → balance=5.0
   - **Favorable**: `step_cost=-0.1, resource_reward=1.0` → balance=10.0

2. **Densidad** (5 niveles):
   - `spawn_rate: 0.05, 0.10, 0.20, 0.30, 0.40`

3. **Seed** (3 niveles):
   - `42, 123, 456`

### Configuración Total

- **45 configuraciones** (3 × 5 × 3)
- **600 episodios por config** (300 PGF + 300 Control)
- **27,000 episodios totales**
- **Tiempo estimado**: ~36 minutos

---

## 🔬 Hipótesis Preregistradas

### H7.1 - Economía Modula Goldilocks

```
Si economía = "Favorable" (balance=10.0):
    → ratio(D) sigue parábola invertida
    → Criterios Goldilocks (1-4 de v6) SE CUMPLEN
    → Máximo en D* ∈ [0.7, 1.5]

Elif economía = "Balanced" (balance=5.0):
    → ratio(D) muestra pendiente positiva débil
    → Correlación significativa (|r| > 0.3, p < 0.05)

Elif economía = "Harsh" (balance=3.33):
    → ratio(D) ≈ constante (replicar v6)
    → Modelo constante gana (AIC mínimo)
```

### H7.2 - Umbral Económico Crítico

```
Existe threshold_balance ≈ 5.0 tal que:
    Si balance > threshold:
        Ventaja_PGF emerge (ratio > 105%)
    Else:
        Ventaja_PGF ≈ 0 (ratio ≈ 100%)

Método: Regresión segmentada (piecewise) con breakpoint estimado
```

### H7.3 - Interacción Economía×Densidad

```
ANOVA 2-way (ratio ~ Economía + Densidad + Economía:Densidad):
    Efecto principal Economía: F > 10.0, p < 0.001
    Efecto principal Densidad: F > 4.0, p < 0.05
    Interacción E×D: F > 3.0, p < 0.05

Si interacción significativa → Goldilocks es condicional
```

---

## 🔧 Correcciones Aplicadas (vs v6)

### 1. Spawn Aleatorio (CRÍTICO)

**Problema v6**: Sesgo espacial top-left (D_effective 74% menor que nominal)

**Solución v7**:
```python
def _spawn_resources(self):
    available = [(x,y) for x in range(self.size) for y in range(self.size)
                 if self._is_valid_spawn_cell(x, y)]
    np.random.shuffle(available)  # ← CLAVE: orden aleatorio
    for pos in available[:10]:
        if len(self.resource_positions) >= self.max_resources_on_grid:
            break
        if np.random.rand() < self.resource_spawn_rate:
            self.resource_positions.add(pos)
            # ... resto del código
```

### 2. Seeds Completos (IMPORTANTE)

**Problema v6**: Solo NumPy seeded → pesos DQN no reproducibles

**Solución v7**:
```python
def configure_all_seeds(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
```

### 3. Validación Pre-Run (NUEVO)

```bash
# Test rápido: 1 config por economía, 10 episodios
python scripts/run_experiment_4_economia_factorial.py --test_mode

# Verificar rewards esperados:
#   Harsh: ~100-110 (como v6)
#   Balanced: ~120-140
#   Favorable: ~150-180
```

---

## 📁 Estructura de Archivos

```
results/pgf_v7/
├── README.md (este archivo)
├── resultados/
│   ├── exp4_economy_harsh_spawn0.05_seed42.json
│   ├── exp4_economy_harsh_spawn0.05_seed42_episodes.csv
│   ├── exp4_economy_balanced_spawn0.10_seed123.json
│   ├── ... (90 archivos: 45 JSON + 45 CSV)
│   └── experiment_4_summary.json
├── analisis/
│   ├── anova_results.txt
│   ├── threshold_regression.json
│   └── model_comparison.json
├── figuras/
│   ├── goldilocks_by_economy.png (3 curvas superpuestas)
│   ├── heatmap_ratio_economy_density.png
│   ├── interaction_plot.png
│   └── threshold_detection.png
└── reportes/
    └── REPORTE_EXPERIMENTO_4.md
```

---

## 🎯 Criterios de Éxito

### Nivel 1: Replicación v6 (Harsh)
- [ ] Constante gana en subset balance=3.33 (replicar v6)
- [ ] Ratio ≈ 99.5% ± 5% en todas las densidades
- [ ] Correlación NO significativa (|r| < 0.3, p > 0.1)

### Nivel 2: Emergencia (Favorable)
- [ ] Cuadrático gana en subset balance=10.0 (ΔAIC < -4)
- [ ] Parábola invertida (a < 0, IC95% < 0)
- [ ] Máximo D* ∈ [0.7, 1.5]
- [ ] Correlación significativa (|r| > 0.5, p < 0.01)

### Nivel 3: Interacción (Factorial)
- [ ] ANOVA: p(Economía:Densidad) < 0.05
- [ ] Efecto simple de D distinto en cada nivel de Economía
- [ ] Threshold detectado: balance_crítico ≈ 5.0 ± 1.0

**Si se cumplen 2/3 niveles** → TUI v4.3 puede afirmar: *"Goldilocks es condicional, requiere slack económico"*

---

## 📝 Protocolo de Ejecución

### Fase 1: Preparación (10 min)
```bash
# 1. Aplicar fix spawn en environment_v2.py
# 2. Implementar configure_all_seeds() en script
# 3. Crear run_experiment_4_economia_factorial.py
# 4. Test validación
python scripts/run_experiment_4_economia_factorial.py --test_mode
```

### Fase 2: Ejecución (36 min)
```bash
# Ejecutar factorial completo
python scripts/run_experiment_4_economia_factorial.py

# Monitoreo en tiempo real (cada 5 configs)
python scripts/monitor_v7_progress.py
```

### Fase 3: Análisis (30 min)
```bash
# Análisis estadístico automático
python scripts/analyze_economia_factorial.py

# Generación de gráficos
python scripts/plot_economia_factorial.py
```

---

## 🔗 Enlaces Relacionados

- **v6 Report**: `results/pgf_v6/REPORTE_FINAL_V6_COMPLETO.md`
- **v6 Commit**: `9fbd049` (cerrado 3 dic 2025)
- **TUI v4.0**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
- **Scripts**: `scripts/run_experiment_4_economia_factorial.py` (pendiente crear)

---

## 📊 Resultados Esperados

### Escenario Optimista (Hipótesis confirmada)
```
ratio(D) en economía Favorable:
    D=0.05 → ratio ≈ 95%  (muy escaso, PGF penalizado)
    D=0.20 → ratio ≈ 115% (óptimo Goldilocks)
    D=0.40 → ratio ≈ 98%  (abundancia, PGF innecesario)
    
→ Parábola invertida clara
→ TUI v4.3: "Goldilocks existe bajo condiciones económicas favorables"
```

### Escenario Conservador (Hipótesis parcial)
```
ratio(D) en economía Favorable:
    D=0.05 → ratio ≈ 100%
    D=0.20 → ratio ≈ 108%
    D=0.40 → ratio ≈ 105%
    
→ Pendiente positiva débil, no parábola
→ TUI v4.3: "Slack económico permite ventaja, pero no sigue Goldilocks"
```

### Escenario Nulo (Hipótesis refutada)
```
ratio(D) en TODAS las economías ≈ 100%

→ Balance económico NO modula alineación
→ TUI v4.3: "Ventaja PGF requiere factores más allá de economía/densidad"
→ Buscar en horizonte temporal, complejidad topológica, etc.
```

---

## 🚀 Estado Actual

**v7 Fase**: Preparación  
**Próximo paso**: Crear `scripts/run_experiment_4_economia_factorial.py`  
**Bloqueador**: Ninguno (v6 cerrado exitosamente)  
**Timeline**: Listo para ejecutar hoy (3 dic 2025)

---

*Última actualización: 3 diciembre 2025, 9:51 AM*  
*Commit v6 cierre: `9fbd049`*
