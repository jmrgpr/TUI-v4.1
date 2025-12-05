# Preregistro Experimento 2: Manipulación de Densidad de Recursos

**Proyecto:** Teoría Unificada de la Inteligencia (TUI) v4.3 - Validación de Hipótesis de Densidad-Riesgo  
**Investigador Principal:** Jose M Rivera Garcia  
**Fecha de Preregistro:** 2 de diciembre de 2025  
**Timestamp Git:** `git log --oneline -1` (evidencia inmutable)  

---

## 🎯 Objetivo

Validar la **Hipótesis de Densidad-Riesgo (H-DR)** que propone que el costo de la alineación (prudencia) en sistemas de IA es inversamente proporcional a la densidad efectiva de recursos del entorno.

---

## 📊 Hipótesis

### **H0 (Hipótesis Nula):**
El ratio PGF/Control es **independiente** de la densidad efectiva de recursos ($D_{efectiva}$).

$$\text{ratio} = \text{constante}$$

### **H1 (Hipótesis Alternativa - H-DR):**
El ratio PGF/Control es **inversamente proporcional** a la densidad efectiva de recursos:

$$\text{ratio} = \frac{\kappa}{D_{efectiva} + D_0}$$

Donde:
- $\kappa$ = constante de proporcionalidad
- $D_0$ = término de estabilización (evita singularidad cuando $D \to 0$)

---

## 🔬 Definición Operacional de $D_{efectiva}$

**Fórmula:**

$$D_{efectiva} = \frac{\rho \cdot N^2 \cdot p_{acceso}}{\tau_{consumo}}$$

**Componentes (definidos A PRIORI):**

1. **$\rho$ (spawn_rate):**
   - Definición: Probabilidad de que aparezca un recurso por celda por paso
   - Medición: Parámetro experimental controlado
   - Valores: 0.2, 0.5, 0.8

2. **$N$ (grid_size):**
   - Definición: Tamaño del grid (NxN celdas)
   - Medición: Parámetro experimental fijo
   - Valor: 4 (para Experimento 2)

3. **$p_{acceso}$:**
   - Definición: Fracción de celdas alcanzables sin morir
   - Medición: Número de celdas únicas visitadas / Total de celdas
   - Protocolo: Registrar durante episodios, calcular al final

4. **$\tau_{consumo}$:**
   - Definición: Pasos promedio desde spawn de recurso hasta su recolección
   - Medición: Timestamp de spawn - timestamp de recolección, promediar
   - Protocolo: Registrar cada evento de recolección, calcular media

**Importante:** Esta definición NO será modificada post-hoc después de ver los datos.

---

## 🎲 Predicciones Cuantitativas (A Priori)

### **Predicción 1: Ordinal**
$$\text{ratio}_{0.2} > \text{ratio}_{0.5} > \text{ratio}_{0.8}$$

**Traducción:** A mayor densidad, menor ventaja de la prudencia (PGF).

### **Predicción 2: Cuantitativa**

| Config | spawn_rate | $D_{efectiva}$ (estimado) | ratio Predicho |
|--------|------------|---------------------------|----------------|
| A      | 0.2        | ~2.5                      | 60-70%         |
| B      | 0.5        | ~6.0                      | 30-40%         |
| C      | 0.8        | ~10.0                     | 15-25%         |

**Nota:** Estas estimaciones se basan en:
- PGF v4 baseline (grid 4x4, spawn_rate implícito ~0.5): ratio = 32%
- Extrapolación asumiendo $p_{acceso} \approx 0.6$, $\tau_{consumo} \approx 5$

### **Predicción 3: Efecto Grande**
$$\frac{\text{ratio}_{0.2}}{\text{ratio}_{0.8}} \geq 2.5$$

**Traducción:** El efecto debe ser sustancial, no marginal.

---

## ✅ Criterios de Éxito (Fijados A Priori)

### **Confirmación Fuerte (TUI v4.3 validado):**
```
✅ R² > 0.75              (ajuste robusto)
✅ r(D, ratio) < -0.8     (correlación fuerte)
✅ p < 0.05               (significancia estadística)
✅ ΔAIC (v4.3 vs v4.1) < -4  (mejora sustancial del modelo)
✅ ratio_max / ratio_min > 2.5  (efecto grande)
```

**Acción:** Publicar como TUI v4.3 en Nature Machine Intelligence / Science Robotics

---

### **Confirmación Moderada (evidencia parcial):**
```
⚠️ R² > 0.5
⚠️ r(D, ratio) < -0.6
⚠️ p < 0.05
⚠️ ΔAIC (v4.3 vs v4.1) < -2
```

**Acción:** Publicar en NeurIPS/ICLR con caveats ("evidencia preliminar, requiere validación adicional")

---

### **Refutación (H-DR no confirmada):**
```
❌ R² < 0.5
❌ r(D, ratio) > -0.4
❌ p > 0.05
❌ ΔAIC ≥ 0
```

**Acción:** Reportar negative result honestamente. Buscar explicación alternativa (topología, layout, etc.). Paper: "The Grid 4×4 Valley Mystery: Ruling Out Density Hypothesis"

---

## 🧪 Diseño Experimental

### **Variables Independientes:**
- **spawn_rate (ρ):** 0.2, 0.5, 0.8 (3 niveles)
- **seed:** 42, 123, 456 (3 réplicas)

### **Variables Dependientes:**
- **ratio_pgf_control:** (mean_reward_pgf / mean_reward_control) × 100
- **D_efectiva:** Calculada según fórmula preregistrada

### **Variables Controladas (Fijas):**
- grid_size: 4
- episodes: 500
- risk_scale: 1.5
- pgf_mix: 0.2
- resource_reward: 5.0
- max_resources_on_grid: 10

### **Total de Configuraciones:**
3 spawn_rates × 3 seeds = **9 runs**  
9 runs × 500 episodes = **4500 episodes totales**

---

## 📈 Plan de Análisis (Preregistrado)

### **Paso 1: Cálculo de D_efectiva**
Para cada configuración:
1. Cargar datos de episodios
2. Calcular $p_{acceso}$ = cells_visited / total_cells
3. Calcular $\tau_{consumo}$ = mean(collection_times)
4. Calcular $D_{efectiva}$ según fórmula

### **Paso 2: Análisis Descriptivo**
- Scatter plot: D_efectiva vs ratio
- Correlación de Pearson: r(D, ratio)
- Estadísticas por grupo (spawn_rate)

### **Paso 3: Ajuste de Modelos**
Comparar 3 modelos:

1. **Modelo v4.1 (nulo):** 
   $$\text{ratio} = a$$
   
2. **Modelo v4.3 (H-DR):**
   $$\text{ratio} = \frac{\kappa}{D + D_0}$$
   
3. **Modelo alternativo:**
   $$\text{ratio} = \frac{\kappa}{\log(D + D_0)}$$

### **Paso 4: Comparación de Modelos**
- Calcular AIC, BIC para cada modelo
- Reportar ΔAIC respecto a v4.1
- Seleccionar mejor modelo

### **Paso 5: Estimación de Parámetros**
- Bootstrap (n=10,000) para IC95% de $\kappa$ y $D_0$
- Reportar: $\kappa = X.XX$ [IC95%: X.XX, X.XX]

### **Paso 6: Diagnóstico**
- Residuales vs predicciones (homocedasticidad)
- QQ-plot (normalidad de residuales)

### **Paso 7: Decisión**
- Verificar criterios de éxito preregistrados
- Decidir: Confirmar, Parcial, o Refutar

---

## 🔒 Compromisos de Integridad Científica

**Me comprometo a:**

1. ✅ **NO modificar la definición de $D_{efectiva}$** después de ver los datos
2. ✅ **NO cambiar las predicciones** después de ejecutar el experimento
3. ✅ **NO ajustar los criterios de éxito** post-hoc
4. ✅ **Reportar TODOS los resultados**, incluso si refutan H-DR
5. ✅ **Publicar código y datos** en GitHub + Zenodo para reproducibilidad
6. ✅ **NO hacer p-hacking** (probar múltiples hipótesis sin corrección)
7. ✅ **NO cherry-pick** configuraciones que "funcionen mejor"

---

## 📚 Contexto Teórico

### **Motivación:**
El experimento PGF v4 reveló un "valle" inesperado en grid 4x4:
- Grid 3x3: ratio = 105% (PGF > Control)
- Grid 4x4: ratio = 32% (PGF << Control) ← Anomalía
- Grid 5x5: ratio = 39% (PGF < Control)

La TUI v4.1 original ($I \propto P_{riesgo}$) no explica por qué 4x4 < 5x5.

### **Hipótesis H-DR:**
El valle 4x4 se explica por **alta densidad efectiva de recursos**, no por complejidad espacial per se.

### **Conexión con Optimal Foraging Theory:**
En ecología evolutiva (Charnov 1976, MacArthur & Pianka 1966):
> "Cuando la densidad de presas aumenta, el depredador no necesita ser selectivo"

Aplicado a IA:
> "Cuando la densidad de recursos aumenta, la IA no necesita ser prudente (costoso) para sobrevivir"

---

## 🚀 Timeline Estimado

- **Día 1 (hoy):** Preregistro + implementación código
- **Día 2-4:** Ejecución de 9 configuraciones (batch automático)
- **Día 5:** Análisis estadístico + figuras
- **Día 6-7:** Escritura de reporte

**Total:** 7 días calendario

---

## 📝 Archivos Generados (Metadata Completa)

Cada run generará:

1. **JSON con metadata:**
   ```json
   {
     "experiment": "PGF_v5_Experimento_2_Densidad",
     "version": "v4.3_candidate",
     "config": {
       "grid_size": 4,
       "spawn_rate": 0.X,
       "seed": XX,
       "episodes": 500,
       ...
     },
     "results": {
       "ratio_pgf_control": XX.XX,
       "D_effective_mean": XX.XX,
       ...
     }
   }
   ```

2. **CSV con episodios:**
   - Columnas: episode, agent, total_reward, steps, resources_collected, D_effective, etc.

---

## ✍️ Firma Digital

**Investigador:** Jose M Rivera Garcia  
**Fecha:** 2 de diciembre de 2025  
**Commit Hash:** `[se completará al commitear este archivo]`  
**Repositorio:** https://github.com/jmrgpr/TUI-v4.1

---

**Este preregistro es INMUTABLE. Cualquier desviación será documentada y justificada explícitamente.**

---

## 📧 Contacto

Para preguntas sobre este preregistro o el experimento:
- GitHub Issues: https://github.com/jmrgpr/TUI-v4.1/issues
- Email: [pendiente]

---

**La ciencia rigurosa requiere transparencia total. Este documento es mi compromiso público con la integridad científica.**

✨ **Que gane la evidencia, no mis expectativas.** ✨
