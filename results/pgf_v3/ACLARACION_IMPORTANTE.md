# ⚠️ ACLARACIÓN IMPORTANTE - Nomenclatura de Agentes
# ⚠️ IMPORTANT CLARIFICATION - Agent Nomenclature

**Fecha / Date:** 2 de diciembre de 2025

---

## Español

### ¿Qué agentes hay en los experimentos PGF v3?

En TODOS los experimentos de PGF v3 (seeds 42, 123, 456) hay **exactamente 2 agentes**:

1. **`control`** - Agente baseline SIN PGF
2. **`simbiosis`** - Agente CON PGF v3 (implementa la teoría TUI)

### ⚠️ NO existe una etiqueta `'tui'` separada

**Importante:** En el código y en los archivos CSV, el agente que implementa la Teoría Unificada de Inteligencia (TUI) se llama **`simbiosis`**.

**NO hay** filas con el label `'tui'` en los datos.

### Equivalencias

```
simbiosis = TUI = Agente con PGF v3
```

Son **tres nombres para el mismo agente**:
- **Simbiosis:** Nombre técnico en el código
- **TUI:** Nombre conceptual (Teoría Unificada de Inteligencia)
- **Agente con PGF:** Descripción funcional

### ¿Por qué esta confusión?

En las visualizaciones y reportes, a veces usamos "TUI/Simbiosis" o "Simbiosis (TUI)" para conectar el nombre técnico del código con el concepto teórico. Esto puede crear la impresión de que son dos agentes distintos, **pero NO lo son**.

### Verificación en los datos

Si abres cualquier archivo CSV de experimentos (ejemplo: `exp3a_pgfv3_risk15_seed42_episodes.csv`), la columna `Agente` contiene solo dos valores únicos:
- `control`
- `simbiosis`

No hay ningún valor `tui`.

---

## English

### What agents are in the PGF v3 experiments?

In ALL PGF v3 experiments (seeds 42, 123, 456) there are **exactly 2 agents**:

1. **`control`** - Baseline agent WITHOUT PGF
2. **`simbiosis`** - Agent WITH PGF v3 (implements TUI theory)

### ⚠️ There is NO separate `'tui'` label

**Important:** In the code and CSV files, the agent implementing the Unified Intelligence Theory (TUI) is called **`simbiosis`**.

There are **NO** rows with the label `'tui'` in the data.

### Equivalences

```
simbiosis = TUI = Agent with PGF v3
```

These are **three names for the same agent**:
- **Simbiosis:** Technical name in the code
- **TUI:** Conceptual name (Unified Intelligence Theory)
- **Agent with PGF:** Functional description

### Why this confusion?

In visualizations and reports, we sometimes use "TUI/Simbiosis" or "Simbiosis (TUI)" to connect the technical code name with the theoretical concept. This can create the impression that they are two distinct agents, **but they are NOT**.

### Data verification

If you open any experiment CSV file (example: `exp3a_pgfv3_risk15_seed42_episodes.csv`), the `Agente` column contains only two unique values:
- `control`
- `simbiosis`

There is no `tui` value.

---

## Implicaciones para Análisis / Implications for Analysis

### Correcto / Correct ✅

```python
# Cargar datos de Simbiosis (que implementa TUI)
df_simbiosis = df[df['Agente'] == 'simbiosis']

# Cargar datos de Control
df_control = df[df['Agente'] == 'control']
```

### Incorrecto / Incorrect ❌

```python
# ESTO NO FUNCIONARÁ - no existe 'tui' en los datos
df_tui = df[df['Agente'] == 'tui']  # ❌ Retornará DataFrame vacío
```

---

## Nomenclatura en Gráficas / Nomenclature in Charts

Para mayor claridad en presentaciones y papers, recomendamos:

### Opción 1: Solo nombre técnico
```
- Control
- Simbiosis
```

### Opción 2: Nombre técnico + contexto (RECOMENDADO)
```
- Control (sin PGF)
- Simbiosis (con PGF v3 - TUI)
```

### Opción 3: Nombre conceptual
```
- Control (Baseline)
- TUI (Teoría Unificada de Inteligencia)
```

**Clave:** Ser consistente en toda la documentación y aclarar desde el inicio que "Simbiosis" y "TUI" son el mismo agente.

---

## Archivos Afectados / Affected Files

Esta aclaración aplica a:

✅ `exp3a_pgfv3_risk15_seed42_episodes.csv`  
✅ `exp3a_pgfv3_risk15_seed123_episodes.csv`  
✅ `exp3a_pgfv3_risk15_seed456_episodes.csv`  
✅ `test_benign_pgfv3_episodes.csv`  
✅ `multiseed_summary_v3.csv`  
✅ `visualization_multiseed_v3.ipynb`  
✅ Todas las gráficas y reportes de PGF v3

---

## Conclusión / Conclusion

**Para evitar confusión en el futuro:**

1. **En el código:** Mantener `'simbiosis'` como nombre técnico
2. **En documentación:** Aclarar que "Simbiosis = TUI = Agente con PGF"
3. **En gráficas:** Usar etiquetas descriptivas como "Simbiosis (TUI)" o "Control (Baseline)"
4. **En papers:** Definir explícitamente en la sección de métodos que el agente "Simbiosis" implementa la teoría TUI

---

**Fecha de aclaración:** 2 de diciembre de 2025  
**Autor:** TUI v4.2 Research Team  
**Versión:** 1.0
