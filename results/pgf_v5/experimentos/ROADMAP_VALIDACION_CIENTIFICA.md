# 🎯 Roadmap de Validación Científica - TUI v4.2

**Autor:** Jose M Rivera Garcia  
**Fecha:** 2 de diciembre de 2025  
**Fuente:** Análisis crítico con IA revisora (peer review simulado)

---

## 🚨 TESIS CENTRAL

**Tu hallazgo del "valle 4x4" puede ser:**
1. ✅ Una ley científica nueva (Density-Risk Law) → Nature paper
2. ❌ Un artefacto de 3 puntos con overfitting → Paper regional

**La diferencia:** Hacer Experimento 2 CORRECTAMENTE.

---

## 📊 Estado Actual: ¿Dónde Estás?

### **Lo que TIENES:**
```
✅ Hallazgo reproducible (32.41% ± 1.77% en 3 seeds)
✅ Hipótesis plausible (densidad modula alineación)
✅ Respaldo teórico interdisciplinario (Optimal Foraging)
✅ Predicción testeable (manipular spawn_rate)
```

### **Lo que te FALTA (CRÍTICO):**
```
❌ Solo 3 puntos de datos (3x3, 4x4, 5x5)
❌ D_efectiva no definido operacionalmente
❌ No hay comparación formal de modelos
❌ No hay análisis de incertidumbre (IC95%)
❌ No está preregistrado (vulnerable a p-hacking)
```

### **Calificación Científica:**
```
Actual:    ⭐⭐⭐ (3/5) - "Hallazgo interesante + hipótesis"
Potencial: ⭐⭐⭐⭐⭐ (5/5) - "Ley cuantitativa validada"

Gap: 1-2 semanas de trabajo riguroso
```

---

## 🛣️ Roadmap Ejecutable (Fase por Fase)

### **Semana 1: Diseño y Ejecución**

#### **Día 1-2: Diseño Experimental Riguroso**

**Objetivo:** Definir protocolo ANTES de ver los datos (evitar p-hacking)

```python
# 1. Definir D_efectiva operacionalmente
def compute_D_effective(grid_size, spawn_rate, episodes_data):
    """
    D_efectiva = (spawn_rate × N² × p_acceso) / τ_consumo
    
    Donde:
    - spawn_rate: tasa de aparición de recursos
    - N: grid_size
    - p_acceso: fracción de celdas alcanzables sin morir
    - τ_consumo: pasos promedio para consumir un recurso
    """
    N = grid_size
    rho = spawn_rate
    
    # Calcular p_acceso empíricamente
    safe_cells = count_reachable_cells_without_dying(episodes_data)
    p_acceso = safe_cells / (N**2)
    
    # Calcular τ_consumo empíricamente
    tau_consumo = np.mean([
        ep['steps_between_resources'] 
        for ep in episodes_data
    ])
    
    D_eff = (rho * N**2 * p_acceso) / tau_consumo
    return D_eff

# 2. Preregistrar en OSF
preregister_osf({
    'hypothesis': 'ratio_pgf/control ∝ 1/D_effective',
    'predictions': {
        'config_A (spawn=0.2)': '60-70%',
        'config_B (spawn=0.5)': '32% (baseline)',
        'config_C (spawn=0.8)': '20-25%',
    },
    'success_criteria': {
        'R²': '> 0.75',
        'correlation': 'r(D, ratio) < -0.8',
        'p_value': '< 0.05',
        'effect_size': 'ratio_A > 1.5 × ratio_C',
    }
})

# 3. Diseñar configuraciones (mínimo 10 puntos)
configs = [
    # Variar densidad en grid fijo (5 puntos)
    {'grid': 4, 'spawn_rate': 0.2,  'name': '4x4_d0.2'},
    {'grid': 4, 'spawn_rate': 0.35, 'name': '4x4_d0.35'},
    {'grid': 4, 'spawn_rate': 0.5,  'name': '4x4_d0.5'},   # baseline
    {'grid': 4, 'spawn_rate': 0.65, 'name': '4x4_d0.65'},
    {'grid': 4, 'spawn_rate': 0.8,  'name': '4x4_d0.8'},
    
    # Variar grid con densidad fija (5 puntos)
    {'grid': 3, 'spawn_rate': 0.5, 'name': '3x3_d0.5'},
    {'grid': 4, 'spawn_rate': 0.5, 'name': '4x4_d0.5'},   # duplicado
    {'grid': 5, 'spawn_rate': 0.5, 'name': '5x5_d0.5'},
    {'grid': 6, 'spawn_rate': 0.5, 'name': '6x6_d0.5'},
    {'grid': 7, 'spawn_rate': 0.5, 'name': '7x7_d0.5'},
]

# Cada config × 3 seeds = 30 runs totales (manejable en 2-3 días)
```

---

#### **Día 3-5: Ejecución Experimental**

```bash
# Implementar spawn_rate en environment.py (si no existe)
# Ver: results/pgf_v5/experimentos/PLAN_EXPERIMENTO_2.md

# Ejecutar batch completo
for config in configs:
    for seed in [42, 123, 456]:
        python sim/prototipo_rl_simbiosis.py \
            --episodes 500 \
            --seed $seed \
            --grid_size ${config.grid} \
            --spawn_rate ${config.spawn_rate} \
            --risk_scale 1.5 \
            --pgf_mix 0.2 \
            --output_prefix results/pgf_v5/resultados/${config.name}_seed${seed}
```

**Tiempo estimado:** 2-3 días (10 configs × 3 seeds × 500 episodes × 2 agentes)

---

#### **Día 6-7: Análisis Preliminar**

```python
# 1. Calcular D_efectiva para cada configuración
results = []
for config in configs:
    episodes_data = load_episodes(config)
    D_eff = compute_D_effective(config.grid, config.spawn_rate, episodes_data)
    ratio = compute_pgf_control_ratio(episodes_data)
    results.append({
        'config': config.name,
        'D_effective': D_eff,
        'ratio': ratio,
        'grid': config.grid,
        'spawn_rate': config.spawn_rate,
    })

# 2. Verificar predicción cualitativa
print("Predicción: ratio debería BAJAR cuando D sube")
print(f"Correlación: r = {np.corrcoef(D_eff, ratio)[0,1]:.3f}")
# Esperado: r < -0.8

# 3. Visualización rápida
plt.scatter(D_eff, ratio)
plt.xlabel('D_efectiva')
plt.ylabel('Ratio PGF/Control')
plt.title('Predicción TUI v4.2: ratio ∝ 1/D')
plt.savefig('results/pgf_v5/figuras/density_vs_ratio_preliminary.png')
```

**Checkpoint:** Si correlación r > -0.5 → ⚠️ Hipótesis en problemas, revisar antes de continuar.

---

### **Semana 2: Análisis Completo y Escritura**

#### **Día 8-10: Análisis Estadístico Riguroso**

```python
# 1. Ajustar modelos competidores
from scipy.optimize import curve_fit

# Modelo v4.1: ratio no depende de D
def model_v4_1(x, a):
    return a * np.ones_like(x)

# Modelo v4.2: ratio ∝ 1/D
def model_v4_2(D, kappa, D0):
    return kappa / (D + D0)

# Modelo v4.2b: ratio ∝ 1/log(D)
def model_v4_2b(D, kappa, D0):
    return kappa / np.log(D + D0)

# Ajustar con bootstrap para IC95%
from sklearn.utils import resample

bootstrap_params = []
for _ in range(10000):
    sample = resample(results)
    D_sample = [r['D_effective'] for r in sample]
    ratio_sample = [r['ratio'] for r in sample]
    
    params, _ = curve_fit(model_v4_2, D_sample, ratio_sample)
    bootstrap_params.append(params)

kappa_mean = np.mean([p[0] for p in bootstrap_params])
kappa_ci = np.percentile([p[0] for p in bootstrap_params], [2.5, 97.5])

print(f"κ = {kappa_mean:.3f} [{kappa_ci[0]:.3f}, {kappa_ci[1]:.3f}]")

# 2. Comparación de modelos con AIC/BIC
def compute_aic(residuals, n_params):
    n = len(residuals)
    rss = np.sum(residuals**2)
    aic = n * np.log(rss/n) + 2 * n_params
    return aic

models = {
    'v4.1 (constante)': (model_v4_1, 1),
    'v4.2 (1/D)': (model_v4_2, 2),
    'v4.2b (1/log D)': (model_v4_2b, 2),
}

for name, (model, n_params) in models.items():
    params, _ = curve_fit(model, D_eff, ratio)
    predictions = model(D_eff, *params)
    residuals = ratio - predictions
    aic = compute_aic(residuals, n_params)
    r2 = 1 - np.sum(residuals**2) / np.sum((ratio - np.mean(ratio))**2)
    print(f"{name}: AIC = {aic:.1f}, R² = {r2:.3f}")

# Criterio: Δ AIC > 4 → Mejora sustancial
```

---

#### **Día 11-12: Generación de Figuras**

```python
# Figura 1: Scatter + fit
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(D_eff, ratio, s=100, alpha=0.6, label='Datos experimentales')

# Plot del fit con IC95%
D_range = np.linspace(min(D_eff), max(D_eff), 100)
predictions = model_v4_2(D_range, kappa_mean, D0_mean)
ax.plot(D_range, predictions, 'r-', lw=2, label='TUI v4.2: ratio ∝ 1/D')

# Sombrear IC95%
predictions_lower = model_v4_2(D_range, kappa_ci[0], D0_ci[0])
predictions_upper = model_v4_2(D_range, kappa_ci[1], D0_ci[1])
ax.fill_between(D_range, predictions_lower, predictions_upper, alpha=0.2, color='red')

ax.set_xlabel('Densidad Efectiva de Recursos (D)', fontsize=14)
ax.set_ylabel('Ratio PGF/Control', fontsize=14)
ax.set_title('Ley de Densidad-Riesgo: Validación Experimental', fontsize=16)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('results/pgf_v5/figuras/density_law_validated.png', dpi=300)

# Figura 2: Residuales para diagnóstico
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(predictions, residuals)
ax.axhline(0, color='red', linestyle='--')
ax.set_xlabel('Predicciones', fontsize=14)
ax.set_ylabel('Residuales', fontsize=14)
ax.set_title('Diagnóstico: Residuales vs Predicciones', fontsize=16)
plt.savefig('results/pgf_v5/figuras/residuals_diagnostic.png', dpi=300)

# Figura 3: Comparación de modelos (AIC)
fig, ax = plt.subplots(figsize=(8, 6))
model_names = list(models.keys())
aics = [compute_aic(...) for model in models.values()]
ax.bar(model_names, aics)
ax.set_ylabel('AIC (menor = mejor)', fontsize=14)
ax.set_title('Comparación de Modelos', fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('results/pgf_v5/figuras/model_comparison.png', dpi=300)
```

---

#### **Día 13-14: Escritura del Reporte**

**Estructura sugerida:**

```markdown
# Experimento 2: Validación de la Ley de Densidad-Riesgo

## Resumen Ejecutivo
[100 palabras: Hipótesis, método, resultado, conclusión]

## Hipótesis Preregistrada
- H0: ratio es independiente de D_efectiva
- H1: ratio ∝ 1/(D + D0)
- Predicción: r(D, ratio) < -0.8, R² > 0.75

## Método
### Diseño Experimental
[10 configuraciones, 3 seeds, protocolo]

### Definición Operacional de D
[Ecuación con justificación]

### Análisis Estadístico
[Bootstrap IC95%, AIC/BIC, comparación de modelos]

## Resultados
### Hallazgo Principal
"La relación inversa predicha entre densidad y ratio fue confirmada
 (r = -0.XX, p < 0.001, R² = 0.XX)"

### Parámetros Estimados
κ = XX.X [IC95%: XX.X, XX.X]
D0 = XX.X [IC95%: XX.X, XX.X]

### Comparación de Modelos
AIC_v4.1 = XX.X
AIC_v4.2 = XX.X (ΔAIC = -X.X, mejora sustancial)

## Interpretación
[Conectar con Optimal Foraging Theory, AI Safety]

## Limitaciones
[Listar honestamente: n todavía pequeño, generalización, etc.]

## Conclusión
[Si confirma: "TUI v4.2 validada" / Si refuta: "Hipótesis descartada"]
```

---

## ✅ Checklist de Validación Pre-Publicación

**Antes de enviar a venue:**

### **Rigor Metodológico:**
- [ ] Protocolo preregistrado (OSF o equivalente)
- [ ] D_efectiva definido operacionalmente (antes de experimentos)
- [ ] n≥10 configuraciones diferentes
- [ ] Múltiples seeds por configuración (≥3)
- [ ] Análisis de sensibilidad (¿qué pasa si D se calcula diferente?)

### **Rigor Estadístico:**
- [ ] IC95% reportado para todos los parámetros
- [ ] Comparación formal de modelos (AIC/BIC)
- [ ] p-valores corregidos si múltiples comparaciones
- [ ] Diagnóstico de residuales (normalidad, homocedasticidad)
- [ ] Bootstrap con n≥1000 para estabilidad

### **Rigor Científico:**
- [ ] Predicción cuantitativa a priori (no solo "ratio baja")
- [ ] Hipótesis nula explícita
- [ ] Criterios de éxito definidos antes de ver datos
- [ ] Limitaciones discutidas honestamente
- [ ] Data y código disponibles (GitHub + Zenodo)

### **Rigor en Escritura:**
- [ ] Abstract menciona Optimal Foraging Theory
- [ ] Introducción conecta con AI Safety
- [ ] Método es reproducible (todos los parámetros reportados)
- [ ] Figuras tienen DPI≥300 y labels legibles
- [ ] Referencias completas (Charnov 1976, MacArthur & Pianka 1966)

---

## 🎯 Criterios de Decisión Post-Experimento

### **Escenario A: Confirmación Fuerte** ✅
```
Resultados:
- R² > 0.75
- r(D, ratio) < -0.8, p < 0.001
- AIC_v4.2 < AIC_v4.1 - 4
- ratio_A > 1.5 × ratio_C

Acción:
→ Paper "Resource Density Law for AI Alignment"
→ Venues: Nature Machine Intelligence, Science Robotics
→ Claim: "New quantitative law discovered"
```

---

### **Escenario B: Confirmación Parcial** ⚠️
```
Resultados:
- R² = 0.5-0.75 (moderado)
- r(D, ratio) < -0.6 (tendencia clara pero no fuerte)
- AIC_v4.2 < AIC_v4.1 - 2 (mejora modesta)

Acción:
→ Paper "Density Effects in AI Alignment: Preliminary Evidence"
→ Venues: NeurIPS, ICLR, ICML
→ Claim: "Suggestive evidence, requires further validation"
```

---

### **Escenario C: Refutación** ❌
```
Resultados:
- R² < 0.5
- r(D, ratio) > -0.4 (correlación débil)
- AIC_v4.2 ≥ AIC_v4.1 (no mejora)

Acción:
→ Paper "The Grid 4×4 Valley Mystery: An Unexplained Phenomenon"
→ Venues: NeurIPS (negative results track), workshops
→ Claim: "We rule out density hypothesis, seek alternative explanations"

Importante: Los negative results también son valiosos si son rigurosos
```

---

## 🚀 El Mensaje Final

### **Lo que esta IA revisora te dijo (y tiene razón):**

> "HAZ EL EXPERIMENTO DE DENSIDAD HOY MISMO.  
> Es la diferencia entre:  
> 'Tengo un resultado raro y una idea' (paper regional)  
> vs  
> 'Tengo una ley cuantitativa validada' (top-tier venue)"

### **ROI del esfuerzo:**
```
Inversión:  1-2 semanas de trabajo
Retorno:    Posible Nature/Science paper
Riesgo:     BAJO (ganas incluso si refuta)
```

### **Tu próximo paso:**
```bash
# Paso 1: Implementar spawn_rate en environment.py (2-4 horas)
# Paso 2: Ejecutar configuraciones (2-3 días)
# Paso 3: Análisis riguroso (3-4 días)
# Paso 4: Escritura (2-3 días)

Total: 7-10 días de calendario
```

---

**La ciencia no es solo tener una idea brillante.**  
**Es validarla con el rigor que resista el escrutinio más duro.**

✨ **¿Listo para convertir tu hallazgo en una ley científica?** ✨
