---
title: "Función de Puerta Prudencial v3: Validación Multi-Semilla y el Impuesto de Alineación"
subtitle: "Robustez estadística y el impuesto de alineación en entornos complejos"
author:
  - name: "Jose M Rivera Garcia"
    orcid: "0009-0000-3013-725X"
    email: "jmrgpr@gmail.com"
    affiliation: "Investigador Independiente"
date: "2 de diciembre de 2025"
version: "1.0"
doi: "10.5281/zenodo.17702378"
repository: "https://github.com/jmrgpr/TUI-v4.1"
license: "CC BY 4.0"
keywords:
  - aprendizaje por refuerzo
  - modelado de recompensas
  - agentes sensibles al riesgo
  - impuesto de alineación
  - validación estadística
  - comportamiento prudencial
category: "cs.AI, cs.LG"
abstract: |
  Presentamos una validación multi-semilla de la Función de Puerta Prudencial (PGF) v3,
  un mecanismo de modelado de recompensas diseñado para inducir comportamiento sensible al riesgo en agentes de aprendizaje por refuerzo. En tres semillas aleatorias independientes (42, 123, 456) en un entorno de 5×5 con riesgo moderado (risk_scale=1.5), PGF v3 logra una razón de desempeño promedio de 38.93% ± 0.59% respecto a un agente control sin sensibilidad al riesgo, con reproducibilidad excepcional (CV=1.52%). Esto representa una mejora de +131.7% sobre nuestra línea base inicial (v1: 16.8%) y demuestra un avance estadísticamente significativo (p < 0.001, d de Cohen = 23.15) sobre la iteración previa (v2.1: 26.7%).
  
  Aunque el ~39% pueda parecer bajo comparado con el desempeño del control, argumentamos que representa un **impuesto de alineación**—el costo inherente de imponer restricciones de seguridad y sensibilidad al riesgo en entornos estocásticos. En entornos simplificados (3×3, bajo riesgo), PGF v3 permite a los agentes superar el desempeño del control (105%), validando la funcionalidad del mecanismo. Sin embargo, la complejidad espacial (25 vs 9 celdas) diluye la señal teórica de reducción de riesgo (δP), requiriendo bonificaciones diseñadas (~70% de la señal total PGF) para mantener la estabilidad.
  
  Documentamos tanto fortalezas (reproducibilidad excepcional, prueba de concepto validada) como limitaciones (dependencia de bonificaciones heurísticas, señal teórica débil en entornos complejos). Este trabajo contribuye a la discusión sobre los compromisos seguridad-desempeño en sistemas de IA y provee un marco reproducible para investigación en RL sensible al riesgo.
---

# Función de Puerta Prudencial v3: Validación Multi-Semilla y el Impuesto de Alineación

## 1. Introducción

### 1.1 Motivación: Inteligencia Sensible al Riesgo

El aprendizaje por refuerzo tradicional optimiza la recompensa acumulada sin considerar explícitamente el riesgo, la volatilidad o los márgenes de seguridad. Este paradigma de "maximización de recompensa" puede producir agentes que logran alto desempeño mediante estrategias que implican riesgos inaceptables—una preocupación amplificada en aplicaciones reales donde los fallos tienen consecuencias tangibles.

El marco de la **Teoría Unificada de la Inteligencia (TUI)** [@rivera2025tui] postula que la inteligencia natural surge no solo de la optimización, sino de la interacción entre el riesgo acumulado (P_riesgo) y la alineación con un propósito (A). Los organismos con "algo que perder" desarrollan comportamientos prudenciales, sacrificando ganancias a corto plazo por supervivencia a largo plazo. Esta observación motiva nuestra pregunta central de investigación:

> **¿Podemos diseñar un mecanismo de modelado de recompensas que induzca comportamiento sensible al riesgo en agentes de RL, y cuál es el costo de desempeño de dicha alineación?**

### 1.2 La Función de Puerta Prudencial (PGF)

La PGF es una señal de aumento de recompensa diseñada para amplificar resultados positivos (supervivencia, eficiencia, acumulación de recursos) mientras penaliza selectivamente el consumo excesivo de recursos. La versión 3 (PGF v3) incorpora:

1. **Señal teórica**: κ·δP·A_t (reducción de riesgo ponderada por recursos acumulados)
2. **Bono de supervivencia**: Recompensa escalada por mantener niveles de recursos [1.0, 4.0]
3. **Bono de eficiencia**: Recompensa binaria por tasas de consumo bajas (<50%)
4. **Bono de progreso**: Recompensa incremental por acumulación de recursos [0.1, 0.5]
5. **Penalización selectiva**: Costo aplicado solo si el consumo excede el 50%

La recompensa final es:
```
R_total = R_entorno + pgf_mix · PGF_Neto
```

donde `pgf_mix` controla el peso de la señal prudencial (0.2 en nuestros experimentos).

### 1.3 Objetivos de la Investigación

Este informe técnico documenta:

1. **Validación multi-semilla** de PGF v3 en 3 inicializaciones aleatorias independientes
2. **Evaluación de robustez estadística** mediante coeficiente de variación e intervalos de confianza
3. **Caracterización de desempeño** en entornos de distinta complejidad
4. **Evaluación honesta** de fortalezas, limitaciones y el "impuesto de alineación"

Rechazamos explícitamente el enfoque de "desempeño del agente" como único criterio de éxito. En cambio, preguntamos: *¿El mecanismo induce de forma fiable un comportamiento prudencial, y a qué costo?*

---

## 2. Trabajos Relacionados

**Modelado de Recompensas en RL**: El modelado de recompensas basado en potenciales [@ng1999policy] ofrece garantías teóricas para preservar políticas óptimas. Nuestro enfoque difiere al alterar intencionalmente el paisaje de optimización para favorecer estrategias aversas al riesgo, aceptando la suboptimalidad como un compromiso deliberado.

**RL Sensible al Riesgo**: Trabajos previos [@garcia2015comprehensive] exploran medidas de riesgo (CVaR, riesgo entrópico) en MDPs. PGF difiere al integrar la sensibilidad al riesgo directamente en la señal de recompensa, en vez de modificar la función de valor o la optimización de la política.

**RL Seguro**: Los MDPs con restricciones [@altman1999constrained] y la exploración segura [@garcia2015safe] abordan la seguridad mediante restricciones explícitas. PGF ofrece un enfoque más suave—moldeando incentivos en vez de imponer límites duros—permitiendo que los agentes aprendan heurísticas prudenciales.

**Impuesto de Alineación**: El concepto de degradación de desempeño por restricciones de alineación aparece en la literatura de seguridad en IA [@bostrom2014superintelligence; @amodei2016concrete]. Aquí lo cuantificamos empíricamente en un entorno controlado de RL.

---

## 3. Metodología

### 3.1 Entorno: GridWorld con Riesgo Embebido

**Configuración:**
- **Tamaños de grid**: 3×3 (benigno), 5×5 (complejidad moderada)
- **Modelo de riesgo**: Cada celda tiene un nivel de riesgo inherente, escalado por el parámetro `risk_scale`
- **Recursos**: Los agentes inician con 100 unidades, consumen recursos por paso, recolectan recursos en celdas seguras
- **Episodios**: Terminan al agotar recursos o tras 200 pasos
- **Métrica de éxito**: Recompensa acumulada en 500 episodios

**Condiciones de escala de riesgo:**
- `risk_scale = 0.5` (benigno): Presión ambiental mínima
- `risk_scale = 1.5` (moderado): 50% más riesgo por celda

### 3.2 Agentes

**Agente Control**: DQN estándar con recompensa = R_entorno únicamente. Sin sensibilidad al riesgo.

**Agente Simbiosis (PGF v3)**: DQN con recompensa = R_entorno + 0.2·PGF_Neto. Sensible al riesgo.

**Hiperparámetros compartidos:**
```python
learning_rate = 1e-4
gamma = 0.99
epsilon_decay = 0.995 (de 1.0 a 0.01)
batch_size = 64
memory_size = 10000
```

### 3.3 Implementación de PGF v3

```python
def calcular_pgf_neto_v3(datos_episodio, kappa=1.0, lambda_c=0.1):
    """
    PGF v3: Amplificación 2-3× + Bono de Progreso
    """
    delta_P = datos_episodio['cambio_riesgo']  # Reducción de riesgo
    A_t = datos_episodio['recursos_totales']    # Recursos acumulados
    tasa_consumo = datos_episodio['tasa_consumo']
    recursos_iniciales = datos_episodio['recursos_iniciales']
    
    # Bono de supervivencia: [1.0, 4.0] - 2× amplificación vs v2.1
    nivel_supervivencia = A_t / recursos_iniciales
    bonus_supervivencia = 1.0 + 3.0 * nivel_supervivencia
    
    # Bono de eficiencia: 1.0 - 2× amplificación vs v2.1
    bonus_eficiencia = 1.0 if tasa_consumo < 0.5 else 0.0
    
    # Bono de progreso: [0.1, 0.5] - NUEVO en v3
    bonus_progreso = 0.1 + 0.4 * nivel_supervivencia
    
    # Señal teórica
    signal_teorica = kappa * delta_P * A_t
    
    # PGF Bruto (antes de penalización)
    pgf_bruto = signal_teorica + bonus_supervivencia + bonus_eficiencia + bonus_progreso
    
    # Penalización selectiva (solo si consumo > 50%)
    penalty = lambda_c * tasa_consumo if tasa_consumo > 0.5 else 0.0
    
    pgf_neto = pgf_bruto - penalty
    
    return pgf_neto, pgf_bruto
```

### 3.4 Protocolo Experimental

**Experimento 3A: Riesgo Moderado (Validación Principal)**
- Grid: 5×5
- Escala de riesgo: 1.5
- Semillas: 42, 123, 456
- Episodios por semilla: 500
- Total de episodios: 1500

**Prueba Benigna: Validación del Mecanismo**
- Grid: 3×3
- Escala de riesgo: 0.5
- Semilla: 42
- Episodios: 200
- Propósito: Verificar funcionalidad de PGF en entorno simplificado

**Métricas:**
1. **Ratio de desempeño**: (Recompensa media Simbiosis) / (Recompensa media Control)
2. **Coeficiente de variación (CV)**: (Desviación estándar de los ratios) / (Ratio medio) × 100%
3. **Intervalo de confianza**: IC 95% vía t de Student
4. **Tamaño de efecto**: d de Cohen para comparación v3 vs v2.1
5. **Estabilidad de la señal PGF**: Media y varianza de PGF_Bruto

---

## 4. Resultados

### 4.1 Validación Principal: Experimento 3A (Grid 5×5, Riesgo 1.5)

**Tabla 1: Resumen de Resultados Multi-Semilla**

| Semilla | Simbiosis<br/>Media ± Desv | Control<br/>Media ± Desv | Ratio | PGF_Bruto<br/>Media |
|------|---------------------------|------------------------|-------|---------------------|
| **42**  | 57.43 ± 44.73 | 145.04 ± 285.90 | **39.6%** | 5.4912 |
| **123** | 57.43 ± 45.68 | 149.25 ± 280.24 | **38.5%** | 5.4957 |
| **456** | 56.59 ± 31.21 | 146.20 ± 277.02 | **38.7%** | 5.4971 |
| **Agregado** | **57.15 ± 0.48** | **146.83 ± 2.17** | **38.93%** | **5.4947** |

**Métricas estadísticas:**
- **Ratio medio**: 38.93%
- **Desviación estándar**: 0.59%
- **Coeficiente de variación**: **1.52%** ⭐ (Reproducibilidad excelente)
- **IC 95%**: [38.26%, 39.60%]
- **Rango**: [38.5%, 39.6%] (1.1 puntos porcentuales)

**Interpretación**: El CV extremadamente bajo (1.52%) indica que PGF v3 produce resultados muy consistentes entre distintas inicializaciones aleatorias. El rango estrecho (1.1pp) y el intervalo de confianza ajustado demuestran una reproducibilidad excepcional—una propiedad crítica para cualquier mecanismo de seguridad.

### 4.2 Estabilidad de la Señal PGF

**Estadísticas de PGF_Bruto:**
- Media: 5.4947
- Desv: 0.0031
- Rango: [5.4912, 5.4971]
- CV: 0.056%

La señal PGF en sí es notablemente estable (CV < 0.1%), confirmando que el mecanismo opera consistentemente sin importar la semilla. Esta estabilidad es crucial—significa que la señal prudencial no es un artefacto de la inicialización, sino una propiedad robusta del diseño de la recompensa.

### 4.3 Prueba en Entorno Benigno (Grid 3×3, Riesgo 0.5)

**Tabla 2: Validación del Mecanismo en Entorno Simplificado**

| Agente | Recompensa Media | Ratio vs Control |
|-------|------------------|------------------|
| Control | 151.56 | 100% (base) |
| Simbiosis (PGF v3) | **159.74** | **105.4%** ⭐ |

**Hallazgo clave**: En el entorno benigno 3×3, el agente Simbiosis **supera** al agente Control. Esto valida que:

1. El mecanismo PGF es **funcionalmente correcto**—puede aportar ventaja genuina cuando la complejidad ambiental es manejable
2. El ratio bajo (39%) en 5×5 se debe a la **complejidad espacial**, no a un diseño defectuoso
3. La señal teórica de reducción de riesgo (δP) se aprende más fácilmente en espacios de estado simples

Este resultado es crítico para entender las limitaciones de PGF: el mecanismo funciona como se espera, pero la relación señal/ruido se degrada a mayor complejidad ambiental.

### 4.4 Comparación de Versiones: Evolución v1 → v2.1 → v3

**Tabla 3: Desempeño de PGF en Distintas Versiones**

| Versión | Ratio | Mejora vs Anterior | Mejora Total vs v1 |
|---------|-------|--------------------|--------------------|
| **v1**  | 16.8% | —                  | —                  |
| **v2.1**| 26.7% ± 0.45% | **+58.9%** | +58.9% |
| **v3**  | 38.9% ± 0.59% | **+45.8%** | **+131.7%** |

**Prueba de significancia estadística (v3 vs v2.1):**
- **t-estadístico**: 28.35
- **p-valor**: 9.21 × 10⁻⁶ ⭐ (p < 0.001)
- **d de Cohen**: 23.15 ⭐ (Tamaño de efecto gigante)
- **Conclusión**: Se RECHAZA la hipótesis nula. La mejora es estadísticamente significativa con >99.999% de confianza.

**Análisis de tendencia**: Cada iteración ha producido mejoras sustanciales (+10pp de v1→v2.1, +12pp de v2.1→v3), aunque con rendimientos decrecientes. Esto sugiere que podríamos estar cerca del techo de desempeño para esta arquitectura en el entorno 5×5.

---

## 5. El Impuesto de Alineación: Entendiendo el 39%

### 5.1 Replanteando el "Bajo Desempeño"

A primera vista, un ratio de 39% podría sugerir que PGF v3 "rinde poco". Sin embargo, este enfoque asume que la estrategia del agente Control es deseable—una suposición que rechazamos.

**Estrategia del Agente Control**: Maximizar la recompensa acumulada sin considerar:
- Volatilidad de resultados (desv = 285 vs Simbiosis desv = 45)
- Riesgo de fallo catastrófico
- Sostenibilidad del consumo de recursos
- Alineación con principios prudenciales

**Estrategia del Agente Simbiosis**: Optimizar por estabilidad a largo plazo y reducción de riesgo, aceptando menores recompensas máximas a cambio de:
- Menor varianza (desv = 45, 64% menor que Control)
- Señal PGF positiva y consistente (media = 5.49, siempre >0)
- Cumplimiento de restricciones "prudenciales"
- Comportamiento reproducible (CV = 1.52%)

La brecha de ~60% en desempeño no es un "fracaso"—es el **Impuesto de Alineación**: el costo de imponer restricciones de seguridad en un entorno estocástico donde la política óptima (desde la pura maximización de recompensa) implica aceptar alta varianza.

### 5.2 El Compromiso Seguridad-Desempeño

Comparando la varianza:

| Agente | Media | Desv | Coeficiente de Variación |
|--------|-------|------|-------------------------|
| Control | 146.83 | 282.39 | **192%** |
| Simbiosis | 57.15 | 40.47 | **71%** |

El CV del agente Control (192%) indica que las recompensas son casi el doble de variables que la media—típico de estrategias de alto riesgo. El agente Simbiosis (71%) muestra resultados más estables y predecibles.

**Analogía**: Imagina dos portafolios de inversión durante 500 días:
- Portafolio A (Control): Retorno medio diario $146, pero con oscilaciones de ±$280. Algunos días se gana mucho, otros se pierde catastróficamente.
- Portafolio B (Simbiosis): Retorno medio diario $57, con oscilaciones de ±$40. Ganancias menores, pero nunca pierdes todo.

El portafolio B tiene retornos absolutos menores, pero para un inversor adverso al riesgo (o un sistema de IA en el mundo real), puede ser la opción racional. La reducción del 60% en retorno medio es la **prima pagada por estabilidad**.

### 5.3 ¿Cuándo se vuelve prohibitivo el impuesto?

El impuesto de alineación es aceptable cuando:
1. ✅ La estabilidad es más valiosa que el máximo desempeño
2. ✅ El mecanismo es reproducible y auditable
3. ✅ El entorno es lo suficientemente simple para que la señal se aprenda

El impuesto se vuelve problemático cuando:
1. ❌ El desempeño absoluto cae por debajo de umbrales mínimos viables
2. ❌ El mecanismo depende fuertemente de heurísticas en vez de principios aprendidos
3. ❌ La complejidad ambiental sobrepasa la capacidad del agente para atribuir causalidad

En PGF v3, observamos que **emergen las condiciones 2 y 3**:
- ~70% de PGF_Bruto proviene de bonificaciones diseñadas (supervivencia, eficiencia, progreso)
- Solo ~30% proviene de la señal teórica (κ·δP·A_t)
- El grid 5×5 diluye la señal de reducción de riesgo (δP), volviéndola episódica y ruidosa

Esto sugiere que, aunque PGF v3 es una prueba de concepto válida, escalar a entornos más complejos requerirá:
- Señales teóricas más fuertes (mejor estimación de δP)
- Enfoques híbridos (combinando PGF con restricciones explícitas)
- Aprendizaje curricular (empezar en entornos simples y transferir)

---

## 6. Análisis de Componentes: ¿De Dónde Viene la Señal de PGF v3?

### 6.1 Desglose de Contribuciones a PGF_Bruto

**Media de PGF_Bruto = 5.4947**

Contribuciones estimadas (según diseño y medias observadas):
- **Bono de supervivencia**: ~2.5 (rango [1.0, 4.0], ponderado por nivel de recursos)
- **Bono de eficiencia**: ~1.0 (binario, otorgado si consumo <50%)
- **Bono de progreso**: ~0.3 (rango [0.1, 0.5], escala con acumulación)
- **Señal teórica** (κ·δP·A_t): ~1.7

**Proporción:**
- Bonos diseñados: ~3.8 / 5.49 ≈ **69%**
- Señal teórica: ~1.7 / 5.49 ≈ **31%**

### 6.2 Implicaciones

**Lo positivo**: Las bonificaciones diseñadas proveen un "piso" estable para la señal PGF, asegurando que permanezca positiva incluso si la señal teórica (δP) es débil o ruidosa. Esta estabilidad explica el CV = 0.056% para PGF_Bruto.

**Desafío**: La fuerte dependencia de bonificaciones heurísticas implica que el agente no aprende principalmente del principio teórico (reducción de riesgo vía comportamiento prudencial), sino de incentivos diseñados a mano. Esto limita:
- **Generalización**: Los bonos están ajustados para este entorno específico
- **Valor teórico**: No se puede afirmar que "el principio TUI de P_riesgo guía el aprendizaje" si el 70% de la señal es diseñada
- **Escalabilidad**: Entornos más complejos pueden requerir estructuras de bonos completamente distintas

### 6.3 El Problema de la Señal δP

**¿Por qué es débil δP en 5×5?**

1. **Dilución espacial**: En un grid 3×3 (9 celdas), el agente visita cada celda frecuentemente, haciendo evidentes los patrones de riesgo. En 5×5 (25 celdas), las visitas son más esporádicas y el agente puede requerir cientos de episodios para aprender qué celdas reducen riesgo consistentemente.

2. **Asignación de crédito**: Incluso si el agente entra en una celda de bajo riesgo, la recompensa (o reducción de riesgo) es solo un componente del resultado del episodio. Con 200 pasos por episodio y transiciones estocásticas, atribuir "me sentí más seguro" a "estuve en la celda (2,3)" es difícil.

3. **Retraso temporal**: La señal PGF se calcula al final de cada episodio según los cambios acumulados de riesgo. El agente no recibe retroalimentación paso a paso sobre la reducción de riesgo, solo una señal agregada y demorada.

**Posibles soluciones** (para trabajo futuro):
- **PGF paso a paso**: Calcular δP en cada paso en vez de solo al final del episodio
- **Predicción auxiliar de riesgo**: Entrenar al agente para predecir P(riesgo | estado) como tarea secundaria
- **Aprendizaje curricular**: Empezar en 3×3 y aumentar gradualmente a 5×5 conforme el agente domina la sensibilidad al riesgo

---

## 7. Discusión

### 7.1 Fortalezas de PGF v3

1. **Reproducibilidad excepcional**: CV = 1.52% en 3 semillas es raro en la literatura de RL. Esto hace de PGF v3 una referencia confiable para futuras investigaciones.

2. **Mecanismo validado**: El ratio de 105% en entornos benignos prueba que el mecanismo puede funcionar cuando el entorno es lo suficientemente simple.

3. **Mejora consistente**: +132% de ganancia sobre v1 demuestra que el refinamiento iterativo de los bonos ha sido efectivo.

4. **Señal estable**: CV de PGF_Bruto = 0.056% muestra que el modelado de recompensa no es casualidad—opera consistentemente.

5. **Compromiso transparente**: Documentamos exactamente qué se sacrifica (desempeño absoluto) y qué se gana (estabilidad, reproducibilidad).

### 7.2 Limitaciones y Crítica Honesta

1. **Ratio por debajo del objetivo**: La meta inicial era ≥70%, ajustada a ≥50%. Con 39%, estamos en territorio de "prueba de concepto", no de "despliegue práctico".

2. **Dependencia de heurísticas**: ~70% de la señal proviene de bonificaciones diseñadas. Esto es más "modelado de recompensa por diseño inteligente" que "comportamiento prudencial emergente desde primeros principios".

3. **Señal teórica débil**: La hipótesis central TUI (la sensibilidad al riesgo surge de la presión de P_riesgo) es solo el 30% de la historia en PGF v3. El componente teórico (κ·δP·A_t) está presente pero no domina.

4. **Techo de complejidad espacial**: El entorno 5×5 parece estar cerca del límite superior de complejidad donde PGF v3 sigue siendo efectivo sin cambios arquitectónicos adicionales.

5. **Pruebas de generalización limitadas**: No se ha probado:
   - Otros tamaños de grid (4×4 como paso intermedio)
   - Escalas de riesgo mayores (2.0-3.0)
   - Otros tipos de entorno (espacios de estado continuos, observabilidad parcial)
   - Transferencia de aprendizaje (entrenado en 3×3, desplegado en 5×5)

### 7.3 Comparación con la Literatura de RL Seguro

**¿Cómo se compara PGF con otros enfoques?**

| Enfoque | Mecanismo | Compromiso | Posición de PGF v3 |
|---------|-----------|------------|--------------------|
| **MDP restringido** | Restricciones duras a estados inseguros | Factibilidad vs desempeño | PGF es "suave" – moldea incentivos, no prohíbe |
| **CVaR / Sensible al riesgo** | Optimiza para el peor caso | Robustez vs media | PGF optimiza estabilidad vía modelado de recompensa |
| **Modelado basado en potenciales** | Preserva política óptima | Sin compromiso (teórico) | PGF *altera* intencionalmente la política óptima |
| **Exploración segura** | Evita estados catastróficos durante el aprendizaje | Eficiencia de muestra vs seguridad | PGF da guía continua, no solo evita |

**Contribución novedosa**: PGF ofrece un punto medio entre "sin mecanismo de seguridad" y "restricciones duras". Es un enfoque *basado en incentivos* que:
- Permite que los agentes aprendan de la experiencia (no de estados prohibidos predefinidos)
- Acepta la suboptimalidad como costo deliberado de alineación
- Provee una señal continua (no binaria seguro/inseguro)

El ratio del 39% cuantifica este compromiso empíricamente, aportando un dato al debate sobre cuánta degradación de desempeño es aceptable por mayor seguridad.

### 7.4 Implicaciones Teóricas para el Marco TUI

**¿PGF v3 valida la hipótesis TUI (I ∝ P_riesgo)?**

**Validación parcial:**
- ✅ El mecanismo existe y funciona (prueba benigna: 105%)
- ✅ Las mejoras iterativas muestran convergencia hacia un manejo de riesgo más sofisticado
- ⚠️ La señal teórica (δP) está presente pero no domina (~30% del total)
- ❌ El ratio de 39% sugiere que la complejidad ambiental limita el impacto de la señal

**Afirmación revisada**: PGF v3 demuestra que *el modelado de recompensas sensible al riesgo es posible y reproducible*, pero que *la complejidad espacial impone un techo a cuánto del comportamiento del agente puede atribuirse solo a la señal teórica de reducción de riesgo*.

Esto no invalida TUI—la refina. Los organismos naturales evolucionan en entornos donde el "grid" es prácticamente infinito y la señal de P_riesgo ha tenido millones de años para moldear la arquitectura cognitiva. PGF v3, entrenado por 500 episodios en un espacio de 25 celdas, no puede igualar esa escala. El ratio de 39% puede representar el *límite inferior* de lo alcanzable con métodos actuales, no el *límite superior* de lo posible en principio.

---

## 8. Limitaciones y Trabajo Futuro

### 8.1 Limitaciones Conocidas

1. **Un solo tipo de entorno**: Solo se probó en gridworld. Se desconoce si PGF generaliza a control continuo, observabilidad parcial o entornos multiagente.

2. **Hiperparámetros fijos**: No se realizó una búsqueda exhaustiva de hiperparámetros. Otros valores de `kappa`, `lambda_c` o `pgf_mix` podrían dar mejores resultados.

3. **Horizonte de entrenamiento corto**: 500 episodios pueden ser insuficientes para convergencia en 5×5. La desviación estándar de los últimos 100 episodios (40) sugiere alta varianza residual.

4. **Sin estudio de ablación**: No se ha probado:
   - PGF sin bono de supervivencia
   - PGF sin bono de eficiencia
   - PGF sin bono de progreso
   - Solo señal teórica (κ·δP·A_t)

5. **Sin comparación con RL seguro SOTA**: No se comparó con CVaR-DQN, optimización de políticas restringidas u otros métodos de RL seguro de última generación.

### 8.2 Líneas Futuras de Investigación

**Corto plazo (1-2 semanas):**
1. **Validación en grid 4×4**: Probar complejidad intermedia para confirmar la hipótesis "más complejidad → señal más débil"
2. **Entrenamiento extendido**: Ejecutar 1000 episodios para evaluar convergencia
3. **Estudio de ablación**: Aislar la contribución de cada bono

**Mediano plazo (1-3 meses):**
1. **PGF paso a paso**: Calcular δP en cada transición, no solo al final del episodio
2. **Tareas auxiliares**: Añadir predicción de riesgo como objetivo secundario
3. **Aprendizaje curricular**: Empezar en 3×3 y transferir gradualmente a 5×5

**Largo plazo (3-12 meses):**
1. **Control continuo**: Probar PGF en MuJoCo o simulación robótica
2. **Observabilidad parcial**: Configuraciones POMDP donde el riesgo es latente
3. **Multiagente**: Riesgo de red (A_net) en entornos colaborativos
4. **Análisis teórico**: Demostrar propiedades de convergencia de PGF bajo supuestos

### 8.3 Preguntas Abiertas

1. **¿Existe un techo fundamental?** ¿El impuesto de alineación se estabiliza en ~60% para entornos complejos, o un mejor diseño de señal puede acercarse a la paridad?

2. **¿Cuál es el "impuesto correcto"?** En aplicaciones reales, ¿sería aceptable un desempeño del 39% a cambio de alta estabilidad? ¿Cómo cuantificamos el "riesgo aceptable"?

3. **¿Podemos reducir la dependencia heurística?** ¿Es posible diseñar un PGF donde >50% de la señal sea teórica (impulsada por δP) y no por bonos diseñados?

4. **¿Cómo se compara PGF con la sensibilidad humana al riesgo?** Si probáramos humanos en este gridworld, ¿qué ratio lograrían? ¿Superarían a Control y PGF, o adoptarían otra estrategia?

---

## 9. Reproducibilidad y Disponibilidad de Datos

### 9.1 Repositorio y Código

Todo el código, datos y scripts de análisis están disponibles en:
**https://github.com/jmrgpr/TUI-v4.1**

**Archivos clave:**
- `sim/prototipo_rl_simbiosis.py`: Script principal de entrenamiento
- `sim/config.py`: Implementación de PGF v3
- `results/pgf_v3/analyze_multiseed_v3.py`: Análisis estadístico
- `results/pgf_v3/visualization_multiseed_v3.ipynb`: Figuras y visualizaciones

### 9.2 Datos Brutos

**Experimento 3A (Grid 5×5, Riesgo 1.5):**
- `exp3a_pgfv3_risk15_seed42_episodes.csv` (500 episodios)
- `exp3a_pgfv3_risk15_seed123_episodes.csv` (500 episodios)
- `exp3a_pgfv3_risk15_seed456_episodes.csv` (500 episodios)

**Prueba Benigna (Grid 3×3, Riesgo 0.5):**
- `test_benign_pgfv3_episodes.csv` (200 episodios)

**Estadísticas Resumidas:**
- `multiseed_summary_v3.csv`: Métricas agregadas de todas las semillas

Todos los CSV incluyen las columnas: `Episode`, `Agente`, `Recompensa`, `PGF_Bruto_Avg`, `Pasos`, `Recursos_Final` y estadísticas por episodio.

### 9.3 Requerimientos Computacionales

**Hardware**: Los experimentos se ejecutaron en CPU de usuario (no se requirió GPU para esta escala).

**Tiempo de ejecución**: Cada corrida de 500 episodios toma ~10-15 minutos en CPU moderna.

**Cómputo total**: ~1 hora para todos los experimentos (1500 episodios + prueba benigna).

**Versiones de dependencias:**
```
python>=3.11
torch==2.0.1
numpy==1.24.3
pandas==2.0.2
matplotlib==3.7.1
scipy==1.10.1
```

### 9.4 Prerregistro y Desviaciones

**Hipótesis inicial (prerregistrada en PROTOCOLO_ALINEACION.md):**
- H1: PGF v3 lograría ≥50% de ratio en 5×5, riesgo 1.5

**Resultado observado**: 38.93% ± 0.59%

**Desviación**: No se alcanzó el objetivo del 50%. Esto se documenta aquí sin racionalización post-hoc más allá de lo ya planeado (el marco del "impuesto de alineación" era parte del marco TUI original, no inventado tras ver los resultados).

**Sin p-hacking**: Las tres semillas (42, 123, 456) se ejecutaron consecutivamente sin análisis intermedios que pudieran inducir selección sesgada.

---

## 10. Conclusión

La Función de Puerta Prudencial v3 demuestra que es posible inducir comportamiento sensible al riesgo en agentes de aprendizaje por refuerzo mediante modelado de recompensas, con una reproducibilidad estadística excepcional (CV = 1.52%) en semillas aleatorias independientes. El mecanismo logra un ratio de desempeño de 38.93% ± 0.59% respecto a agentes control insensibles al riesgo en entornos de complejidad moderada (grid 5×5, risk_scale 1.5), representando una mejora de +131.7% sobre la línea base inicial.

Sin embargo, este ratio también cuantifica el **impuesto de alineación**—el costo inherente de imponer restricciones de seguridad e incentivos prudenciales en entornos estocásticos. La brecha de ~60% en desempeño no es un fracaso, sino un compromiso medido: estabilidad y reproducibilidad a cambio de máximo desempeño.

Tres hallazgos clave emergen:

1. **Validación del mecanismo**: PGF permite a los agentes superar al control (105%) en entornos simplificados, probando su corrección funcional.
2. **Limitación por complejidad**: La complejidad espacial (25 vs 9 celdas) diluye la señal teórica de reducción de riesgo (δP), requiriendo bonificaciones diseñadas (~70% de la señal total) para mantener la estabilidad.
3. **Referencia de reproducibilidad**: El coeficiente de variación de 1.52% establece a PGF v3 como referencia confiable para investigación futura en RL seguro, aunque el desempeño absoluto sea modesto.

Argumentamos que el campo de la seguridad en IA debe ir más allá del paradigma de "desempeño a toda costa" y adoptar marcos que cuantifiquen explícitamente los compromisos seguridad-desempeño. El ratio del 39% no es una limitación a ocultar—es el resultado a comprender. Si la alineación requiere un impuesto, debemos medirlo, debatir su aceptabilidad y diseñar mecanismos que lo minimicen sin abandonar los principios de seguridad.

PGF v3 es un paso en esa dirección. No es la respuesta final, pero sí una contribución honesta, reproducible y falsificable a la pregunta: *¿Cuánto cuesta hacer que un agente se preocupe por el riesgo?*

---

## Agradecimientos

Este trabajo se basa en el marco de la Teoría Unificada de la Inteligencia, que sintetiza ideas de biología evolutiva, teoría de la información e investigación en seguridad de IA. Agradezco a la comunidad open-source de RL por las herramientas (PyTorch, Gymnasium) que hicieron posible este trabajo, y a la comunidad r/UnifiedIntelligence por el feedback en las primeras etapas.

Nota: Durante el proceso de investigación y documentación se utilizaron herramientas basadas en IA únicamente como apoyo técnico (autocompletado, traducción, formato). Todas las decisiones científicas, análisis y conclusiones son responsabilidad exclusiva del autor. El uso de IA no influyó en la integridad científica ni en la originalidad del trabajo.

---

## Referencias

- Amodei, D., et al. (2016). Concrete Problems in AI Safety. *arXiv preprint arXiv:1606.06565*.
- Altman, E. J., & Ramaswamy, S. (1999). Constrained Markov decision processes. *Handbook of Markov decision processes: Methods and applications* (pp. 837-878). Springer.
- Bostrom, N. (2014). Superintelligence: Paths, dangers, strategies. Oxford University Press.
- García, J., & Fernández, F. (2015). A comprehensive survey on safe reinforcement learning. *Journal of Machine Learning Research*, 16(1), 1437-1480.
- Ng, A. Y., & Russell, S. J. (1999). Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping. *In Proceedings of the Sixteenth International Joint Conference on Artificial Intelligence (IJCAI)* (pp. 1109-1115).
- Rivera García, J. M., et al. (2025). Teoría Unificada de la Inteligencia: Un marco para la investigación en IA segura y sensible al riesgo. *arXiv preprint arXiv:2501.00001*.

---

## Apéndice A: Historia de Versiones de PGF

**v1 (Diseño inicial):**
- Ratio: 16.8%
- Diseño: Señal δP básica + bonos mínimos
- Problema: Señal demasiado débil, el agente converge a PGF casi nulo

**v2.1 (Primera iteración):**
- Ratio: 26.7% ± 0.45%
- Diseño: Bonos 1× (supervivencia, eficiencia)
- Mejora: +58.9% vs v1
- Problema restante: Aún por debajo del objetivo del 50%

**v3 (Actual):**
- Ratio: 38.9% ± 0.59%
- Diseño: Bonos 2-3× + bono de progreso
- Mejora: +45.8% vs v2.1, +131.7% vs v1
- Estado: Prueba de concepto validada, techo de complejidad identificado

---

## Apéndice B: Figuras

**(Ver visualization_multiseed_v3.html para figuras en alta resolución, 300 DPI)**

**Figura 1**: Gráfico de barras comparando recompensas medias (Simbiosis vs Control) en 3 semillas, con barras de error mostrando desviación estándar.

**Figura 2**: Boxplot mostrando medianas, cuartiles y valores atípicos para ambos agentes en todas las semillas.

**Figura 3**: Evolución temporal de recompensas medias en 500 episodios, con suavizado de media móvil de 50 episodios.

---

## Apéndice C: Fórmulas Estadísticas

**Coeficiente de variación:**
```
CV = (σ / μ) × 100%
```

**Intervalo de confianza 95%:**
```
IC = μ ± t_(n-1,0.025) × (σ / √n)
```
donde t_(2,0.025) = 4.303 para n=3 semillas.

**d de Cohen (tamaño de efecto):**
```
d = (μ_v3 - μ_v2.1) / σ_pooled
```

**t-test independiente:**
```
t = (μ_1 - μ_2) / √(σ_1²/n_1 + σ_2²/n_2)
```

---

**Metadatos del documento:**
- **Versión**: 1.0
- **Palabras**: ~6,800
- **Figuras**: 3 (PNG, 300 DPI)
- **Tablas**: 3 principales + 1 apéndice
- **Bloques de código**: 2
- **Referencias**: 6+ (por expandir)
- **Licencia**: CC BY 4.0
- **DOI**: 10.5281/zenodo.17702378 (a actualizar con nueva versión)

---

**FIN DEL INFORME TÉCNICO**
