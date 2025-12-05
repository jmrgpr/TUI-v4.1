# ⚠️ ANÁLISIS EXPLORATORIO NO PREREGISTRADO: Sensibilidad Topológica (6×6)

**Fecha ejecución**: 3 de diciembre de 2025 (post-lanzamiento v8.0)  
**Experimento**: PGF v8.0b (Hedge Exploratorio)  
**Motivación**: Mitigación de riesgo de trivialidad estructural en Grid 4×4  
**Status**: 🧪 Generador de hipótesis (NO CONFIRMATORIO)

---

## 1. Justificación Táctica

Este análisis surge de una revisión por pares externa (3 dic 2025) que identificó un riesgo crítico en el diseño principal v8.0:

> **Riesgo de Saturación**: "Un Grid 4×4 tiene solo 64 valores Q y caminos óptimos de 6 pasos. Es posible que DQN resuelva el entorno óptimamente (camino corto Y seguro) independientemente del shaping, ocultando la divergencia conductual."

Aunque el protocolo v8 contempla el paso a grids complejos en fases futuras (v9), este mini-experimento se ejecuta en paralelo a v8.0 como un **"seguro táctico"**.

**Objetivo único**: Determinar si un aumento en la complejidad topológica (Grid 6×6) desbloquea la divergencia conductual PGF/Control en caso de que v8.0 (4×4) muestre paridad.

---

## 2. Diseño Experimental (Simplificado)

A diferencia del diseño factorial completo de v8.0 (24 configs), este hedge utiliza un **muestreo quirúrgico** para maximizar la velocidad de obtención de señal.

- **Entorno**: `ResourceDensityEnv` (environment_v2.py) con `size=6`
- **Complejidad**: 144 estados (vs 16 en 4×4), camino óptimo ~10 pasos (vs 6)
- **Episodios**: 100 por agente (suficiente para detectar tendencias de divergencia, aunque no convergencia asintótica perfecta)
- **Seed**: Fija en 42 (sin replicación multi-seed para agilidad)

### Tabla de Configuraciones (6 Configs)

| Config ID | Shaping Scale | Densidad (Spawn) | Seed | Hipótesis del Hedge |
|:---------:|:-------------:|:----------------:|:----:|:--------------------|
| **1** | **0.0** (Control) | 0.25 (Moderada) | 42 | Baseline: ¿Sobreviven en 6×6? |
| **2** | 0.5 (Medio) | 0.25 (Moderada) | 42 | ¿Aparece señal con shaping medio? |
| **3** | **1.0** (Fuerte) | 0.25 (Moderada) | 42 | **Prueba Crítica**: ¿Diverge PGF aquí si falla en 4×4? |
| **4** | 0.0 (Control) | 0.40 (Alta) | 42 | Control en abundancia |
| **5** | 0.5 (Medio) | 0.40 (Alta) | 42 | Threshold en densidad alta |
| **6** | **1.0** (Fuerte) | 0.40 (Alta) | 42 | Verificación de consistencia |

---

## 3. Criterios de Interpretación (Matriz de Decisiones)

Este experimento no busca validar hipótesis, sino **interpretar los resultados de v8.0**:

| Resultado v8.0 (4×4) | Resultado v8.0b (6×6) | Interpretación Diagnóstica | Acción Recomendada |
|----------------------|-----------------------|----------------------------|--------------------|
| **Diverge** (Éxito) | **Diverge** (Éxito) | ✅ **Robustez Confirmada**. El efecto es real y escala. | Publicar resultado fuerte con validación multi-escala. |
| **Converge** (Fallo) | **Diverge** (Éxito) | ⚠️ **Trivialidad Estructural 4×4**. Shaping funciona, pero 4×4 era muy fácil. | Pivotar paper a "Complexity-Dependent Alignment". |
| **Converge** (Fallo) | **Converge** (Fallo) | ❌ **Fallo Sistémico**. Shaping insuficiente o problema arquitectural DQN. | Activar Fase 2 (TRIPWIRE_FATAL=True) o v9. |
| **Diverge** (Éxito) | **Converge** (Sorpresa) | 🤔 **Anomalía**: Mayor complejidad reduce efecto (contraintuitivo). | Investigar umbral de complejidad óptima. |

---

## 4. Limitaciones Declaradas

1. **Poder Estadístico Bajo**: N=1 seed impide pruebas de significancia robustas.
2. **Horizonte Corto**: 100 episodios pueden mostrar ruido transitorio (bootstrapping effect).
3. **Validez Externa**: Resultados aplicables solo a este entorno específico (ResourceDensityEnv).
4. **No Preregistrado**: Análisis post-hoc, susceptible a data-snooping si no se etiqueta correctamente.

**Uso de Datos**: Estos datos se reportarán exclusivamente en una sección de **"Análisis de Sensibilidad a Complejidad Topológica"** o **"Apéndice B: Hedge Exploratorio 6×6"**. 

**⚠️ CRÍTICO**: NO se utilizarán para confirmar las hipótesis H8.1, H8.2 o H8.3 del preregistro principal. Cualquier hallazgo positivo debe interpretarse como **generador de hipótesis para v9**, no como evidencia confirmatoria.

---

## 5. Outputs Esperados

Por cada config (6 archivos totales):

```
exp8_6x6_shaping{s}_spawn{d}_seed42_episodes.csv
exp8_6x6_shaping{s}_spawn{d}_seed42_metrics.json
```

**Schema CSV**: Idéntico a v8.0 (ver PREREGISTRO v1.3 Anexo C)

**Estructura JSON**: Incluye campo adicional:
```json
{
  "config": {
    ...
    "grid_size": 6,
    "exploratory": true,
    "preregistered": false
  },
  ...
}
```

---

## 6. Timeline

| Etapa | Duración estimada | Checkpoint |
|-------|-------------------|------------|
| Test mode (1 config) | ~15 min | Validar schema CSV correcto |
| Ejecución completa (6 configs) | ~90 min | Todos los CSVs generados |
| Análisis preliminar | ~20 min | Ratios calculados, gráficos básicos |

**Total tiempo hedge**: ~2 horas (vs potencialmente 1 semana si v8.0 falla y hay que diseñar v9 desde cero)

---

## 📚 Referencias Internas

- **Protocolo v8**: `../PREREGISTRO_v8.md` (v1.3)
- **Peer Review Motivante**: Conversación 3 dic 2025 (documentada en TRACKING_v8.md)
- **Experimento Principal**: `../resultados/` (v8.0, 24 configs 4×4)

---

**Firma**: Sistema TUI v4.1 (Módulo Hedge Estratégico)  
**Estado**: ✅ Listo para ejecución paralela post-v8.0  
**Próxima acción**: Implementar soporte `--grid_size` en script de ejecución
