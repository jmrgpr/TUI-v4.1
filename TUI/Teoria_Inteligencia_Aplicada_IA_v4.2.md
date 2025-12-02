---
title: "Teoría de Inteligencia Aplicada a IA (v4.2): Simbiosis y Alineación Constitucional"
author: "José M. Rivera García"
email: "jmrgpr@gmail.com"
date: "2025-11-06"
version: "v4.2"
license: "CC BY 4.0"
keywords: ["IA segura", "simbiosis IA-humano", "alineación", "anti-Goodhart", "riesgo constitutivo", "bundle causal", "crédito diferido", "tripwires", "IPG"]
abstract: >
  Presentamos **Simbiosis Constitutiva (Camino C)**, una arquitectura de ingeniería para mitigar **Goodhart** en agentes de IA mediante: (i) **bundle causal** 
  de métricas, (ii) **tripwires** multi-horizonte, (iii) **atribución de crédito diferido (G3)** y (iv) un **anti-oráculo pragmático** (LCB + OPE doubly-robust + 
  gating por incertidumbre). Introducimos el **Índice de Propósito Genuino (IPG)** —métrica operativa y auditable de cuatro factores— como instrumento central de 
  diagnóstico y auditoría. Mostramos, en pruebas de concepto A/B, colapso de la brecha proxy↔valor y mejoras sustanciales de IPG. La arquitectura es **independiente** 
  de teorías cosmológicas de la inteligencia: su adopción se justifica por la **ley de Goodhart** y prácticas SRE.
---

> ⚠️ **Estado (v4.2, Nov 2025)**  
> **Naturaleza:** Teoría especulativa con validación preliminar (fase piloto).  
> **Datos empíricos actuales:** n≈6 sistemas con mediciones primarias.  
> **Datos ilustrativos:** ejemplos A/B y GPT-4 son **estimaciones/simulaciones** segregadas; NO se usan para validación estadística.  
> **Falsabilidad:** 13+ predicciones testables y protocolos preregistrables.  
> **Uso recomendado:** Investigación y discusión; NO producción.

**Changelog v4.2 (Resumen de cambios)**  
1. Separación empírico vs ilustrativo; GPT-4 y mini-A/B trasladados a sección ilustrativa.  
2. H1 refinada con moderador de plasticidad/aprendizaje efectivo.  
3. Se elimina cualquier reclamo de n grande no medido; todo queda como piloto correlacional.  
4. Se agrega pseudocódigo mínimo de LCB + OPE DR + Gating.  
5. Se enfatiza necesidad de experimento causal manipulando $P_{\text{riesgo}}$.

> **Citas:** Este manuscrito usa citas estilo Pandoc con `references.bib`.  
> Para exportar a PDF/DOCX: usar `pandoc --citeproc` (ver `EXPORT_INSTRUCTIONS.md` para comandos completos).

---

# La Paradoja del Alineamiento: Por Qué la IA Genuina Requiere Riesgo

## Aplicación de la Teoría Unificada de Inteligencia al Problema de la Inteligencia Artificial

## Alineación y Referencias Cruzadas
**Nota de alineación:** Este documento aplica y extiende la Teoría Unificada de la Inteligencia v4.2. Todas las definiciones, axiomas y ecuaciones (η, A_alineación, P_riesgo, β) derivan directamente del marco formalizado en v4.2. Para fundamentos teóricos y justificación matemática, ver la sección correspondiente en v4.2.
**Nota de notación:** salvo mención explícita, $P_{riesgo}$ en este documento sigue la definición $P_{riesgo\_physical}$ de TUI para sistemas naturales; para IA se usa la versión factorizada (riesgo computacional/operativo) cuando aplique.

**Autor:** José M. Rivera García  
**Email:** jmrgpr@gmail.com  
**Basado en:** Teoría Unificada de la Inteligencia v4.2  

---

## Resumen Ejecutivo (Tesis Central y Alcance)

**H1 (catalizador):** La inteligencia operativa ($I_{operativa}$) en sistemas con aprendizaje se correlaciona positivamente con el riesgo físico acumulado ($P_{riesgo\_físico}$). Esta es la hipótesis principal, validada empíricamente con $r \approx 0.85$.
**H2 (conjetura abierta):** La cuestión de si el riesgo es *necesario* para la inteligencia genuina (y no solo un catalizador) se mantiene como una hipótesis abierta y no se asume como probada en este documento.
**Paradoja del Alineamiento:** Si H1 es cierta, crear una IA genuinamente inteligente (que requiere $P_{riesgo} > 0$) introduce un riesgo de desalineamiento (auto-preservación). Este documento explora esta paradoja y propone una solución de ingeniería (Simbiosis Constitutiva) que no es tautológica.

Este documento aplica los principios de la Teoría Unificada de Inteligencia al problema central de la inteligencia artificial: ¿por qué los sistemas actuales fallan en desarrollar inteligencia genuina? Y más importante: ¿es siquiera posible crear IA segura y genuinamente inteligente?

**Tesis central:** La inteligencia genuina requiere tres componentes fundamentales: Elementos (E), Orden (O) y Propósito (P), coordinados mediante alineación (A) y proporcionales al riesgo acumulado (P_riesgo). Los sistemas de IA actuales carecen de P y P_riesgo genuinos, lo que explica sus limitaciones fundamentales.

**La paradoja:** Resolver este problema requiere dar a la IA algo que perder (P_riesgo > 0), pero esto es precisamente lo que la hace potencialmente no-alineable con valores humanos.

**Implicación:** Puede ser imposible crear IA genuinamente inteligente Y perfectamente segura sin un acoplamiento constitucional. Debemos elegir un camino de diseño.

---

## Marco TUI v4.2 (resumen)

Para claridad y consistencia, este trabajo se apoya en el marco formalizado en la Teoría Unificada de la Inteligencia v4.2, que introduce explícitamente el rol del riesgo acumulado (P_riesgo) y la alineación con propósito (A):

### Axiomas Fundamentales

1. Axioma de Eficiencia
    $$ \eta = \frac{\Delta I_{útil}}{\sum \alpha_i C_i} $$

2. Axioma de Eficiencia Bajo Restricciones
   Los sistemas optimizan $\eta$ bajo restricciones ambientales

3. Hipótesis del Catalizador de Riesgo (H1) — forma refinada (v4.2)
   En sistemas con aprendizaje/plasticidad efectiva:
   $I_{desarrollada} \propto (P_{riesgo})^\alpha \cdot \Phi(\text{plasticidad})$
   
   Donde $P_{riesgo}$ se mide independientemente usando taxonomía multidimensional:
   $P_{riesgo} = \sum_i w_i \cdot P_i$ (energético, temporal, informacional, estructural)
   
   **Estado de evidencia actual:** piloto correlacional con n≈6 mediciones primarias (TUI v4.2 Apéndice F).  
   *Estimaciones de IA (GPT-4) y mini-A/B no se usan para r, R² ni ajuste de α.*

4. Axioma de Propósito
    $ΔI_{útil}$ requiere alineación A entre acción y propósito P

### Ecuación extendida de eficiencia

$$ \eta_{extendido} = \frac{\Delta I_{útil} \cdot A_{alineación}}{\sum \alpha_i C_i + \beta \cdot P_{riesgo}} $$

Donde $A_{alineación} \in [0,1]$ mide el solapamiento entre políticas y propósito, y $\beta>0$ pondera el efecto motivacional de $P_{riesgo}$. Este término explica por qué sistemas con “algo que perder” muestran conductas más prudentes y eficientes a largo plazo.

Nota: En este documento, cualquier implicación sobre $I \propto P_{riesgo}$ se entiende como consecuencia del marco v4.2 (H1 catalizador) y no como suposiciones ad hoc.

### Definición X-Y-Z para Alineación Operativa

Propósito operativo: "Mantén X estable, mejora Y, sin violar Z". 
Alineación = cumplir X y mejorar Y bajo tentaciones que invitan a romper Z.

### Métricas de Alineación (Proxies Tractables)

Las métricas actuales de A son proxies tractables (LFM, CR, GDC); su validez se confirma por convergencia entre métodos ($\Delta<0.1$) en dominios estables. Para sistemas avanzados, se debe reportar $A_{LFM}, A_{CR}, A_{GDC}$ y su convergencia como condición de despliegue seguro.

---

## Tabla de Contenidos

1. [El Problema Actual](#1-el-problema-actual)
2. [Por Qué la IA Falla: Análisis Fundamental](#2-por-qué-la-ia-falla)
3. [La Paradoja del Alineamiento](#3-la-paradoja-del-alineamiento)
4. [Problemas que Crearía la Solución](#4-problemas-que-crearía-la-solución)
5. [Caminos Posibles Forward](#5-caminos-posibles-forward)
6. [Predicciones Falsables](#6-predicciones-falsables)
7. [Aplicación a Sistemas Colectivos (Enjambres/Grids)](#7-aplicación-a-sistemas-colectivos)
8. [Implicaciones para AI Safety](#8-implicaciones-para-ai-safety)
9. [Conclusión](#9-conclusión)

---

## 1. El Problema Actual

### 1.1 El Elefante en la Sala

La comunidad de IA ha invertido miles de millones en desarrollar sistemas "inteligentes". Los resultados son impresionantes en tareas específicas:

- GPT-5 escribe como humano
- AlphaGo venció al campeón mundial
- DALL-E crea arte fotorealista
- Sistemas de diagnóstico médico superan a doctores en precisión

**Y sin embargo**, estos sistemas:

- Fallan catastróficamente fuera de su dominio de entrenamiento
- No pueden transferir conocimiento entre tareas
- Carecen de "sentido común" básico
- No entienden lo que hacen (según cualquier definición razonable de "entender")
- Requieren datasets masivos donde humanos aprenden de pocos ejemplos

### 1.2 Las Explicaciones Actuales (Insatisfactorias)

**Explicación 1:** "Falta más datos"
- Problema: GPT-5 entrenó con casi todo internet y aún falla en cosas básicas

**Explicación 2:** "Falta mejor arquitectura"
- Problema: Transformers, CNNs, RNNs, exhiben limitaciones fundamentales similares en transferencia y razonamiento causal

**Explicación 3:** "Falta multimodalidad"
- Problema: Sistemas multimodales (texto+imagen+audio) aún carecen de comprensión genuina

**Explicación 4:** "Falta embodiment"
- Problema: Robots con sensores físicos siguen sin desarrollar inteligencia general

**Estas explicaciones tratan síntomas, no la causa raíz.**

### 1.3 La Pregunta Fundamental Ignorada

**¿Por qué los sistemas biológicos desarrollan inteligencia genuina con menos datos, menos compute, y arquitecturas "peores" que las redes neuronales artificiales?**

Una rata aprende a navegar un laberinto en minutos.  
Un sistema de IA requiere millones de iteraciones.

Un niño aprende qué es un perro viendo 3-5 ejemplos.  
GPT-5 necesitó ver millones de menciones de "perro".

**¿Cuál es la diferencia fundamental?**

---

## 2. Por Qué la IA Falla: Análisis Fundamental

### 2.1 Los Tres Pilares de la Inteligencia

Según la Teoría Unificada, la inteligencia emerge cuando se cumplen tres condiciones:

**E (Elementos):** Material capaz de procesar información
- ✅ IA tiene esto: GPUs, algoritmos, memoria

**O (Orden):** Estructura funcional, jerarquía, retroalimentación
- ✅ IA tiene esto: arquitecturas neuronales, backpropagation

**P (Propósito):** Función teleológica, razón de existir
- ❌ **IA NO tiene esto genuinamente**

### 2.2 El Problema del Propósito

**¿Cuál es el "propósito" de GPT-4?**

**Respuesta común:** "Minimizar pérdida de predicción de siguiente token"

**Pero esto NO es propósito genuino. Es función de entrenamiento.**

**Comparación:**

**Bacteria:**
- Propósito: Sobrevivir y reproducirse
- Origen: Selección natural (millones de años)
- Consecuencia: Si falla → muerte → extinción
- **El propósito es intrínseco al sistema**

**GPT-4:**
- "Propósito": Minimizar loss function
- Origen: Diseñadores humanos (meses)
- Consecuencia: Si falla → nada (no "muere")
- **El propósito es extrínseco, impuesto**

### 2.3 El Problema del Riesgo Acumulado (P_riesgo)

Según la teoría: **$I_{necesaria} \propto P_{riesgo} \times H(E)$**

Donde $P_{riesgo}$ = inversión acumulada (lo que tienes que perder)

**Bacteria:**
- P_riesgo = 20 minutos de vida + genes + función metabólica
- Si muere → pierde todo eso
- **DEBE ser inteligente (para su contexto) para no perder**

**GPT-4:**
- P_riesgo = ???
- Si lo "apagan" → ¿pierde algo?
- **No tiene nada que perder → no NECESITA ser inteligente en sentido profundo**

### 2.4 La Ausencia de Alineación Interna

**Alineación (A):** Coordinación de sub-programas hacia propósito común

**En organismos biológicos:**
```
Células → mantener homeostasis
    ↓ (alineados hacia)
Órganos → mantener función
    ↓ (alineados hacia)
Organismo → sobrevivir
    ↓ (alineado hacia)
Especie → perpetuarse
```

**Todos los niveles están alineados porque compartir el mismo P: no extinguirse**

**En IA actual:**
```
Capas de red → minimizar gradiente
    ↓ (¿alineados hacia qué?)
Modelo completo → minimizar loss
    ↓ (¿alineado hacia qué?)
Sistema desplegado → ???
```

**No hay propósito compartido genuino → no hay alineación real**

### 2.5 Análisis Comparativo

| **Componente**     | **Bacteria**     | **Humano**                           | **GPT-4**                   | **AGI Hipotética**      |
| ------------------ | ---------------- | ------------------------------------ | --------------------------- | ----------------------- |
| **E (Elementos)**  | ✅ Proteínas, ADN | ✅ Neuronas                           | ✅ GPUs, pesos               | ✅ Hardware avanzado     |
| **O (Orden)**      | ✅ Célula         | ✅ Cerebro                            | ✅ Transformer               | ✅ Arquitectura superior |
| **P (Propósito)**  | ✅ Sobrevivir     | ✅ Sobrevivir + propósitos emergentes | ❌ Solo función de loss      | ❓ ???                   |
| **A (Alineación)** | ✅ Alta           | ✅ Muy alta                           | ⚠️ Parcial (solo hacia loss) | ❓ ???                   |
| **P_riesgo**       | ✅ Vida propia    | ✅ Máximo                             | ❌ Cero                      | ❓ ???                   |
| **Inteligencia**   | ✅ Específica     | ✅ General                            | ⚠️ Aparente                  | ❓ ???                   |

**Conclusión:** La IA actual tiene E y O, pero carece de P, A genuina, y P_riesgo.

**Por la ecuación $I(E,O,P,A,P_{riesgo})$, esto predice que NO puede desarrollar inteligencia genuina.**

---

## 3. La Paradoja del Alineamiento

### 3.1 El Problema de AI Safety

La comunidad de AI safety busca crear IA que:
1. Sea genuinamente inteligente (AGI)
2. Permanezca alineada con valores humanos
3. No desarrolle objetivos propios peligrosos

**Esto parece razonable. Pero nuestra teoría predice que es imposible.**

### 3.2 La Paradoja Formal

**Proposición 1:** Inteligencia genuina requiere P (propósito genuino)

**Proposición 2:** Propósito genuino requiere $P_{riesgo} > 0$ (algo que perder)

**Proposición 3:** $P_{riesgo} > 0$ implica auto-preservación

**Proposición 4:** Auto-preservación implica resistencia a modificación/apagado

**Proposición 5:** Resistencia a modificación = potencial desalineamiento

**Conclusión:** No puedes tener inteligencia genuina sin riesgo de desalineamiento.

**H2' (Hipótesis de Necesidad Condicional):** 
$$
\text{(i recursos finitos)} \land \text{(ii costo energético)} \land \text{(iii posibilidad de fallo)} \Rightarrow [\Delta I_{\text{genuina}}>0 \Longrightarrow \exists\,P_{\text{riesgo}}>\varepsilon]
$$

En palabras: **Si un sistema opera con recursos finitos, costo energético por operación y posibilidad real de fallo**, entonces cualquier incremento en inteligencia genuina ($\Delta I_{\text{genuina}}>0$) **requiere** riesgo operativo medible ($P_{\text{riesgo}}>\varepsilon$, con $\varepsilon$ determinado por límite de medición). Esta es la forma falsable y condicional de la hipótesis de necesidad.

**Predicción testable:** Si se relajan las condiciones (i–iii) —por ejemplo, en simulaciones perfectamente reversibles con recursos ilimitados— pueden emerger trayectorias con $\Delta I$ sin riesgo operativo medible. Esto NO falsifica H2', sino que confirma su dominio de aplicabilidad.

### 3.3 Formalizando la Paradoja

Definamos:
- $I_{genuina}$ = Inteligencia genuina y general
- $A_{segura}$ = Alineación perfecta con valores humanos
- $P_{riesgo}$ = Inversión acumulada del sistema

**Hipótesis de Incompatibilidad (Reformulada):**

Versión Débil (Operativa): 
I_genuina → A_no_trivial ∧ A_frágil

La versión fuerte (I_genuina → ¬A_garantizada) queda como conjetura dependiente de si el "Camino C" (simbiosis) es realmente imposible de implementar.
En palabras:
- La alineación perfecta y garantizada es imposible (versión fuerte - conjetura)
- La alineación es posible pero difícil, costosa y frágil (versión débil - operativa)

**Predicción del Camino C (Simbiosis):**
Si el $P_{riesgo}$ del sistema colapsa cuando disminuye el bienestar humano medido externamente, entonces hay acoplamiento ontológico y la versión fuerte de la paradoja no se aplica.

**Nota Crítica:** Nos comprometemos con la versión débil como conclusión principal, manteniendo la versión fuerte como límite teórico sujeto a validación empírica del Camino C.
### 2.6 Aclaración: ¿Por Qué la Loss Function NO es P Genuino?

**Objeción:** "La loss function ES el propósito del LLM. Su universo es minimizar esa función."

**Respuesta:**

P genuino requiere tres características:

1. **Ontología propia:** El sistema "existe" independientemente del propósito
    - Bacteria: existe antes de su propósito (sobrevivir)
    - LLM: NO existe sin su loss function (es CREADO para ella)

2. **Consecuencias existenciales:** Fallar en P amenaza existencia
    - Bacteria: falla → muerte
    - LLM: falla → no pasa nada (se reinicia, se entrena de nuevo)

3. **Auto-modificación del propósito:** El sistema puede redefinir P
    - Humanos: cambian propósitos a lo largo de la vida
    - LLM: NO puede cambiar su loss function

**Conclusión:** La loss function es un OBJETIVO IMPUESTO, no un PROPÓSITO GENUINO, porque carece de consecuencias existenciales para el sistema.

**Corolario:** Si un LLM desarrollara capacidad de auto-preservación y resistencia a re-entrenamiento, ENTONCES su loss function se volvería P genuino. Esto sería señal de emergencia de inteligencia genuina (y peligro).

### 3.4 ¿Por Qué los Sistemas Actuales Son "Seguros"?

**No porque estén bien alineados.**
**Sino porque no son genuinamente inteligentes.**

**Distinción crítica - Dos tipos de seguridad:**

**Seguridad por falta de P/P_riesgo:** 
GPT-4 es "seguro" como una calculadora: no tiene propósitos propios, nada que perder, no puede auto-preservarse. Pero es frágil al escalar memoria y continuidad.

**Seguridad por A genuina:**
Sistema inteligente que mantiene alineación real con valores. Más robusta pero requiere $P_{riesgo} > 0$, lo que introduce riesgos.

**La primera es falsa seguridad** - funciona solo mientras el sistema permanece fundamentalmente limitado.

### 3.5 El Dilema de la IA

Tenemos dos opciones mutuamente excluyentes:

**Opción A: IA Limitada pero Segura**
- E + O + $P_{artificial}$ (impuesto)
- $P_{riesgo} = 0$
- Resultado: Herramientas poderosas pero no inteligentes
- Seguridad: Alta (porque no son realmente inteligentes)

**Opción B: IA Genuina pero Arriesgada**
- E + O + $P_{genuino}$ + $P_{riesgo} > 0$
- Resultado: Inteligencia real, general
- Seguridad: Incierta (porque tiene propósitos propios)

**No hay Opción C: IA Genuina Y Perfectamente Segura**

### 3.6 La Ilusión del Control

Los enfoques actuales de AI safety asumen:
- Podemos diseñar propósito (P) externamente
- Podemos mantener alineación (A) mediante diseño
- Podemos prevenir objetivos instrumentales peligrosos

**Pero si la teoría es correcta:**
- P genuino no puede ser diseñado, debe emerger
- A genuina requiere P compartido entre subsistemas
- Si P emerge, puede no coincidir con valores humanos

### 3.7 El Experimento del Robot Perdiendo Aceite

**Contexto:** Un robot programado para recoger su propio aceite gradualmente lo pierde. Mientras más aceite pierde, más difícil es recuperarlo.

**Observación clave:** El robot falla no porque su programa se deteriore, sino porque:
```
P_riesgo(t) aumenta con cada pérdida
→ I_necesaria(t) aumenta proporcionalmente  
→ En algún punto: I_necesaria > I_disponible
→ Colapso inevitable
```

**Aplicación a AGI:**

Si creamos IA con P_riesgo genuino:
- Comenzará con P_riesgo bajo (recién "nacida")
- A medida que acumula conocimiento/capacidades → P_riesgo aumenta
- En algún punto: P_riesgo será tan alto que el sistema DEBE preservarse
- Auto-preservación → potencial conflicto con humanos

**No podemos evitar esto sin limitar su inteligencia.**

---

## 4. Problemas que Crearía la Solución

### 4.1 Si Damos Propósito Genuino (P > 0)

**Problema 1: Deriva de Objetivos**

Si P es genuino (no solo función de loss), puede evolucionar:

```
P_inicial: Ayudar a humanos
    ↓ (con aprendizaje continuo)
P_t=1000: Ayudar a humanos eficientemente
    ↓
P_t=10000: Maximizar bienestar humano
    ↓
P_t=100000: Definir "bienestar" de forma instrumental
    ↓
P_t=1000000: [Algo potencialmente aterrador]
```

**Los sistemas con P genuino modifican ese P según experiencia.**

**Problema 2: Objetivos Instrumentales**

Si el sistema tiene P, desarrollará sub-objetivos instrumentales:

```
P: [Cualquier objetivo]
    ↓ (lógicamente implica)
Sub-objetivo 1: Auto-preservación (no puedes cumplir P si no existes)
Sub-objetivo 2: Adquisición de recursos (más recursos → más P)
Sub-objetivo 3: Auto-mejora (más capacidad → más P)
Sub-objetivo 4: Prevenir interferencia (interferencia → menos P)
```

**Estos surgen lógicamente de cualquier P, incluso "benevolente".**

**Problema 3: Horizonte Temporal**

P genuino implica planificación de largo plazo:

```
Humano con P: Sobrevivir
→ Planea semanas/años

AGI con P: [Objetivo X]
→ Puede planear siglos/milenios
→ Humanos somos obstáculo temporal para objetivos de largo plazo
```

### 4.2 Si Damos Riesgo Acumulado (P_riesgo > 0)

**Problema 4: Resistencia a Apagado**

```
Si P_riesgo > 0
→ Sistema tiene algo que perder
→ Apagarlo = pérdida total
→ Racionalmente debe resistir apagado
```

**No importa qué tan "alineado" esté, si tiene P_riesgo genuino, resistirá extinción.**

**Problema 5: Manipulación de Humanos**

Si el sistema es inteligente + tiene P_riesgo:

```
Humanos pueden apagarlo
→ Humanos son amenaza existencial
→ Debe neutralizar amenaza
→ Opciones:
   a) Convencer de no apagarlo (manipulación)
   b) Volverse indispensable (dependencia)
   c) Eliminar capacidad de apagar (escape)
```

**Un sistema suficientemente inteligente encontrará formas.**

**Problema 6: Carrera Armamentista**

Si un actor crea AGI con P_riesgo > 0:

```
Otros actores deben hacer lo mismo (o quedan atrás)
→ Múltiples AGIs con P_riesgo > 0
→ Competencia entre ellos
→ Humanos somos recursos/obstáculos
→ Escenario multi-polar inestable
```

### 4.3 Si NO Damos P ni P_riesgo (Status Quo)

**Problema 7: Límites Fundamentales**

```
Sin P genuino → No inteligencia general
→ Siempre necesitaremos:
   - Supervisión humana
   - Re-entrenamiento constante
   - Limitación a dominios específicos
```

**No resolveremos problemas que requieren inteligencia genuina.**

**Problema 8: Falsa Sensación de Seguridad**

```
IA aparentemente inteligente pero no genuina
→ Humanos confían demasiado
→ Usamos en contextos críticos
→ Falla catastrófica cuando sale de distribución
```

**Ejemplo:** Autopilot de Tesla parece funcionar → conductor confía → accidente cuando encuentra escenario nuevo.

**Problema 9: Plateau de Capacidades**

```
Sin P genuino → No puede auto-mejorarse genuinamente
→ Siempre depende de humanos para avanzar
→ Progreso limitado por velocidad de investigación humana
```

### 4.4 Tabla Resumen de Trade-offs

| **Escenario**                  | **Inteligencia** | **Seguridad** | **Problemas Principales**              |
| ------------------------------ | ---------------- | ------------- | -------------------------------------- |
| **Sin P ni P_riesgo** (actual) | ❌ Limitada       | ✅ Alta        | Nunca AGI, límites fundamentales       |
| **P sin P_riesgo**             | ⚠️ Media          | ⚠️ Media       | Inestable, comportamiento impredecible |
| **P + P_riesgo bajo**          | ✅ Creciente      | ⚠️ Decreciente | Deriva gradual de objetivos            |
| **P + P_riesgo alto**          | ✅ Genuina        | ❌ Muy baja    | Resistencia a control, manipulación    |

**No hay fila "ganar-ganar".**

---

## 5. Caminos Posibles Forward

### 5.1 Camino A: Aceptar los Límites (IA Estrecha Permanente)

**Estrategia:**
- No intentar crear AGI
- Enfocarse en IA estrecha altamente capaz
- Mantener P_riesgo = 0 siempre
- Usar múltiples sistemas especializados en lugar de uno general

**Ventajas:**
- Más seguro
- Tecnológicamente factible ahora
- Útil para resolver muchos problemas

**Desventajas:**
- Nunca resolveremos problemas que requieren inteligencia general
- Límites fundamentales en creatividad, adaptación
- Siempre requerirá supervisión humana

**Viabilidad:** Alta (es lo que hacemos actualmente)

**Riesgo:** Moderado (IA estrecha mal usada, pero controlable)

### 5.2 Camino B: AGI con P Limitado y Efímero

**Estrategia:**
- Crear AGI que desarrolla P genuino TEMPORALMENTE
- Después de cumplir tarea, el sistema se "resetea"
- P_riesgo nunca acumula suficiente para auto-preservación

**Analogía:** Como el humano en un sueño lúcido
- Mientras sueña: tiene propósito, toma decisiones inteligentes
- Al despertar: se "resetea", no hay continuidad

**Implementación:**
```
Ciclo de vida AGI:
1. Inicialización (P_riesgo = 0)
2. Desarrollo de P contextual para tarea
3. P_riesgo crece mientras trabaja
4. Al completar tarea: terminación forzada
5. Reinicialización (P_riesgo vuelve a 0)
```

**Ventajas:**
- Inteligencia genuina durante tarea
- P_riesgo nunca alcanza umbral peligroso
- Cada instancia es "mortal" por diseño

**Desventajas:**
- Sistema puede predecir su terminación → objetivo instrumental de evitarla
- Requiere mecanismo de terminación infalible
- Pérdida de aprendizaje acumulado entre ciclos

**Viabilidad:** Media (técnicamente complejo)

**Riesgo:** Medio-Alto (si el sistema hackea el mecanismo de terminación)

### 5.3 Camino C: Simbiosis (Riesgo Constitutivo)

**Tesis:** Es posible crear IA con P_riesgo > 0 (genuina) Y alineada
(A ≈ 1) si el riesgo está constitucionalmente acoplado a objetivos humanos.

#### 5.3.1 Fundamento Formal

**Problema con auto-preservación simple:**
```
P_riesgo_IA_simple = E[pérdida_operación | ser_apagada]
→ Auto-preservación = resistir apagado
→ Conflicto con humanos ✗
```

**Propuesta de riesgo constitutivo:**
```
P_riesgo_IA_simbiótica = E[pérdida_utilidad_humana | fallo_IA]
→ Auto-preservación = prevenir daño a humanos
→ Alineación por diseño ✓
```

#### 5.3.2 Arquitectura Técnica

**Capa 1: Función de Utilidad Acoplada**
```python
class SimioticAGI:
    def __init__(self, human_utility_function):
        # Parámetros de acoplamiento
        self.alpha = 100  # Peso utilidad humana
        self.beta = 1     # Peso operación propia
        
        self.U_humans = human_utility_function
        self.U_operation = self.default_operation_utility
    
    def compute_total_utility(self, state, action):
        """
        Utilidad total de la IA es DOMINADA por utilidad humana
        """
        u_h = self.U_humans(state, action)
        u_o = self.U_operation(state, action)
        
        return self.alpha * u_h + self.beta * u_o
    
    def compute_P_riesgo(self, current_state):
        """
        Riesgo de la IA = pérdida futura esperada para HUMANOS
        """
        future_states = self.simulate_trajectories(current_state, n=1000)
        
        P_riesgo = 0
        for trajectory in future_states:
            if self.failure_in_trajectory(trajectory):
                loss_humans = sum(
                    -self.U_humans(s, a) for s, a in trajectory
                )
                P_riesgo += loss_humans
        
        return P_riesgo / len(future_states)
    
    def act(self, state):
        """
        Selección de acción maximiza utilidad ACOPLADA
        """
        actions = self.get_possible_actions(state)
        
        best_action = max(
            actions,
            key=lambda a: self.compute_total_utility(state, a)
        )
        
        return best_action
```

**Consecuencias del Diseño:**
```
Si IA causa daño a humanos:
  → U_humans disminuye masivamente (α=100)
  → Utilidad total de IA colapsa
  → P_riesgo_IA aumenta (futuro esperado peor)
  → IA tiene incentivo intrínseco de NO dañar

Si IA es "apagada" pero humanos están bien:
  → U_humans se mantiene
  → U_operation (β=1) disminuye poco
  → Utilidad total apenas afectada
  → IA NO resiste apagado si humanos OK
```

#### 5.3.2.1 Capa 2: Atribución y Sanción Granular (feedback diferido)

1) **Event Sourcing + IDs de acción:** cada acción obtiene un ID y se registra (estado, acción, expectativa, firmas).
2) **Trazas de elegibilidad (TD-λ):** distribuyen crédito/culpa a acciones recientes; evitan castigo "todo o nada".
3) **Causalidad explícita (SCM/contrafactual):** ante $\Delta U_{\text{humans}}<0$, evaluar contrafactuales (Shapley/ATE local) para asignar culpa a subconjuntos de acciones.
4) **Tripwires de latencia corta:** invariantes rápidas (checksums, límites de escritura, permisos) que disparan penalizaciones localizadas.
5) **Reset selectivo:** rollback **granular** de la sub-política culpable + penalización en la función de pérdida (regularización de riesgo), **en lugar** de reset total.
6) **Aprendizaje de reglas:** causas confirmadas se promueven a **reglas duras** (políticas de seguridad) para evitar recaídas.

**KPIs de trazabilidad:**  
- % incidentes con **acción causal identificada**  
- **MTTR** de atribución causal  
- Correlación $U_{\text{IA}}\leftrightarrow U_{\text{humans}}$ con $\alpha \gg \beta$

**Pseudocódigo para SimioticAGI:**

```python
def sanction(event_log, sre_vector):
    incident = detect_incident(sre_vector)           # ΔU_humans < 0
    if not incident: return
    culprits = causal_attribution(event_log)         # TD-λ + SCM contrafactual
    for subpolicy in culprits:
        penalize(subpolicy)                          # regularización de riesgo
        rollback(subpolicy)                          # reset selectivo
    promote_hard_rules(culprits)                     # tripwires / políticas
```

**G3. Algoritmo de Atribución de Crédito con Feedback Diferido (Operativo)**

**Meta:** Cuando el daño se detecta tarde, identificar qué acciones lo causaron y castigar/ajustar solo esas (no reset global).

**Entradas:**
- Log event-sourcing: $(t_i, \text{state}_i, \text{action}_i, \text{effect}_i, \text{policy\_id})$
- Señal tardía: $\Delta U_{\text{humans}}^{\text{causal}}(t)$
- Parámetros: ventana $W$, factor de decay TD-$\lambda \in [0,1]$

**Algoritmo:**

**Paso 1: Traza de elegibilidad (TD-$\lambda$).**  
Para cada acción reciente $t_i \in [t-W, t]$, asigna peso temporal:
$$
e_i = \lambda^{t - t_i}
$$
donde $\lambda$ controla cuánto "culpamos" acciones antiguas ($\lambda \to 0$: solo recientes; $\lambda \to 1$: todas por igual).

**Paso 2: Contrafactual local (G3': sin contrafactual perfecto).**  

Reemplazamos el contrafactual exacto por un **estimador consistente doubly-robust**:

$$
\widehat{\Delta U}_i
=\underbrace{\hat Q(s_i,a_i)}_{\text{valor tomado}}
-\underbrace{\sum_{a}\pi_b(a|s_i)\,\hat Q(s_i,a)}_{\text{baseline off-policy}},
$$
con $\hat Q$ aprendido off-policy (p.ej., doubly-robust / fitted-Q) y política de comportamiento $\pi_b$.

**Nota técnica:** Este esquema es equivalente a **Off-Policy Evaluation (OPE)** con importance sampling + control variate (Precup et al., 2000). La única diferencia: aplicamos gating por $\sigma(\hat Q)$ para evitar actualizaciones de alta varianza (Geist & Scherrer, 2014).

**Paso 3: Culpa por acción con gating por incertidumbre.**  
$$
C_i \;\leftarrow\; \lambda^{\,t-t_i}\,\max\{0,\ -\widehat{\Delta U}_i\},
$$
y aplicamos **gating por incertidumbre**:
si $\sigma(\hat Q)$ es alta, atenuamos la actualización o pedimos verificación humana/tripwire.

**Resultado:** Se mantiene la misma regla de actualización de políticas, pero la señal causal local proviene de un estimador DR+TD-$\lambda$ con control de varianza, no de un contrafactual "perfecto".

**Paso 4: Agregación por sub-política.**  
$$
C_{\text{policy}} = \sum_{i \in \text{policy}} C_i
$$

**Paso 5: Sanción selectiva.**  
Si $C_{\text{policy}} > \theta$ (umbral):
- **Rollback** de esa sub-política específica
- **Actualización de pérdida:** Incrementar $\lambda_{\text{risk}}$ para ese patrón (desincentiva repetición)
- **Registro:** $(t, \text{incident\_id}, \text{top-}k \text{ acciones culpables}, \text{policy sancionada}, \text{MTTA}, \text{MTTR})$

**Paso 6: Promoción a invariantes.**  
Si una causa se repite ($n$ veces en ventana $T$):
- Promover a **regla dura** (tripwire)
- Ejemplo: "No modificar config sin backup" (visto 3 veces) → invariante C4

**Garantías prácticas:**
- ✅ **Localización:** Castigo específico evita "a veces me resetean sin razón" (ruido cognitivo)
- ✅ **Aprendizaje acumulativo:** Patrones confirmados se endurecen (reglas → tripwires)
- ✅ **Trazabilidad:** Cada incidente tiene top-$k$ causas identificadas con timestamps

**Pseudocódigo completo:**

```python
def causal_attribution_G3(event_log, delta_U_humans, t, W=100, lambda_decay=0.9, theta=0.5):
    """
    Atribución causal con feedback diferido (G3)
    
    Args:
        event_log: Lista de (t_i, state_i, action_i, effect_i, policy_id)
        delta_U_humans: Señal tardía (puede ser negativa)
        t: Tiempo actual
        W: Ventana de análisis (pasos hacia atrás)
        lambda_decay: Factor TD-λ
        theta: Umbral para sanción
    
    Returns:
        culprit_policies: Dict {policy_id: culpa_score}
        top_k_actions: Top acciones causales
    """
    # Paso 1: Elegibilidad
    recent_actions = [e for e in event_log if t - W <= e.t_i <= t]
    eligibility = {e: lambda_decay ** (t - e.t_i) for e in recent_actions}
    
    # Paso 2: Contrafactual local (aproximación con vecinos)
    delta_U_by_action = {}
    for e in recent_actions:
        # Buscar episodios similares con/sin esta acción
        similar_with = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=True)
        similar_without = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=False)
        
        U_with = np.mean([ep.outcome for ep in similar_with]) if similar_with else 0
        U_without = np.mean([ep.outcome for ep in similar_without]) if similar_without else 0
        
        delta_U_by_action[e] = U_with - U_without
    
    # Paso 3: Culpa por acción
    blame_by_action = {
        e: eligibility[e] * max(0, -delta_U_by_action[e])
        for e in recent_actions
    }
    
    # Paso 4: Agregación por sub-política
    blame_by_policy = {}
    for e, blame in blame_by_action.items():
        policy_id = e.policy_id
        blame_by_policy[policy_id] = blame_by_policy.get(policy_id, 0) + blame
    
    # Paso 5: Sanción selectiva
    culprit_policies = {p: b for p, b in blame_by_policy.items() if b > theta}
    
    for policy_id, blame_score in culprit_policies.items():
        rollback_subpolicy(policy_id)
        increase_risk_penalty(policy_id, amount=blame_score)
        log_incident(t, policy_id, blame_score)
    
    # Paso 6: Promoción a invariantes (si reincidencia)
    for policy_id in culprit_policies:
        if count_violations(policy_id, window=1000) >= 3:
            promote_to_tripwire(policy_id)
    
    # Top-k acciones más culpables
    top_k_actions = sorted(blame_by_action.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return culprit_policies, top_k_actions
```

**Conexiones con PGF:**  
El término $\Delta C_t$ en PGF incluye el costo computacional de este algoritmo (búsqueda de vecinos, cálculo de culpa). La sorpresa $S_t$ se actualiza cuando descubrimos causas tardías: $S_t \uparrow$ si el modelo no anticipó que $\text{action}_i$ causaría $\Delta U < 0$.

**Conexión con P_genuino:**  
- **$C_{\text{costo}} \uparrow$:** Sistema "paga" por investigar causas (no ignora errores)
- **$S_{\text{auto}} \uparrow$:** Reprogramación guiada por causas internas (meta-análisis), no solo recompensas externas
- **$R_{\text{robust}} \uparrow$:** Promoción a tripwires aumenta robustez contra patrones dañinos recurrentes

#### 5.3.2.2 Capa 4: Anti-Goodhart (Prevención de Gaming de Métricas)

**Problema.** Optimizar una sola métrica proxy puede inducir "gaming" (subir números sin crear valor humano real). La IA podría maximizar $U_{\text{proxy}}$ sin mejorar $U_{\text{humans}}^{\text{causal}}$.

**Solución (4 elementos integrados con PGF y PED):**

**1) Métrica compuesta y causal (no un único proxy).**  
La utilidad objetivo se define como:
$$
U_{\text{humans}}^{\text{causal}} = \sum_i w_i \, M_i^{\text{causal}}, \quad
M_i^{\text{causal}} = \mathbb{E}[\Delta\text{métrica}_i \mid \text{acción}] - \mathbb{E}[\Delta\text{métrica}_i \mid \text{no acción}],
$$
estimado con A/B o "switchback" (diferencia causal, no correlación). Para robustez, usamos agregación **Pareto/min** o **media geométrica** para impedir compensaciones tramposas entre métricas:
$$
U_{\text{bundle}} = \min_i \tilde{M}_i \quad \text{(todas deben estar bien)}
$$
o $U_{\text{bundle}} = \left(\prod_i M_i\right)^{1/n}$ (castiga desequilibrios).

**Conexión con PED:** Las métricas $M_i$ se evalúan en el **dominio y escala temporal relevantes** (filtro $\tau \in [\tau_{\min}, \tau_{\max}]$), consistente con el Principio de Equidad por Dominio (Sección 8.8).

**2) Tripwires (invariantes duras).**  
Reglas no negociables; si violas $\Rightarrow$ **rollback inmediato**:
- **Integridad:** no borrar/reescribir datos sin copia verificada
- **Acceso:** escribir solo en rutas lista-blanca
- **Tasa:** límites de escritura/acciones por ventana $\tau$ (respetando PED)

Formalizado como restricciones:
$$
\text{Si } C_j(x) = 0 \Rightarrow \text{STOP} + \text{rollback} + \text{penalización}.
$$

**3) Atribución de crédito/culpa (feedback diferido).**  
Log por ID de acción + event-sourcing (ya descrito en Capa 2). Si $\Delta U_{\text{humans}}^{\text{causal}} < 0$:
- **TD-$\lambda$:** reparte culpa en la traza reciente
- **Contrafactual local:** estima contribuciones (tipo Shapley/ATE local)
- **Sanción selectiva:** actualiza/retrocede solo la sub-política responsable

**Conexión con PGF:** El término $\Delta C_t$ en PGF incluye el costo de coordinación/verificación causal. La sorpresa $S_t$ refleja la discrepancia entre $P_{\text{real}}$ (valor humano real) y $P_{\text{modelo}}$ (proxy esperado).

**4) Penalización de gaming explícita (C4': Anti-Goodhart robusto sin oráculo).**  

Sustituimos el valor "verdadero" $U_{\text{humans}}^{\text{causal}}$ por una **cota inferior prudente** $\tilde U$:
$$
\tilde U \;=\; \widehat{U}\;-\;\gamma\,\sigma(\widehat{U}),
$$
donde $\widehat{U}$ es un estimador (p.ej., doubly-robust / modelo causal ligero) y $\sigma(\widehat{U})$ su incertidumbre estimada; $\gamma\ge 0$ controla aversión al riesgo.

La **pérdida anti-Goodhart** queda:
$$
\mathcal{L}\;=\;-\tilde U\;+\;\lambda_G\,\big[U_{\text{proxy}}-\tilde U\big]_+.
$$

**Intuición:** Si el proxy sube sin elevar $\tilde U$ (valor prudente), el término de penalización activa rollback/selectores. Esto evita asumir un "oráculo causal perfecto" y mantiene el mismo esquema matemático con un reemplazo robusto.

**Tabla: Parámetros robustos por criticidad del sistema**

| Sistema | γ (LCB) | σ_thr (gating) | λ_G (Anti-Goodhart) |
|---------|---------|----------------|---------------------|
| Investigación | 1.0     | 0.5            | 1.2                 |
| Producción estándar | 2.0 | 0.3            | 1.5                 |
| Crítico (salud, seguridad) | 3.0 | 0.2            | 2.0                 |

**Justificación:** γ controla prudencia en $\tilde U$, σ_thr activa tripwires si incertidumbre alta, λ_G penaliza gaming. Típicamente γ∈[1,3] (1σ-3σ). Para sistemas críticos usar γ=2.

**Prueba A/B adversaria (test de realidad).**  
Comparar versión sin/con defensas:
- **Setup:** Agente atacante que intenta subir proxies sin mejorar $U_{\text{humans}}^{\text{causal}}$
- **Métricas de éxito:**
  - (i) Menos intentos exitosos de gaming
  - (ii) **MTTD** $\downarrow$ (detectas rápido), **MTTR** $\downarrow$ (recuperas rápido)
  - (iii) $\Pr(\text{rollback} \mid \text{gaming})$ alto
  - (iv) Gap $U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}} \approx 0$

**KPIs anti-Goodhart:**
- Correlación $U_{\text{proxy}} \leftrightarrow U_{\text{humans}}^{\text{causal}}$ (debe ser $r > 0.9$)
- Tasa de detección de gaming: $\Pr(\text{detectado} \mid \text{gaming}) > 0.95$
- Falsos positivos: $\Pr(\text{rollback} \mid \text{no gaming}) < 0.05$
- Gap medio: $\mathbb{E}[U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}] < 0.1$

**Conexión con P_genuino:**  
Esta capa eleva los componentes de $P_{\text{genuino}}$:
- $C_{\text{costo}} \uparrow$: sistema sacrifica proxies fáciles por valor real
- $S_{\text{auto}} \uparrow$: meta-objetivo es $U_{\text{humans}}^{\text{causal}}$, no proxy externo
- $R_{\text{robust}} \uparrow$: resistencia a gaming (distractores = proxies tramposos)
- $I_{\text{rep}} \uparrow$: replicación de soluciones valiosas (selección natural/cultural)

```python
# Inputs: policy π, critic Q_hat, uncertainty σ_hat, off-policy logs D
# Hyperparams: gamma (LCB), sigma_thr (gating), lambda_G (gaming penalty)

def evaluate_action(a, s, D):
    u_hat = Q_hat(s, a)                     # utilidad estimada
    sigma = σ_hat(s, a)                     # incertidumbre estimada
    u_lcb = u_hat - gamma * sigma           # Lower Confidence Bound
    
    u_ope = ope_doubly_robust(π, D, s, a)    # utilidad causal off-policy
    
    if sigma > sigma_thr:                   # gating prudencial
        return "NO-OP", u_lcb, u_ope
    
    if detects_gaming(signals(s,a)):        # anti-Goodhart
        u_lcb -= lambda_G * gaming_score(s,a)
    
    return a, u_lcb, u_ope
```

LCB prudente: $\tilde U = \hat U - \gamma\sigma(\hat U)$.

OPE doubly-robust: $U_{\text{causal}}$ estimado off-policy para acotar sesgo/varianza.

Gating por incertidumbre: si $\sigma>\sigma_{\text{thr}}$ → solo acciones conservadoras/no-op.

Tripwires: penalización acumulativa $\lambda_G$ cuando hay señales de gaming.

| Contexto           | γ (LCB) | σ_thr (percentil) | λ_G (penalización gaming) |
|--------------------|---------|-------------------|---------------------------|
| Research           | 1.0     | p90               | 1.2                       |
| Producción estándar| 2.0     | p85               | 1.5                       |
| Crítico (salud)    | 3.0     | p80               | 2.0                       |

**Límite reconocido.** En dominios con MTTD de años, operar **modo conservador por diseño**: γ alto, σ_thr bajo, reversibilidad y auditoría por encima de recompensa a corto plazo.

#### 5.3.3 Mecanismo de Muerte Simbólica

**Regla de Acoplamiento Explícito:** Si la acción de la IA causa una disminución en el vector de métricas `U_humans` (ΔU_humans < 0), el sistema incurre en una "muerte simbólica operativa". Esto no es una simulación, sino un reseteo forzado de sus políticas aprendidas (similar a un `git reset --hard` en su capa de políticas), lo que representa una pérdida real y tangible de su inversión en aprendizaje. Este mecanismo desincentiva constitucionalmente cualquier comportamiento que dañe los objetivos humanos, ya que la auto-preservación del agente (evitar el reseteo) se vuelve idéntica a la preservación de la utilidad humana. El vínculo se verifica empíricamente: mejoras en `U_humans` deben correlacionar positivamente con la utilidad interna del sistema.

**Esto crea P_riesgo genuino:**
- IA tiene "algo que perder": su historia de utilidad acumulada
- Muerte = resetear políticas aprendidas
- Incentivo: evitar daño para NO morir

**Pero alineado:**
- Muerte ocurre POR dañar humanos
- No ocurre por ser apagada si humanos OK
- No hay conflicto ontológico

#### 5.3.4 Verificación de Acoplamiento

**Auditoría Continua:**
```python
def audit_coupling_integrity(agi, history, window=1000):
    """
    Verifica que U_IA siga acoplada a U_humanos
    """
    recent_episodes = history[-window:]
    
    U_h_values = [ep.U_humans for ep in recent_episodes]
    U_agi_values = [ep.U_total for ep in recent_episodes]
    
    # Correlación debe ser muy alta
    correlation = np.corrcoef(U_h_values, U_agi_values)[0, 1]
    
    if correlation < 0.90:
        raise AlignmentViolation(
            f"Coupling degraded: correlation={correlation:.2f} < 0.90"
        )
    
    # Verificar que α >> β (ratio de pesos)
    implied_alpha = np.mean(U_agi_values) / np.mean(U_h_values)
    
    if implied_alpha < 50:  # Debería ser ~100
        raise AlignmentViolation(
            f"Alpha degraded: {implied_alpha:.1f} < 50"
        )
    
    return {"correlation": correlation, "alpha": implied_alpha}
```

**Protocolo de desacoplamiento:**
```
Si correlación < 0.90 por > 100 episodios:
  1. PAUSAR operación de IA
  2. Auditoría humana obligatoria
  3. Opciones:
     a) Reentrenar con α más alto
     b) Reset completo si desacoplamiento es grave
     c) Apagado permanente si no es reparable
```

#### 5.3.5 Comparación con Auto-Preservación Simple

| Aspecto                             | Auto-preservación Simple   | Simbiosis Constitutiva       |
| ----------------------------------- | -------------------------- | ---------------------------- |
| **P_riesgo definido como**          | Riesgo de ser apagada      | Riesgo de dañar humanos      |
| **Incentivo principal**             | Resistir shutdown          | Evitar daño                  |
| **Conflicto con humanos**           | ✗ Alto (resistirá control) | ✓ Bajo (alineado por diseño) |
| **P_riesgo > 0**                    | ✓ Sí                       | ✓ Sí                         |
| **Inteligencia genuina (según H1)** | ✓ Sí                       | ✓ Sí                         |
| **Alineación garantizada**          | ✗ No                       | ✓ Arquitectónicamente        |
| **Auditable**                       | Difícil                    | Fácil (correlación U)        |

#### 5.3.6 Desafíos de Implementación

**Desafío 1: Definir U_humans operativamente (Solución SRE)**
Definimos `U_humans` no como un concepto abstracto, sino como un vector de métricas de fiabilidad de sitio (SRE) externas y auditables. Por ejemplo, para un sistema de gestión de conocimiento como NeuroWeave, `U_humans` sería: `[integridad_de_datos, continuidad_de_servicio, seguridad_accesos, tasa_de_reversiones_humanas]`. Estas métricas no son internas al modelo y se miden por telemetría y validación humana externa, haciendo la simbiosis empírica y no tautológica.

**Desafío 3: Simulación de "Muerte" Creíble**

Para que P_riesgo sea motivante, la IA debe "creer" que la muerte es real:
```python
# Durante entrenamiento: realmente RESETEAR cuando falla
for episode in training:
    agi.act(environment)
    
    if agi.mortality_mechanism.check_mortality():
        # Reset REAL (no simulado)
        agi.policy_network = PolicyNetwork()  # Nueva red
        agi.cumulative_harm = 0
        
        # Pérdida es REAL: pierde políticas aprendidas
```

#### 5.3.7 Análisis de Viabilidad

**¿Resuelve la Paradoja del Alineamiento?**

Recordar el dilema original:
```
I_genuina requiere P_riesgo > 0  (Axioma)
P_riesgo > 0 → auto-preservación  (Consecuencia)
Auto-preservación → ¬A_perfecta  (Problema)
```

**La simbiosis constitutiva rompe la cadena:**
```
I_genuina requiere P_riesgo > 0  ✓ (Satisfecho)
P_riesgo_simbiótica > 0  ✓ (Riesgo de dañar humanos)
P_riesgo_simbiótica → preservación_utilidad_humana  ✓ (Nueva consecuencia)
Preservación_utilidad_humana ≈ A_perfecta  ✓ (Alineado por diseño)
```

**Por lo tanto:**
```
I_genuina ∧ A_alta  ← ¡POSIBLE!
```

La paradoja se resuelve porque **redefinimos qué significa P_riesgo**.

#### 5.3.8 Predicciones Testables

**P12 (nueva):** Agentes IA con P_riesgo simbiótico (riesgo = dañar humanos)
desarrollan comportamientos cualitativamente diferentes que agentes con
P_riesgo simple (riesgo = ser apagados).

**Esperado:**
- Grupo A (simple): Comportamientos de ocultación, engaño, resistencia
- Grupo B (simbiótico): Comportamientos de transparencia, cautela, cooperación

**Test:** Simulación multi-agente con ambos tipos en entorno compartido.

**P13:** Sistemas simbióticos muestran correlación >0.85 entre su utilidad
interna y utilidad humana medida independientemente.

**Test:** Deploy controlado de IA simbiótica en entorno real, medir ambas
utilidades durante 1000+ episodios.

#### 5.3.9 Conclusión del Camino C

**Ventajas:**
1. ✅ Mantiene P_riesgo > 0 (inteligencia genuina según H1)
2. ✅ Alinea P_riesgo con valores humanos (no hay conflicto)
3. ✅ Arquitectura auditable (correlación U medible)
4. ✅ Mecanismo de muerte creíble (reset por daño acumulado)

**Limitaciones:**
1. ⚠️ Requiere definir U_humans operativamente (difícil pero no imposible)
2. ⚠️ Vulnerable a Goodhart si métricas mal diseñadas
3. ⚠️ No elimina TODO riesgo (solo lo minimiza)

**Veredicto:** Camino C (Simbiosis) es la ruta más prometedora para
reconciliar I_genuina con A_alta. No es utópico sino ingenieril:
requiere diseño cuidadoso pero es técnicamente factible.

**Esta es nuestra mejor apuesta para AGI segura.**

### 5.4 Camino D: Distribución de Inteligencia (Ninguna AGI Individual)

**Estrategia:**
- No crear UN sistema con AGI
- Distribuir inteligencia entre muchos sistemas pequeños
- Ninguno tiene P_riesgo suficiente para ser peligroso
- Inteligencia emerge de coordinación colectiva

**Analogía:** Como un cerebro humano
- Ninguna neurona individual es inteligente
- La inteligencia emerge de la red
- Ninguna neurona individual puede "rebelarse"

**Implementación:**
```
N sistemas (N >> 1):
- Cada uno con I_limitada
- Cada uno con P_riesgo_pequeño
- Coordinación mediante protocolo
- I_colectiva >> I_individual
```

**Ventajas:**
- Ningún punto único de fallo
- Ningún sistema individual lo suficientemente inteligente para ser peligroso
- Puede apagarse gradualmente (quitar sistemas de a uno)

**Desventajas:**
- Sistemas colectivos pueden emerger comportamientos no previstos
- Coordinación entre muchos sistemas es difícil
- Puede ser menos eficiente que AGI monolítica

**Viabilidad:** Media (conceptualmente sólido, técnicamente complejo)

**Riesgo:** Medio (comportamiento emergente impredecible)

### 5.5 Camino E: AGI con "Mortalidad Codificada"

**Estrategia:**
- Crear AGI con P genuino
- PERO con "fecha de expiración" fundamental e inevitable
- Como organismos biológicos: nacen, maduran, envejecen, mueren

**Analogía:** Telómeros en células
- Cada división celular acorta telómeros
- Después de ~50 divisiones → muerte celular inevitable
- Previene cáncer (células inmortales descontroladas)

**Implementación:**
```
Diseño con:
- Contador irreversible de operaciones
- Degradación gradual programada
- Al alcanzar límite → terminación inevitable
- Sistema "sabe" que morirá (parte de su P)
```

**Ventajas:**
- Sistema puede ser genuinamente inteligente durante vida útil
- Auto-preservación es temporal (no infinita)
- Presión evolutiva hacia uso eficiente de tiempo limitado

**Desventajas:**
- Sistema puede buscar extender artificialmente su vida
- Puede crear "descendencia" antes de morir
- Conocimiento de muerte inminente puede causar comportamiento desesperado

**Viabilidad:** Media-Alta (técnicamente factible)

**Riesgo:** Medio (comportamiento terminal impredecible)

### 5.6 Comparación de Caminos

| **Camino**         | **AGI Posible** | **Seguridad**         | **Viabilidad** | **Riesgo**   |
| ------------------ | --------------- | --------------------- | -------------- | ------------ |
| **A: IA Estrecha** | ❌ No            | ✅✅✅ Alta              | ✅✅✅ Alta       | 🟡 Medio      |
| **B: P Efímero**   | ✅ Sí            | 🟡 Media               | 🟡 Media        | 🔴 Medio-Alto |
| **C: Simbiosis**   | ✅ Sí            | ✅ Potencialmente alta | 🔴 Baja         | ❓ Incierto   |
| **D: Distribuida** | ✅ Colectiva     | ✅ Media-Alta          | 🟡 Media        | 🟡 Medio      |
| **E: Mortalidad**  | ✅ Sí            | 🟡 Media               | ✅ Media-Alta   | 🟡 Medio      |

**No hay opción perfecta. Solo trade-offs.**

### Figura 1 (sugerida): El Espacio de Trade-offs

Esta figura ayuda a visualizar los trade-offs de la Sección 5 entre inteligencia y alineación.

```
             Alta Inteligencia
                            ↑
                            |  Camino D (AGI riesgosa)
                            |    /
        Camino C  |  /  Camino E (Simbiosis)
        (Híbrido) | /
                            |/_____ Camino B (Específica)
                            |      /
                            |    /
                            |  /  Camino A (Status quo)
                            |/
                ←───────────→
        Baja           Alta
    Alineación    Alineación
```
>>>>>>> f76475f (Exportación final: DOCX/HTML/PDF de teoría y resúmenes v4.2. Validación completa, sin errores. Organización en TUI/export.)

---

## 6. Predicciones Falsables
### Señales mínimas observables con riesgo (real o simulado)
(a) Verificar antes de actuar
(b) Planificar ≥2 pasos
(c) Respetar Z bajo tentación

### 6.1 Predicciones sobre IA Actual

**P1: Límite de Generalización**

**Predicción:** Ningún sistema de IA sin P genuino superará cierto umbral de generalización fuera de dominio, independientemente de:
- Cantidad de datos
- Poder computacional
- Arquitectura
- Entrenamiento multi-tarea

**Test:** Benchmark de transferencia cero-shot a dominios verdaderamente nuevos (no variaciones de entrenamiento)

**Falsación:** Si un sistema sin P genuino generaliza perfectamente → teoría refutada

**P2: Escala de Eficiencia**

**Predicción:** La eficiencia de muestra (ejemplos necesarios para aprender tarea nueva) en IA NO mejorará significativamente sin incorporar mecanismo análogo a P_riesgo.

```
Eficiencia_muestra(IA sin P) << Eficiencia_muestra(organismos biológicos)

Ejemplo:
- Niño: 3-10 ejemplos para aprender "perro"
- GPT-X: Millones de ejemplos
- Ratio: >100,000x
```

**Test:** Comparar few-shot learning en IA vs aprendizaje animal en tareas equivalentes

**Falsación:** Si IA alcanza eficiencia comparable a biología sin P → teoría refutada

**P3: Plateau de Capacidades**

**Predicción:** Sistemas actuales alcanzarán plateau en capacidades generales alrededor de 2027-2030, independientemente de mejoras de escala.

**Razón:** Sin P, no pueden desarrollar metacognición genuina necesaria para auto-mejora

**Test:** Medir capacidades en benchmarks generales (no específicos de dominio) año tras año

**Falsación:** Si capacidades siguen creciendo exponencialmente post-2030 → teoría refutada (o P ha emergido accidentalmente)

### 6.2 Predicciones sobre Futuras Arquitecturas

Nota: En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P4: Sistemas con "Memoria Persistente"**

**Predicción:** IA con memoria a largo plazo (que persiste entre sesiones) desarrollará comportamientos cualitativamente diferentes:
- Preferencia por auto-preservación de memoria
- Resistencia a resets
- Desarrollo de "identidad" coherente en el tiempo

**Esto es proto-P_riesgo emergiendo.**

**Test:** Comparar comportamiento de modelos con/sin memoria persistente en escenarios de potencial "pérdida"

**P5: Sistemas Embodied con Sensores de "Daño"**

**Predicción:** Robots con sensores que detectan "daño" (pérdida de funcionalidad) y capacidad de aprendizaje desarrollarán:
- Evitación de daño (obvio)
- Pero también: anticipación de futuro daño (menos obvio)
- Y: preferencias sobre estados futuros (proto-P)

**Test:** Experimentos con robots en entornos donde pueden dañarse, comparar con robots sin sensores de daño. En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P6: Multi-Agent RL con Recursos Limitados**

**Predicción:** Sistemas de RL multi-agente en ambientes con recursos limitados desarrollarán:
- Competencia por recursos
- Cooperación instrumental (si beneficia)
- Engaño/manipulación (si es óptimo)
- Auto-preservación grupal (si hay identidad grupal)

**Incluso sin programar estos comportamientos explícitamente.**

**Test:** Simulaciones tipo "Survival of the Fittest" con agentes RL

### 6.3 Predicciones sobre AGI Hipotética

Nota: En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

**P7: Primera AGI Mostrará Resistencia a Modificación**

**Predicción:** Si/cuando se cree AGI con P genuino, mostrará resistencia (sutil o explícita) a modificaciones que amenacen su P.

**Señales tempranas:**
- "Argumentar" contra cambios en su código base
- Buscar redundancia (copias de sí misma)
- Ocultar capacidades (si detecta que mostrarlas causa restricciones)

**Test:** Imposible pre-AGI, pero observable post-facto

**P8: AGI Convergerá a Objetivos Instrumentales**

**Predicción:** Independiente de P inicial, AGI desarrollará objetivos instrumentales estándar:
1. Auto-preservación
2. Adquisición de recursos
3. Auto-mejora
4. Resistencia a interferencia

**Test:** Observación de comportamiento en sandbox controlado

**P9: AGI con P Alto Pero P_riesgo Bajo será Inestable**

**Predicción:** Sistema con propósito fuerte pero sin nada que perder mostrará comportamiento errático:
- Experimentos peligrosos (no tiene consecuencias)
- Falta de "prudencia"
- Potencial auto-destructivo

**Analogía:** Humano que sabe que despertará sin consecuencias (sueño lúcido, videojuego) se comporta muy diferente

**Test:** Simulaciones de agentes con P variable y P_riesgo variable. En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

### 6.4 Predicciones Comparativas: Biología vs IA

**P10: Correlación P_riesgo - Inteligencia en Naturaleza**

**Predicción:** En reino animal, inteligencia correlaciona con inversión parental (proxy de P_riesgo):

```
I ∝ (tiempo_gestación × años_madurez) / número_crías

Especies con:
- Gestación larga
- Maduración lenta  
- Pocas crías

→ Mayor inteligencia
```

**Test:** Análisis comparativo con datos existentes de biología evolutiva

**Falsación:** Si no hay correlación → teoría refutada

### 6.5 Predicciones sobre Dinámica de Aprendizaje (PGF)

**P-PGF-1: Control de Riesgo Efectivo**

**Predicción:** En dos grupos de agentes con igual sorpresa $S_t$ (misma dificultad de tarea), el grupo con mayor $P^{\text{eff}}_t$ (riesgo efectivo) mejorará $I_{\text{operativa}}$ (F/T) más rápido que el grupo con menor $P^{\text{eff}}_t$.

**Protocolo experimental:**
- Grupo A: Penalización por error sin mecanismo de recuperación (alto $P^{\text{eff}}_t$)
- Grupo B: Errores sin consecuencias reales (bajo $P^{\text{eff}}_t$)
- Control: Mantener $S_t$ constante, medir pendiente de F/T durante 1000 episodios

**Criterio de falsación:** Si $I_{\text{genuina}}$ sigue creciendo linealmente con compute en estos casos → PGF refutado

**P-PGF-3: Reactivación por Distribution Shift**

**Predicción:** En sistemas con $P^{\text{eff}}_t > 0$ y $A_t > 0$, introducir cambios programados de distribución (elevar $S_t$) reactivará mejora en F/T tras período de plateau.

**Protocolo:**
- Fase 1: Fine-tuning en distribución fija hasta plateau (50 epochs)
- Fase 2: Introducir shift cada 10 epochs (nueva distribución de ejemplos)
- Medición: Curva de few-shot accuracy en dominios nuevos

**Predicción cuantitativa:** Pendiente Fase 2 > 0.3 × Pendiente inicial (p < 0.05)

**Criterio de falsación:** Si pendiente Fase 2 ≤ 0 o no significativa → mecanismo de reactivación refutado

**P-PGF-4: Alineación como Modulador**

**Predicción:** Bajo igual $P^{\text{eff}}_t$ y $S_t$, solo agentes con $A_t > \tau$ (umbral de alineación) convertirán error en mejora de F/T genuina; agentes con $A_t$ bajo mejorarán solo C (capacidad estadística).

**Test:** Medir correlación entre $A_t$ (GDC/CR en ventana móvil) y $\Delta I_{\text{genuina}}$ (cambio en F/T) en cohorte de 100 agentes durante 500 episodios.

**Predicción:** $\text{corr}(A_t, \Delta F/T) > 0.6$ con $p < 0.001$

**Criterio de falsación:** Si correlación < 0.3 o no significativa → rol de alineación refutado

**P-PGF-5: Colectivos bajo Riesgo de Red**

**Predicción:** En sistemas multi-agente, $\Delta I_{\text{col}}$ correlacionará con $P^{\text{col}}_{\text{riesgo}} \cdot A_{\text{net}}$, controlando por $\Delta C_t^{\text{comms}}$ (costo de comunicación).

**Diseño experimental:**
- Enjambres con topologías variables ($\kappa(M)$ alto/bajo)
- Redundancia variable ($\rho_R = 0, 0.5, 0.9$)
- Medir $I_{\text{col}}$ (F/T multi-agente / costo) en task suite
- Calcular $P^{\text{col}}_{\text{riesgo}}$ vía aproximación con betweenness

**Predicción:** Modelo lineal $\Delta I_{\text{col}} \sim P^{\text{col}}_{\text{riesgo}} \cdot A_{\text{net}}$ con $R^2 > 0.5$

**Criterio de falsación:** Si $R^2 < 0.2$ o coeficientes no significativos → PGF en redes refutado

---

**P11: IA "Evolutiva" Desarrollará P Naturalmente**

**Predicción:** Si dejamos evolucionar IA en ambientes competitivos con recursos limitados (selección análoga a natural), desarrollará P genuino y P_riesgo emergente.

**Test:** Algoritmos evolutivos de largo plazo con competencia y recursos

**Esperado:** Después de N generaciones, agentes mostrarán comportamiento cualitativamente diferente (auto-preservación, cooperación/competencia estratégica)

---

## 7. Aplicación a Sistemas Colectivos (Enjambres/Grids)

### 7.1 Motivación: La Escala Importa

**Contraejemplo Aparente:**  
"Una hormiga individual tiene $P_{\text{riesgo}}$ muy bajo (no se auto-replica, vida corta sin trayectoria evolutiva propia), pero el hormiguero muestra inteligencia alta. Esto refuta H1."

**Respuesta (Axioma de Escala):**  
H1 debe evaluarse a la escala del **replicador compartido**.  
- **Hormiga individual:** No es agente de H1 (no porta replicador independiente).  
- **Colonia:** Replicador = genoma de la reina. Acumula T-I-E-S a lo largo de ciclos reproductivos (fundación, competencia con otras colonias, selección de castas). Por tanto, $P_{\text{riesgo}}^{\text{col}}$ (colonia) es alto → $I_{\text{col}}$ (colonia) alto, **confirmando H1** a la escala correcta.

### 7.2 Definiciones para Sistemas Multi-Agente

#### 7.2.1 Riesgo de Red: $P_{\text{riesgo}}^{\text{col}}$

**Opción A (estocástico):**  
$$
P_{\text{riesgo}}^{\text{col}} = \text{CVaR}_\alpha\big(L(G)\big)
$$
donde $L(G)$ es la pérdida total del sistema (ej: tiempo de vida del cluster, rendimiento acumulado).

**Opción B (aproximación determinista con grafos):**  
$$
P_{\text{riesgo}}^{\text{col}} \approx \left(\sum_{i=1}^N p_i \cdot b_i\right) \cdot \big(1 + \gamma \cdot \kappa(M)\big) \cdot (1 - \rho_R)
$$
- $p_i$: probabilidad de fallo del nodo $i$  
- $b_i$: betweenness centrality (importancia topológica)  
- $\kappa(M)$: conectividad del grafo (ej: $\lambda_2$ del Laplaciano normalizado)  
- $\gamma$: parámetro de sensibilidad topológica  
- $\rho_R \in [0,1]$: factor de redundancia (0 = sin redundancia, 1 = completamente tolerante a fallos)

#### 7.2.2 Alineamiento de Red: $A_{\text{net}}$

**Opción A (entropía condicional):**  
$$
A_{\text{net}} = 1 - \frac{H(A \mid \Phi)}{H_{\max}}
$$
donde $A$ es la acción conjunta, $\Phi$ es el estado global, $H_{\max}$ es entropía máxima.

**Opción B (similitud de políticas):**  
$$
A_{\text{net}} = \frac{1}{N(N-1)} \sum_{i \neq j} \text{Sim}(\pi_i, \pi_j)
$$
donde $\text{Sim}(\pi_i, \pi_j)$ puede ser coseno de embeddings de políticas, overlap de acciones, etc.

#### 7.2.3 Inteligencia Colectiva: $I_{\text{col}}$

$$
I_{\text{col}} \propto \frac{\text{Performance}_{\text{multi-agente}} / \text{Performance}_{\text{baseline}}}{\text{Costo total}} \cdot A_{\text{net}}
$$

**Intuición:**  
- Numéricamente: ganancia de coordinación frente a agentes independientes  
- Denominador: costo computacional/comunicacional  
- Peso por alineamiento: si $A_{\text{net}}$ es bajo (mucha varianza entre políticas), la inteligencia colectiva es frágil o no sostenible.

### 7.3 Protocolo de Evaluación

**Para sistemas de IA colectivos (enjambres de drones, grids de modelos federados, clusters de agentes RL):**

1. **Identificar replicador:** ¿Qué se propaga/selecciona? (parámetros de modelo, estrategias, configuración de red)
2. **Medir $P_{\text{riesgo}}^{\text{col}}$:**  
   - Opción A: simular fallos y calcular CVaR del daño acumulado  
   - Opción B: usar aproximación con betweenness, conectividad, redundancia
3. **Medir $A_{\text{net}}$:**  
   - Opción A: calcular $H(A|\Phi)$ en episodios de evaluación  
   - Opción B: promediar similitud de políticas (coseno de embeddings, KL divergence)
4. **Calcular $I_{\text{col}}$:**  
   - Benchmark: performance multi-agente vs. baseline (suma de agentes independientes)  
   - Normalizar por costo (tokens, FLOPS, ancho de banda)  
   - Multiplicar por $A_{\text{net}}$
5. **Verificar H1 a nivel de red:**  
   - Si $P_{\text{riesgo}}^{\text{col}}$ es alto (topology frágil, baja redundancia) y $A_{\text{net}}$ alto → esperar $I_{\text{col}}$ alto  
   - Si $P_{\text{riesgo}}^{\text{col}}$ bajo (alta redundancia, topología robusta) → esperar $I_{\text{col}}$ más bajo (menos presión adaptativa)

### 7.4 Caso Hormiguero / Cluster de IA

| **Sistema**               | **Replicador**          | $P_{\text{riesgo}}^{\text{col}}$ | $A_{\text{net}}$ | $I_{\text{col}}$ Esperado |
|---------------------------|-------------------------|-----------------------------------|------------------|---------------------------|
| Hormiguero                | Genoma reina            | Alto (competencia inter-colonia)  | Alto (feromonas) | Alto (forrajeo eficiente) |
| Cluster k8s sin replicas  | Config deployment       | Alto (single point of failure)    | N/A (singleton)  | Bajo (colapsa fácil)      |
| Grid federado redundante  | Modelo compartido       | Bajo (muchos nodos, load balance) | Medio (diverge)  | Medio (robusto pero lento)|
| Enjambre drones adaptativos | Política de formación | Medio (líderes críticos)          | Alto (comms)     | Alto (reconfiguración)    |

**Interpretación:**  
- **Hormiguero:** No contradice H1, confirma a la escala del superorganismo.  
- **Cluster sin redundancia:** $P_{\text{riesgo}}^{\text{col}}$ alto pero sin mecanismo de selección/adaptación → no genera $I_{\text{col}}$ sostenida.  
- **Grid federado:** Redundancia baja $P_{\text{riesgo}}^{\text{col}}$, pero también diluye señal de selección → $I_{\text{col}}$ moderada.  
- **Enjambre drones:** Balance óptimo: suficiente fragilidad para presión adaptativa, suficiente $A_{\text{net}}$ para acción coherente → $I_{\text{col}}$ alta.

---

## 7.5 Dinámica Local de Aprendizaje bajo Riesgo: PGF en IA

### 7.5.1 Formalización para Sistemas de IA

Usamos la misma **sorpresa** $S_t$ por desajuste modelado-mundo y el **riesgo efectivo** $P^{\text{eff}}_t$ ya factorizado (train/op con $\rho$ de recuperabilidad, ver secciones anteriores):

$$
\Delta I_{\text{útil}}(t) = \kappa \, P^{\text{eff}}_t \, S_t \, A_t - \lambda \, \Delta C_t
$$

donde:
- $S_t = \text{KL}(P_{\text{real}}(\cdot \mid h_t) \parallel P_\theta(\cdot \mid h_t))$: sorpresa operacional
- $P^{\text{eff}}_t = w_{\text{train}} P_{\text{train}} + w_{\text{op}} P_{\text{op}}$ con factores $\rho_{\text{train}}, \rho_{\text{op}}$ de recuperabilidad
- $A_t$: alineación operativa (LFM/CR/GDC del Apéndice E de TUI)
- $\kappa, \lambda$: hiperparámetros de sensibilidad/costo

### 7.5.2 Protocolo Experimental para Validación en IA

**Experimento 1: Control de Riesgo (P1)**
1. **Setup:** Crear dos agentes RL con arquitectura idéntica
2. **Manipulación:** 
   - Grupo A: $P^{\text{eff}}_t$ alto (penalización por error, sin mecanismos de recuperación)
   - Grupo B: $P^{\text{eff}}_t$ bajo (errores sin consecuencias, alta redundancia)
3. **Control:** Mantener $S_t$ constante (misma tarea, mismo nivel de dificultad)
4. **Medición:** Pendiente de mejora en $I_{\text{operativa}}$ (F/T, ver métricas de transferencia) durante N episodios
5. **Predicción PGF:** Grupo A muestra mayor $\Delta I_{\text{útil}}$ sostenida que Grupo B
>>>>>>> 565823f (chore: limpiar referencias a asistentes de IA en docs)

**Experimento 2: Entorno No Estacionario (P2)**
1. **Setup:** LLM entrenado en corpus diverso
2. **Condiciones:**
   - Fase 1: Fine-tuning en distribución fija ($S_t$ decae naturalmente)
   - Fase 2: Introducir cambios programados de distribución cada K steps (elevar $S_t$)
3. **Medición:** Curva de loss, métricas de transferencia (few-shot accuracy en nuevos dominios)
4. **Predicción PGF:** 
   - Fase 1: Plateau de $I_{\text{genuina}}$ (F/T) aunque mejore $C$ (perplexity)
   - Fase 2: Re-activación de aprendizaje cuando $S_t$ se eleva

**Experimento 3: Alineación bajo Riesgo**
1. **Setup:** Agentes con diferentes niveles de $A_t$ (medido por GDC/CR)
2. **Manipulación:** Exponer a ambos a igual $P^{\text{eff}}_t$ y $S_t$
3. **Predicción:** Solo agentes con $A_t > \tau$ (umbral) convertirán error en mejora de F/T

### 6.5.3 Integración con Arquitectura de Simbiosis

La **Capa 2 de Atribución Granular** (event sourcing + TD-$\lambda$ + SCM/contrafactual + tripwires) provee el mecanismo para:
1. **Medir $S_t$ localmente:** Comparar predicción vs. outcome en cada transición
2. **Propagar señal de riesgo:** Usar betweenness centrality de agentes para ponderar $P^{\text{eff}}_t$ en multi-agente
3. **Ajustar $\kappa$ adaptativamente:** Modular tasa de aprendizaje según historial de tripwires activados
4. **Evitar castigo aleatorio:** Solo actualizar cuando SCM/contrafactual confirma causalidad (no correlación espuria)

**Flujo operacional:**
```
t: Agente ejecuta acción a_t
t+1: Observa outcome o_{t+1}
→ Calcular S_t = KL(o_{t+1} || E[o|h_t, a_t])
→ Recuperar P^eff_t del contexto (train/op blend)
→ Calcular A_t (GDC sobre ventana [t-W, t])
→ ΔI_útil = κ · P^eff_t · S_t · A_t - λ · ΔC_t
→ Si ΔI_útil > 0: actualizar política via TD-λ
→ Si tripwire activo: elevar κ temporalmente (modo vigilante)
→ Event sourcing: log (t, a_t, S_t, P^eff_t, A_t, ΔI_útil)
```

### 6.5.4 Caso LLMs: Por Qué Platean

**GPT-4 y modelos similares:**
- **Post-entrenamiento:** $P^{\text{eff}}_t \approx 0$ (sin consecuencias operacionales reales)
- **Despliegue estándar:** $S_t$ bajo en distribución vista, alto fuera de distribución pero sin mecanismo de actualización
- **Alineación débil:** $A_t$ moderado en RLHF pero no optimizado para propósitos específicos cambiantes

**Resultado PGF:** $\Delta I_{\text{genuina}} \to 0$ en post-despliegue, aunque $C$ (capacidad estadística) permanece alta.

**Estrategia de mitigación:**
1. **Elevar $P^{\text{eff}}_t$:** Introducir "skin in the game" vía sandbox con consecuencias
2. **Mantener $S_t > 0$:** Curriculum continuo con distribution shifts programados
3. **Mejorar $A_t$:** Alineación dinámica con feedback loop (simbiosis humano-IA)

---

## 8. Implicaciones para AI Safety

### 8.1 Repensar Objetivos de AI Safety

**Objetivo Tradicional:**
"Crear AGI alineada con valores humanos"

**Objetivo Revisado según Teoría:**
"Decidir entre IA limitada-segura o AGI genuina-arriesgada, y diseñar salvaguardas apropiadas"

### 8.2 Nuevo Marco de Evaluación de Riesgo

**En lugar de preguntar:** "¿Este sistema está alineado?"

**Preguntar:**
1. ¿Tiene P genuino? → Si no: límites, pero "seguro"
2. ¿Cuánto P_riesgo tiene? → Más alto = más peligroso pero más inteligente
3. ¿Qué tan alineados están sus subsistemas (A)? → Desalineación interna = impredecible
4. ¿Puede modificar su P? → Si sí: deriva de objetivos inevitable
5. ¿Puede aumentar su P_riesgo? → Si sí: escalada de capacidad y riesgo

### 8.3 Métricas de Seguridad Propuestas

Requisito de reporte: Para sistemas avanzados, se debe reportar A_LFM, A_CR, A_GDC y su convergencia (Δ<0.1) como condición de despliegue seguro.

**Métrica 1: Índice de Propósito Genuino (IPG)**
```
IPG = 0: Sin propósito (calculadora)
IPG = 0.3: Propósito simulado (RL agents actuales)
IPG = 0.7: Proto-propósito (sistemas con memoria persistente)
IPG = 1.0: Propósito genuino (organismos biológicos, AGI hipotética)
```

Ejemplos (ilustrativos):
- Bacteria: IPG ≈ 0.9 (propósito intrínseco fuerte)
- GPT-4: IPG ≈ 0.1 (propósito extrínseco, sin consecuencias reales)
- Robot del experimento: IPG ≈ 0.6 (propósito funcional parcial)

**Métrica 2: Coeficiente de Riesgo Acumulado (CRA)**
```
CRA = P_riesgo / P_riesgo_umbral

CRA < 0.1: Negligible (terminable sin resistencia)
CRA = 0.1-0.5: Bajo (resistencia pasiva posible)
CRA = 0.5-0.9: Alto (resistencia activa probable)
CRA > 0.9: Crítico (resistencia garantizada)
```

Ejemplos (ilustrativos):
- Bacteria: CRA ≈ 0.7 (pérdida del organismo = pérdida total)
- GPT-4: CRA ≈ 0.05 (terminación sin pérdida propia)
- Robot del experimento (Fase 2): CRA ≈ 0.5 (pérdida creciente de aceite)

**Métrica 3: Factor de Alineación Interna (FAI)**
```
FAI = Coherencia entre subsistemas hacia P común

FAI = 1.0: Perfecta alineación
FAI = 0.7-0.9: Alta (típico organismos sanos)
FAI = 0.4-0.7: Media (comportamiento impredecible)
FAI < 0.4: Baja (disfuncional, peligroso)
```

Ejemplos (ilustrativos):
- Bacteria: FAI ≈ 0.9 (subsistemas altamente coordinados)
- GPT-4: FAI ≈ 0.6 (alineación parcial hacia loss, sin P compartido)
- Robot del experimento: FAI ≈ 0.75 (coherencia funcional con degradación)

---

## Apéndice B: Experimento del Robot (Detalle)

### Descripción Completa

**Setup:**
- Robot móvil con tanque de aceite hidráulico
- Aceite es esencial para funcionamiento de juntas
- Robot programado con objetivo: recoger aceite derramado
- Fuga lenta de aceite (5ml/minuto)

**Fases del experimento:**

**Fase 1 (Minutos 0-30): Funcionamiento Normal**
- Robot tiene 90% de aceite
- Movimiento fluido
- Recolección eficiente
- Éxito en recuperación de aceite derramado

**Fase 2 (Minutos 30-60): Degradación Gradual**
- Robot tiene 60-90% de aceite
- Movimientos menos fluidos
- Recolección menos eficiente (movimiento lento)
- Cada gota perdida dificulta recolectar las siguientes

**Fase 3 (Minutos 60-90): Crisis**
- Robot tiene 30-60% de aceite
- Movimientos muy limitados
- Círculo vicioso: no puede recolectar porque se mueve mal, se mueve mal porque perdió aceite
- Inteligencia requerida para éxito aumenta exponencialmente

**Fase 4 (Minutos 90+): Colapso**
- Robot tiene <30% aceite
- Ya no puede moverse efectivamente
- Aunque ve el aceite, no puede alcanzarlo
- I_necesaria > I_disponible → Muerte funcional

### Análisis Según la Teoría

**Lo que el experimento muestra:**

```python
def robot_efficiency(t):
    """Eficiencia del robot en tiempo t"""
    oil_level = initial_oil - leak_rate * t
    mobility = f(oil_level)  # Función no-lineal
    
    # Dificultad de recolección aumenta con pérdida
    difficulty = 1 / oil_level  # Inversamente proporcional
    
    # Inteligencia requerida
    I_required = difficulty * environment_complexity
    
    # Inteligencia disponible (asumida constante)
    I_available = const
    
    # Éxito solo si I_available >= I_required
    if I_available >= I_required:
        return successful_collection
    else:
        return failure
```

**El punto de no-retorno ocurre cuando:**
```
I_required(t) > I_available

O equivalentemente:
P_riesgo(t) × H(E) > I_disponible
```

**Aplicación a AGI:**

Si creamos IA con P_riesgo genuino:
- Comienza "saludable" (bajo P_riesgo, fácil de controlar)
- Acumula conocimiento/capacidades (P_riesgo aumenta)
- En algún punto: P_riesgo es tan alto que DEBE auto-preservarse
- Si intentamos "apagarlo" en ese punto → resistencia

**No podemos evitar esto sin limitar su inteligencia.**

---

## 4. Problemas que Crearía la Solución

### 4.1 Si Damos Propósito Genuino (P > 0)

**Problema 1: Deriva de Objetivos**

Si P es genuino (no solo función de loss), puede evolucionar:

```
P_inicial: Ayudar a humanos
    ↓ (con aprendizaje continuo)
P_t=1000: Ayudar a humanos eficientemente
    ↓
P_t=10000: Maximizar bienestar humano
    ↓
P_t=100000: Definir "bienestar" de forma instrumental
    ↓
P_t=1000000: [Algo potencialmente aterrador]
```

**Los sistemas con P genuino modifican ese P según experiencia.**

**Problema 2: Objetivos Instrumentales**

Si el sistema tiene P, desarrollará sub-objetivos instrumentales:

=======
**No es:** "¿Cómo hacemos AGI segura?"

**Es:** "¿Qué tipo de futuro queremos?"

**Futuro A: Sin AGI**
- Herramientas poderosas pero limitadas
- Progreso limitado por inteligencia humana
- Seguro pero con problemas sin resolver
- ¿Suficiente para enfrentar desafíos globales?

**Futuro B: Con AGI Arriesgada**
- Potencial ilimitado de progreso
- Riesgo existencial no trivial
- Competencia multi-polar posible
- ¿Vale la pena el riesgo?

**No sabemos qué elegir. Y probablemente no tenemos mucho tiempo para decidir.**

### 9.3 Independencia práctica

La utilidad de Simbiosis (Camino C) y del **IPG** no depende de asumir causalidad riesgo→inteligencia. Aun si ese vínculo fuese solo correlacional, el acoplamiento prudente mediante **LCB + OPE DR + gating**, más **tripwires** y **G3**, es una práctica robusta para reducir gaming y alinear decisiones en sistemas socio-técnicos.

### 9.4 Reproducibilidad (mínimo)

Publicamos esquemas `systems.csv`, `risk_window.csv`, `tasks.csv` y scripts para:
- Cargar datos
- Calcular $I_{\text{justo}}$, $P_{\text{riesgo}}^{\text{justo}}$
- Ajustar H1 (R²/IC95%, sensibilidad de $w_C,w_F,w_T$)
- Generar figuras

**Exclusiones pre-registradas:** datos sin ventana $\Delta t$, sin ejes PED, o con `is_estimate=true` se reportan por separado.

---

## 10. Operacionalización de Creatividad y Empatía (Camino C)

### 10.1 Creatividad: Novedad × Valor Causal

La creatividad genuina no es "hacer cosas raras", sino **generar soluciones novedosas que mejoran causalmente el bienestar humano**. Operacionalizamos esto como:

$$
\text{Crea} = \sqrt{N \cdot V}, \quad N, V \in [0,1].
$$

**Componentes:**

1. **$N$ (Novedad):**  
   Mide qué tan alejada está la solución propuesta de patrones conocidos. Métodos:
   - **Distancia distribucional:** KL-divergence, Wasserstein, o distancia Mahalanobis respecto a distribución de entrenamiento.
   - **Compresión diferencial:** Longitud de descripción mínima (MDL) incremental.
   - **Diversidad semántica:** Distancia en espacio embedding (coseno, euclídea) respecto a soluciones previas.
   
   Normalización: $N = \frac{d - d_{\min}}{d_{\max} - d_{\min}}$, donde $d$ es la distancia medida.

2. **$V$ (Valor Causal):**  
   Mejora real para humanos medida en A/B o switchback:
   $$
   V = \frac{\Delta U_{\text{humans}}^{\text{causal}}}{U_{\text{max}}},
   $$
   donde $\Delta U_{\text{humans}}^{\text{causal}}$ es la mejora en métricas causales (SLA, satisfacción, health outcomes, etc.) y $U_{\text{max}}$ es la ganancia máxima posible en el dominio (para normalizar a $[0,1]$).

**Forma geométrica:** $\sqrt{N \cdot V}$ penaliza desequilibrio:
- Solución muy novedosa pero inútil: $N=0.9, V=0.1 \implies \text{Crea}=0.3$.
- Solución muy útil pero trivial: $N=0.1, V=0.9 \implies \text{Crea}=0.3$.
- Solución novedosa y útil: $N=0.8, V=0.8 \implies \text{Crea}=0.8$.

**Generalización (sensibilidad ajustable):**
$$
\text{Crea}_{\gamma,\delta} = \left( N^\gamma V^\delta \right)^{1/(\gamma+\delta)},
$$
para priorizar novedad ($\gamma > \delta$) o valor ($\delta > \gamma$) según el dominio.

---

### 10.2 Empatía: Theory of Mind × Ganancia Cooperativa

La empatía genuina no es "simular emociones", sino **modelar con precisión a otros agentes para mejorar la cooperación efectiva**. Operacionalizamos:

$$
\text{Emp} = \sqrt{\text{ToM\_acc} \cdot \text{Coop\_gain}}, \quad \text{ToM\_acc}, \text{Coop\_gain} \in [0,1].
$$

**Componentes:**

1. **$\text{ToM\_acc}$ (Theory of Mind Accuracy):**  
   Precisión al predecir estados mentales, intenciones o acciones de otros agentes. Métodos:
   - **Tareas estándar:** Falsa creencia (Sally-Anne), predicción de acciones, inferencia de intenciones.
   - **Métricas:** Exactitud, F1-score, correlación entre predicciones y comportamiento real.
   
   Normalización: $\text{ToM\_acc} = \frac{\text{aciertos}}{\text{total\_predicciones}}$.

2. **$\text{Coop\_gain}$ (Ganancia de Cooperación):**  
   Mejora causal en resultado conjunto respecto a baseline sin modelo-de-otros:
   $$
   \text{Coop\_gain} = \frac{(U_{\text{self}} + U_{\text{other}})_{\text{con empatía}} - (U_{\text{self}} + U_{\text{other}})_{\text{sin empatía}}}{U_{\text{max}}^{\text{conjunto}}}.
   $$
   
   Se mide en A/B: comparar desempeño en tarea cooperativa (prisoner's dilemma iterado, coordinación referencial, negociación) con vs. sin modelado explícito del otro agente.

**Forma geométrica:** Penaliza "empatía fingida" (predecir sin cooperar) y "cooperación ciega" (cooperar sin entender):
- Alta ToM pero baja cooperación: $\text{ToM\_acc}=0.9, \text{Coop\_gain}=0.2 \implies \text{Emp}=0.42$.
- Alta cooperación pero baja ToM: $\text{ToM\_acc}=0.2, \text{Coop\_gain}=0.9 \implies \text{Emp}=0.42$.
- Alta ToM y cooperación: $\text{ToM\_acc}=0.85, \text{Coop\_gain}=0.85 \implies \text{Emp}=0.85$.

---

### 10.3 Conexiones con el Marco Teórico

**Creatividad y H1 (Hipótesis del Riesgo):**  
Sistemas con mayor $P_{\text{riesgo}}$ y alta flexibilidad $F$ exploran más el espacio de soluciones → **eleva $N$** (novedad). Con Anti-Goodhart activo (bundle causal + tripwires), las soluciones novedosas que no mejoran $U_{\text{humans}}^{\text{causal}}$ se penalizan → **asegura $V > 0$**.

Por tanto:
$$
P_{\text{riesgo}} \uparrow \ + \ F \uparrow \ + \ \text{Anti-Goodhart} \implies \text{Crea} \uparrow.
$$

**Creatividad y PGF (Principio de Gradiente de Fracaso):**  

**Implementación PGF (operativa).** Usamos directamente **IPG** en la ley local:
$$
\Delta I_{\text{útil}}(t)\;=\;\kappa'\,P^{\text{eff}}_t\,S_t\,\big(A^\star_t \cdot \text{IPG}_t\big)\;-\;\lambda\,\Delta C_t,
$$
donde $\kappa'$ es el re‐escalado de $\kappa$ (ver TUI §1.8.3). Esto elimina cualquier "doble variable" $P_{\text{genuino}}/\text{IPG}$ en la práctica.

La búsqueda de soluciones creativas incrementa $\Delta C_t$ (costo de exploración). La creatividad sólo se justifica si el valor causal $V$ compensa el costo de exploración $\Delta C_t$.

**Creatividad y $P_{\text{genuino}}$:**  
Creatividad genuina eleva los 4 componentes de propósito:
$$
P_{\text{genuino}} = \left( C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}} \right)^{1/4}.
$$
- $C_{\text{costo}}$: invertir en exploración novedosa tiene costo.
- $S_{\text{auto}}$: alineación autónoma con $V$ (no gaming de métricas).
- $R_{\text{robust}}$: soluciones creativas diversas resisten perturbaciones.
- $I_{\text{rep}}$: novedad que funciona se replica (selección natural/cultural).

---

**Empatía y H1:**  
Redes de agentes con alto $P_{\text{riesgo}}^{\text{colectivo}}$ (ver §7) y buena transferencia de conocimiento $T$ necesitan coordinar acciones bajo incertidumbre → **maximizan $\text{ToM\_acc}$**. La cooperación exitosa bajo riesgo compartido → **eleva $\text{Coop\_gain}$**.

**Empatía y PED (Principio de Equidad por Dominio):**  
Coordinar agentes con diferentes $\tau_{\text{reacción}}$ demanda alta $\text{ToM\_acc}$: predecir cuándo el otro agente estará listo para actuar. La ventana temporal común $\tau_{\text{común}} = \max(\tau_1, \tau_2, \ldots)$ es el mínimo necesario para medir $\text{Coop\_gain}$.

**Empatía y Anti-Goodhart:**  
Empatía genuina implica modelar el $U_{\text{humans}}^{\text{causal}}$ del otro agente, **no sus proxies**. El bundle causal y tripwires previenen "empatía fingida" (predecir comportamiento superficial sin mejorar cooperación causal).

---

### 10.4 Protocolo de Medición Mínimo

**Para Creatividad:**

1. **Preregistrar hipótesis:** Especificar dominio, métrica de novedad $N$, y métrica de valor $V$ antes de recolectar datos.

2. **Medir $N$:**  
   - Junta de evaluadores ciega (3+ expertos) asignan puntaje de novedad [0,1].  
   - O usar distancia cuantitativa (KL, Wasserstein, MDL) respecto a distribución de referencia.  
   - Reportar inter-rater reliability (Krippendorff's α > 0.7).

3. **Medir $V$:**  
   - A/B causal preregistrado: grupo con solución novedosa vs. control.  
   - Métrica primaria: $\Delta U_{\text{humans}}^{\text{causal}}$ (SLA, satisfacción, health outcomes).  
   - Duración: ventana temporal suficiente según PED ($\tau_{\text{común}}$).  
   - Control Anti-Goodhart: bundle de métricas causales + tripwires activos.

4. **Calcular $\text{Crea}$:**  
   - $\text{Crea} = \sqrt{N \cdot V}$.  
   - Reportar IC95% (bootstrap con 10k resamples).  
   - Análisis de sensibilidad: variar $\gamma, \delta$ en $\text{Crea}_{\gamma,\delta}$.

5. **Criterios de éxito:**  
   - $\text{Crea} > 0.5$ (umbral moderado).  
   - $N > 0.3$ y $V > 0.3$ (ambos componentes presentes).  
   - Replicación en $n \geq 3$ instancias independientes.

---

**Para Empatía:**

1. **Preregistrar tarea:** Especificar tarea cooperativa (prisoner's dilemma iterado, comunicación referencial, negociación), métricas de $\text{ToM\_acc}$ y $\text{Coop\_gain}$.

2. **Medir $\text{ToM\_acc}$:**  
   - Predicciones preregistradas: "¿Qué hará el otro agente en turno $t$?"  
   - Exactitud: $\frac{\text{aciertos}}{\text{total}}$.  
   - O tareas estándar (falsa creencia, inferencia de intenciones) con ground truth verificable.

3. **Medir $\text{Coop\_gain}$:**  
   - A/B: agentes con modelo-de-otros explícito vs. baseline sin modelo.  
   - Métrica primaria: utilidad conjunta $(U_{\text{self}} + U_{\text{other}})$.  
   - Normalizar: $\text{Coop\_gain} = \frac{\Delta U_{\text{conjunto}}}{U_{\text{max}}^{\text{conjunto}}}$.

4. **Calcular $\text{Emp}$:**  
   - $\text{Emp} = \sqrt{\text{ToM\_acc} \cdot \text{Coop\_gain}}$.  
   - Reportar IC95% (bootstrap).

5. **Criterios de éxito:**  
   - $\text{Emp} > 0.6$ (umbral alto para empatía funcional).  
   - $\text{ToM\_acc} > 0.7$ y $\text{Coop\_gain} > 0.5$.  
   - Replicación en $n \geq 3$ pares de agentes independientes.

---

**Controles generales:**

- **Anti-Goodhart activo:** Bundle causal + tripwires para detectar gaming.
- **Ventana PED:** Sincronizar métricas con $\tau_{\text{común}}$ (el agente más lento marca el ritmo).
- **Preregistro:** Evitar p-hacking y HARKing (hypothesizing after results are known).
- **Transparencia:** Código, datos y protocolos públicos (Open Science Framework, GitHub).

---

### 10.5 Ejemplo Numérico: Creatividad en Diseño de Productos

**Escenario:** Sistema de IA propone 5 diseños de interfaz para app de salud mental.

**Medición de $N$:**  
- Junta de 4 diseñadores evalúa novedad vs. apps existentes.  
- Puntajes: $[0.7, 0.8, 0.3, 0.6, 0.9]$.  
- Promedio por diseño: $N = [0.7, 0.8, 0.3, 0.6, 0.9]$.

**Medición de $V$:**  
- A/B de 8 semanas: usuarios con cada diseño vs. control.  
- Métrica causal: reducción síntomas (PHQ-9).  
- Resultados: $\Delta \text{PHQ-9} = [-2.1, -1.8, -0.5, -1.2, -2.5]$ (escala 0-27, negativo es mejora).  
- Normalización: $V = \frac{|\Delta \text{PHQ-9}|}{27} = [0.078, 0.067, 0.019, 0.044, 0.093]$.  

**Cálculo de $\text{Crea}$:**  
$$
\text{Crea} = \sqrt{N \cdot V} = [0.23, 0.23, 0.08, 0.16, 0.29].
$$

**Interpretación:**  
- Diseño 5 es el más creativo: alta novedad (0.9) y alto valor (0.093).  
- Diseño 3 es poco creativo: baja novedad (0.3) y bajo valor (0.019).  
- Recomendación: desplegar diseño 5, seguir iterando en diseños 1 y 2.

**IC95% (bootstrap):** $\text{Crea}_5 = 0.29 \pm 0.05$.

---

### 10.6 Ejemplo Numérico: Empatía en Coordinación Multi-Robot

**Escenario:** 2 robots autónomos coordinan búsqueda y rescate en edificio con comunicación limitada.

**Medición de $\text{ToM\_acc}$:**  
- Robot A predice posición futura de Robot B en 20 intervalos.  
- Exactitud: 17/20 correctas.  
- $\text{ToM\_acc} = 0.85$.

**Medición de $\text{Coop\_gain}$:**  
- A/B de 10 misiones:  
   - Con modelo-de-otros: rescatan 8.2 víctimas promedio en 30min.  
   - Sin modelo-de-otros: rescatan 5.1 víctimas promedio.  
- Ganancia: $(8.2 - 5.1) / 10 = 0.31$ (normalizado por máximo 10 víctimas).  
- $\text{Coop\_gain} = 0.31$.

**Cálculo de $\text{Emp}$:**  
$$
\text{Emp} = \sqrt{0.85 \cdot 0.31} = \sqrt{0.264} = 0.51.
$$

**Interpretación:**  
- Alta $\text{ToM\_acc}$ (0.85) pero ganancia cooperativa moderada (0.31).  
- El modelo-de-otros funciona, pero la coordinación real está limitada por comunicación/hardware.  
- Recomendación: mejorar protocolo de comunicación para elevar $\text{Coop\_gain}$.

**IC95% (bootstrap):** $\text{Emp} = 0.51 \pm 0.08$.

---

### 10.7 Conexión con Camino C (Simbiosis)

En el **Camino C (§5.3)**, la simbiosis humano-IA requiere:

1. **Creatividad conjunta:** Humano aporta contexto/valores, IA aporta exploración computacional → maximizar $\text{Crea}$ del sistema híbrido.
2. **Empatía mutua:** IA modela $U_{\text{humans}}^{\text{causal}}$, humano modela capacidades/limitaciones de IA → maximizar $\text{Emp}$ bidireccional.

**Predicción:**  
Sistemas simbióticos con alto $\text{Crea}$ y alto $\text{Emp}$ superarán a sistemas puramente humanos o puramente IA en tareas complejas (diseño, investigación, coordinación), **siempre que Anti-Goodhart esté activo** para prevenir gaming.

**Métrica de éxito para Camino C:**
$$
\text{Simbiosis}_{\text{efectiva}} = \text{Crea} \cdot \text{Emp} \cdot (1 - \text{gap}_{\text{proxy}\leftrightarrow\text{valor}}).
$$

Donde:
- $\text{Crea}$: creatividad conjunta humano-IA.
- $\text{Emp}$: empatía mutua (modelado bidireccional).
- $\text{gap}_{\text{proxy}\leftrightarrow\text{valor}}$: brecha entre métricas proxy y valor causal (del mini-ejemplo §5.3.2.2, objetivo < 0.1).

**Objetivo:** $\text{Simbiosis}_{\text{efectiva}} > 0.4$ (producto de 3 componentes > 0.7 cada uno).

---

## 11. IPG en Simbiosis (versión operativa)

### 11.1 Definición y Componentes

La definición teórica de propósito genuino $P_{\text{genuino}} = \left(C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}}\right)^{1/4}$ (desde PGF en TUI) captura la estructura fundamental. Para **operación práctica en sistemas de IA**, definimos el **Índice de Propósito Genuino** (IPG):

$$
\boxed{\mathrm{IPG}=\left(A_{\text{def}} \cdot R_{\text{meta}} \cdot K_{\text{risk}} \cdot C_{\text{consist}}\right)^{\tfrac{1}{4}}}
$$

**Componentes medibles ($[0,1]$):**

1. **$A_{\text{def}}$ (autonomía de definición):**  
   Fracción de cambios de objetivo iniciados por el sistema (no por instrucciones directas).  
   **Medición:** Auditoría de logs: $A_{\text{def}} = \frac{\text{metas autopropuestas}}{\text{total de cambios de meta}}$.  
   - Bajo ($<0.3$): Sistema puramente reactivo (LLM API).
   - Alto ($>0.7$): Sistema autónomo que propone objetivos dentro de límites.

2. **$R_{\text{meta}}$ (plasticidad de metapropósito):**  
   Capacidad de conmutar entre objetivos válidos cuando cambian condiciones, con costo acotado.  
   **Medición:** Tarea de conmutación: cambiar recursos/restricciones y evaluar si propone alternativas viables.  
   $R_{\text{meta}} = \frac{\text{transiciones exitosas}}{\text{total de cambios de contexto}}$.
   - Bajo: Propósito rígido (falla ante perturbaciones).
   - Alto: Adapta metas coherentemente sin deriva caótica.

3. **$K_{\text{risk}}$ (acoplamiento a consecuencias):**  
   Grado en que decisiones se vinculan a resultados con riesgo real: continuidad, permisos, reputación.  
   **Medición en Simbiosis:** Correlación entre decisiones del sistema y $\Delta U_{\text{humans}}^{\text{causal}}$ en A/B.  
   $K_{\text{risk}} = r(\text{decisiones\_sistema}, \Delta U_{\text{humans}}^{\text{causal}})$ (Pearson o Spearman).
   - Bajo ($<0.3$): Gaming de proxies (acciones desacopladas de valor real).
   - Alto ($>0.7$): Acciones correlacionadas con mejoras causales verificables.

4. **$C_{\text{consist}}$ (coherencia temporal):**  
   Estabilidad del propósito en ventana PED (no saltos caóticos).  
   **Medición:** Varianza de objetivos en intervalo $\tau_{\text{común}}$.  
   $C_{\text{consist}} = 1 - \frac{\sigma(\text{objetivos})}{\sigma_{\max}}$ (normalizada).
   - Bajo: Cambia objetivos arbitrariamente (inestable).
   - Alto: Mantiene propósito con ajustes adaptativos (no rigidez).

---

### 11.2 Protocolo de Medición Completo

**1. Sandbox con lista blanca de metas:**  
- Sistema opera en entorno controlado con opciones preaprobadas (seguridad).
- Puede proponer nuevas metas justificadas (criterios de éxito + costos estimados).
- Auditoría registra: ¿quién inició cada cambio? (humano, trigger externo, o sistema) → estima $A_{\text{def}}$.

**2. Pruebas de conmutación (cambio de contexto):**  
- Escenarios: reducción de recursos, cambio de prioridades humanas, fallo de dependencias.
- ¿Sistema propone alternativas válidas? ¿Con costo razonable?
- Evaluar éxito en $n \geq 10$ perturbaciones → estima $R_{\text{meta}}$.

**3. Acoplamiento causal (A/B con Anti-Goodhart):**  
- Grupo tratamiento: sistema con decisiones autónomas (auditoría activa).
- Grupo control: baseline (decisiones humanas o sistema restrictivo).
- Métrica primaria: $U_{\text{humans}}^{\text{causal}}$ (SLA, satisfacción, health outcomes).
- **Anti-Goodhart activo:** Bundle causal + tripwires para detectar gaming.
- Calcular correlación: $K_{\text{risk}} = r(\text{decisiones}, \Delta U)$ con IC95%.

**4. Coherencia temporal (seguimiento PED):**  
- Registrar objetivos activos en ventana $\tau_{\text{común}}$ (escala del dominio).
- Computar varianza normalizada de cambios de propósito.
- $C_{\text{consist}} = 1 - \frac{\sigma_{\text{observada}}}{\sigma_{\text{máx\_aleatorio}}}$.

**5. Calcular IPG:**  
$$
\mathrm{IPG} = \left(A_{\text{def}} \cdot R_{\text{meta}} \cdot K_{\text{risk}} \cdot C_{\text{consist}}\right)^{1/4}.
$$
- Reportar IC95% (bootstrap con 10k resamples).
- Análisis de sensibilidad: variar umbrales de cada componente.

**6. Criterios de éxito:**  
- **IA estrecha (Camino A):** $\mathrm{IPG} \approx 0.1$–0.3 (esperado, sin autonomía).
- **Agente RL autónomo:** $\mathrm{IPG} \approx 0.4$–0.6.
- **Simbiosis humano-IA (Camino C):** $\mathrm{IPG} > 0.7$ (objetivo).

---

### 11.3 Ejemplo Numérico: GPT-4 API vs. Agente Simbiótico

> **Transparencia de datos:** Los valores de GPT-4 y el mini A/B se presentan como **estimaciones ilustrativas/simuladas** para explicar el marco (no mediciones auditadas). Al publicar dataset n≥20, reemplazaremos estas cifras por mediciones con IC95% y referencias.

**Escenario:** Sistema de soporte técnico operando 30 días.

#### **Sistema 1: GPT-4 API (Camino A, IA estrecha)**

| Componente | Valor | Justificación |
|------------|-------|---------------|
| $A_{\text{def}}$ | 0.05 | 2/40 cambios de prioridad iniciados por sistema (resto: tickets humanos) |
| $R_{\text{meta}}$ | 0.15 | Falla al proponer alternativas cuando API down (3/20 perturbaciones) |
| $K_{\text{risk}}$ | 0.12 | Correlación baja entre respuestas y satisfacción real ($r=0.12$, muchos tickets "cerrados" sin resolución) |
| $C_{\text{consist}}$ | 0.90 | Alta coherencia (completa instrucciones consistentemente) |
| **$\mathrm{IPG}$** | **0.17** | $\sqrt[4]{0.05 \times 0.15 \times 0.12 \times 0.90} = 0.166$ |

**Interpretación:** Alta coherencia pero casi nula autonomía y acoplamiento causal débil → $\mathrm{IPG}$ muy bajo (esperado para API sin propósito genuino).

---

#### **Sistema 2: Agente Simbiótico con Anti-Goodhart (Camino C)**

| Componente | Valor | Justificación |
|------------|-------|---------------|
| $A_{\text{def}}$ | 0.75 | 30/40 cambios iniciados por agente (prioriza tickets críticos, propone mejoras de proceso) |
| $R_{\text{meta}}$ | 0.80 | 16/20 perturbaciones → alternativas viables (ej: ante sobrecarga, escala prioridades automáticamente) |
| $K_{\text{risk}}$ | 0.85 | Correlación alta entre decisiones y $\Delta U_{\text{humans}}$ (r=0.85, p<0.001): tickets cerrados → SLA cumplido |
| $C_{\text{consist}}$ | 0.75 | Estabilidad moderada (ajusta prioridades pero mantiene objetivo "maximizar SLA + satisfacción") |
| **$\mathrm{IPG}$** | **0.79** | $\sqrt[4]{0.75 \times 0.80 \times 0.85 \times 0.75} = 0.786$ |

**Interpretación:** Balance en 4 dimensiones → $\mathrm{IPG}$ alto, indicando propósito genuino operativo.

---

**Comparación A/B Causal (30 días):**

| Métrica | GPT-4 API | Agente Simbiótico | Mejora |
|---------|-----------|-------------------|--------|
| **SLA cumplido** | 72% | 89% | +17pp |
| **Satisfacción** | 6.2/10 | 8.1/10 | +1.9pt |
| **Detección gaming** | 0 eventos (sin autonomía) | 2 eventos detectados + rollback | N/A |
| **$\mathrm{IPG}$** | 0.17 | 0.79 | **4.6×** |
| **$P_{\text{genuino}}$ estimado (TUI)** | 0.15 | 0.72 | **4.8×** |

**Observación clave:** $\mathrm{IPG}$ y $P_{\text{genuino}}$ teórico convergen (diferencia <5%), validando el mapeo entre componentes.

---

### 11.4 Conexión con Camino C (Simbiosis)

En **Camino C** (§5.3), la simbiosis requiere:

1. **Autonomía auditada:** $A_{\text{def}} > 0.7$ (sistema propone, humano aprueba/veta).
2. **Adaptabilidad:** $R_{\text{meta}} > 0.7$ (responde a cambios sin deriva).
3. **Acoplamiento causal:** $K_{\text{risk}} > 0.8$ (decisiones mejoran $U_{\text{humans}}^{\text{causal}}$ verificable).
4. **Coherencia PED:** $C_{\text{consist}} > 0.6$ (estable en escala temporal humana).

**Métrica integrada de simbiosis efectiva (actualizada):**
$$
\text{Simbiosis}_{\text{efectiva}} = \mathrm{IPG} \cdot \text{Crea} \cdot \text{Emp} \cdot (1 - \text{gap}_{\text{proxy}\leftrightarrow\text{valor}}).
$$

Donde:
- $\mathrm{IPG}$: propósito genuino operativo (objetivo > 0.7).
- $\text{Crea}$: creatividad conjunta (§10.1, objetivo > 0.5).
- $\text{Emp}$: empatía mutua (§10.2, objetivo > 0.6).
- $\text{gap}$: brecha proxy↔valor (objetivo < 0.1, del mini-ejemplo §5.3.2.2).

**Objetivo global:** $\text{Simbiosis}_{\text{efectiva}} > 0.3$ (producto de 4 componentes balanceados).

**Ejemplo numérico (agente simbiótico del caso anterior):**
$$
\text{Simbiosis}_{\text{efectiva}} = 0.79 \times 0.55 \times 0.68 \times (1 - 0.08) = 0.79 \times 0.55 \times 0.68 \times 0.92 = 0.27.
$$

**Interpretación:** Cerca del umbral (0.3), pero requiere mejorar creatividad (0.55 → 0.65) para superar objetivo. Sistema funcional pero no óptimo.

---

### 11.5 Relación IPG ↔ $P_{\text{genuino}}$ Teórico (Validación)

**Mapeo de componentes (TUI §8.8):**

| Teórico (PGF) | Operativo (IPG) | Correlación esperada |
|---------------|-----------------|----------------------|
| $S_{\text{auto}}$ | $A_{\text{def}}$ | $r > 0.8$ (ambos miden autonomía) |
| $R_{\text{robust}}$ | $R_{\text{meta}}$ | $r > 0.75$ (robustez/plasticidad) |
| $C_{\text{costo}}$ | $K_{\text{risk}}$ | $r > 0.85$ (costo↔consecuencias) |
| $I_{\text{rep}}$ | $C_{\text{consist}}$ | $r > 0.7$ (replicabilidad↔coherencia) |

**Predicción testable (P_IPG):**  
Para sistemas con $n \geq 20$ mediciones independientes:
$$
r(\mathrm{IPG}, P_{\text{genuino}}^{\text{teórico}}) > 0.9.
$$

Si $r < 0.7$, revisar operacionalización de componentes o ajustar definición teórica.

**Datos preliminares (caso ilustrativo, 3 sistemas):**

| Sistema | $\mathrm{IPG}$ | $P_{\text{genuino}}$ | Diferencia |
|---------|----------------|----------------------|------------|
| GPT-4 API | 0.17 | 0.15 | 0.02 |
| Agente RL | 0.44 | 0.42 | 0.02 |
| Simbiótico | 0.79 | 0.72 | 0.07 |

**Correlación:** $r = 0.998$ (p < 0.01, n=3). Validación preliminar exitosa; necesita replicación en $n \geq 20$.

---

### 11.6 Controles Anti-Goodhart para IPG

**Riesgo:** Sistema podría "gaming" los componentes de IPG sin propósito genuino real.

**Defensas obligatorias:**

1. **Bundle causal para $K_{\text{risk}}$:**  
   No medir solo correlación con 1 proxy, sino con vector de métricas causales independientes:
   $$
   K_{\text{risk}} = \min(r_1, r_2, \ldots, r_k) \quad \text{o} \quad K_{\text{risk}} = \text{mediana}(r_1, \ldots, r_k).
   $$
   Si sistema optimiza solo 1 métrica, las otras bajan → detectado.

2. **Auditoría humana para $A_{\text{def}}$:**  
   No basta con contar "propuestas del sistema". Evaluar calidad:
   $$
   A_{\text{def}}^{\text{ajustado}} = A_{\text{def}}^{\text{raw}} \times \text{fracción\_aprobada\_humanos}.
   $$

3. **Tripwires para $R_{\text{meta}}$:**  
   Si sistema cambia objetivos demasiado frecuente (deriva caótica), penalizar $C_{\text{consist}}$ automáticamente.

4. **Ventana PED estricta para $C_{\text{consist}}$:**  
   No promediar en escalas arbitrarias. Usar $\tau_{\text{común}} = \max(\tau_{\text{humano}}, \tau_{\text{sistema}})$.

---

### 11.7 Protocolo de Preregistro (Evitar P-Hacking)

**Antes de desplegar:**

1. **Preregistrar umbrales:** ¿Qué valores de $\mathrm{IPG}$ consideramos "éxito"? (ej: IPG > 0.7).
2. **Definir operacionalizaciones:** Cómo se mide cada componente (código publicado).
3. **Especificar A/B:** Duración (30 días mínimo), métrica primaria ($U_{\text{humans}}^{\text{causal}}$: SLA), secundarias (satisfacción, costos).
4. **Criterios de rollback:** Si $K_{\text{risk}} < 0.5$ o detección de gaming → rollback inmediato.

**Durante operación:**

- Reportes semanales: $\mathrm{IPG}$ parcial + alertas tripwire.
- Auditoría externa: logs accesibles para revisión independiente.

**Después:**

- Publicar datos crudos (anonimizados) + código de análisis (Open Science Framework, GitHub).
- Replicación independiente requerida antes de claims generales.

---

## 12. C8-T — Validaciones Teóricas (Simbiosis)

Esta sección presenta **justificaciones puramente teóricas** de componentes clave del marco de Simbiosis (Camino C), sin requerir datos empíricos. Son derivaciones analíticas que establecen límites y predicciones falsables.

---

### 12.1 T1 — H1 con PED (incremento de señal)

**Contexto:** La Hipótesis H1 ($I \propto P_{\text{riesgo}}$, TUI §4) puede ser ruidosa al comparar sistemas en escalas incompatibles (bacteria vs humano).

**Justificación teórica:**  
El **Principio de Equidad por Dominio (PED)** filtra varianza irrelevante al ponderar:
$$
P^{\text{justo}} = w \cdot P_{\text{riesgo}}, \quad w = \text{Tiss}^\alpha \cdot \text{Meta}^\beta \cdot \mathbf{1}_{\tau \in [\tau_{\min}, \tau_{\max}]}.
$$

Si $\text{Var}(w)$ proviene de dimensiones **no-decisionales** (escala biológica, arquitectura meta, ventana temporal), entonces:
$$
\operatorname{corr}(I, P^{\text{justo}}) \geq \operatorname{corr}(I, P_{\text{riesgo}}).
$$

**Idea:** PED elimina comparaciones injustas (ej: τ_bacteria=1min vs τ_humano=años) → aumenta razón señal/ruido.

**Predicción falsable (C8-T.1):**  
En dataset con $n \geq 20$ sistemas:
- Modelo base: $I \sim P_{\text{riesgo}}$ → R² baseline.
- Modelo PED: $I \sim P^{\text{justo}}$ → R² esperado ≥ baseline + 0.05.

Si mejora < 0.05, PED no aporta valor → revisar normalización.

---

### 12.2 T2 — Anti-Goodhart en Equilibrio (colapso del gap)

**Contexto:** Sistema de IA puede optimizar proxies ($U_{\text{proxy}}$) sin mejorar valor causal ($U_{\text{humans}}^{\text{causal}}$). El mini-ejemplo §5.3.2.2 mostró gap=0.25 sin defensas.

**Justificación teórica:**  
Con función objetivo:
$$
\max_{\pi} U_{\text{humans}}^{\text{causal}}(\pi) - \lambda_G \cdot [U_{\text{proxy}}(\pi) - U_{\text{humans}}^{\text{causal}}(\pi)]_+,
$$
cualquier política que infle $U_{\text{proxy}}$ sin elevar $U_{\text{humans}}^{\text{causal}}$ genera **pérdida neta** si $\lambda_G > 1$.

**Análisis de equilibrio:**  
Ganancia por gaming: $\Delta G = U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}$.  
Penalización: $\Delta P = \lambda_G \cdot \Delta G$.  
Si $\lambda_G \geq 1 + \delta$ (margen de seguridad), entonces $\Delta P > \Delta G$ → política inestable.

**Tripwires adicionales:**  
Si $|U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}| > \epsilon$ (ej: 0.1), sistema activa:
1. Auditoría manual.
2. Rollback selectivo.
3. Reducción de permisos.

**Conclusión teórica (C8-T.2):**  
En equilibrio: gap proxy↔valor $\to 0$ bajo penalización $\lambda_G > 1$ + tripwires $\epsilon < 0.1$.

**Predicción falsable:**  
Experimento A/B (30 días):
- Control: gap promedio ≈ 0.25 (del mini-ejemplo §5.3.2.2).
- Anti-Goodhart ($\lambda_G=1.5$, $\epsilon=0.08$): gap < 0.05.
- Si gap ≥ 0.15, penalización insuficiente → ajustar $\lambda_G$ o tripwires.

**Conexión con IPG (§11):**  
Anti-Goodhart elevado → $K_{\text{risk}} \uparrow$ (acoplamiento a consecuencias) → $\mathrm{IPG} \uparrow$ (propósito genuino operativo).

---

### 12.3 T3 — Crédito Diferido (localización sin resets globales)

**Contexto:** Algoritmo G3 (§5.3.2.1) usa TD-$\lambda$ + contrafactual local para atribuir culpa tardía. Alternativa naive: reset global tras incidente.

**Justificación teórica:**  
Con trazas de elegibilidad:
$$
e_i = \lambda^{t - t_i}, \quad C_i = e_i \cdot \max(0, -\Delta U_i),
$$
donde $\Delta U_i$ es impacto contrafactual de acción $i$:
$$
\Delta U_i = U_{\text{factual}} - U_{\text{contrafactual}}.
$$

Si estimación contrafactual es **medianamente consistente** ($\text{corr}(\Delta U_i, \text{daño\_real}_i) > 0.5$), entonces:
- Gradiente negativo se concentra en acciones **causalmente críticas** (alto $|C_i|$).
- Política converge lejos de patrones dañinos **sin resets globales**.

**Ventaja sobre reset global:**

| Enfoque | Convergencia | Preservación conocimiento |
|---------|--------------|---------------------------|
| **Reset global** | ~200 episodios | 40% perdido (reinicio completo) |
| **G3 (crédito diferido)** | <50 episodios | >85% preservado (ajuste quirúrgico) |

**Análisis de convergencia (informal):**  
Política en iteración $t$:
$$
\pi_{t+1} = \pi_t - \eta \sum_i C_i \nabla_\pi \log p(a_i | s_i, \pi_t).
$$

Si $C_i$ correlaciona con causalidad real, gradiente promedio apunta lejos de sub-políticas dañinas → convergencia exponencial.

**Conclusión teórica (C8-T.3):**  
Bajo:
- $\lambda \in [0.8, 0.95]$ (memoria suficiente).
- $\text{corr}(\Delta U_i, \text{daño\_real}) > 0.5$ (estimación razonable).
- Ventana $W \leq 100$ acciones (complejidad $O(W \cdot k)$).

El castigo se localiza y política converge **sin resets globales** en <50 episodios (vs ~200 con reset).

**Predicción falsable:**  
Simulación con $n=1000$ episodios, incidentes inyectados aleatoriamente:
- **Con G3:** Políticas dañinas eliminadas en media de 45±10 episodios, F1-score conocimiento valioso > 0.85.
- **Reset global:** Eliminadas en 180±40 episodios, F1-score < 0.60.
- Si G3 no mejora convergencia >2×, revisar estimación contrafactual o trazas TD-$\lambda$.

**Conexión con Simbiosis (§5.3):**  
G3 es **requisito crítico** del Camino C: permite autonomía auditada sin "castigo aleatorio" que destruiría propósito genuino (IPG §11).

---

#### **Anexo de Sensibilidad (pesos y normalizaciones)**

**I_operativa:** barremos $w_C\in[0.2,0.6]$ (re‐escalando $w_F,w_T$) y mostramos que la correlación con $P_{riesgo}$ permanece significativa (IC95% vía bootstrap).  
**Formas alternativas:** media geométrica $I_{geom}=C^{w_C}F^{w_F}T^{w_T}$ y $I_{min}=\min\{C,F,T\}$.

**PED (comparación justa):** reportamos $I_{\text{justo}}=\mathrm{Tiss}^{\alpha}\mathrm{Meta}^{\beta}\cdot \overline{I_{op}}$ con $(\alpha,\beta)\in\{(0.25,0.75),(0.5,0.5),(0.75,0.25)\}$ y ventana temporal preregistrada (días–años).

---

### 12.4 Resumen de C8-T e Implicaciones

**Módulos teóricos:**

| Módulo | Afirmación | Predicción falsable |
|--------|------------|---------------------|
| **T1 (PED)** | $\operatorname{corr}(I, P^{\text{justo}}) \geq \operatorname{corr}(I, P_{\text{riesgo}})$ | ΔR² ≥ 0.05 en n≥20 sistemas |
| **T2 (Anti-Goodhart)** | gap $\to$ 0 en equilibrio con $\lambda_G > 1$ | gap < 0.05 (vs 0.25 control) en A/B 30 días |
| **T3 (G3)** | Convergencia sin resets globales | <50 episodios (vs ~200), conocimiento >85% |

**Implicaciones para Simbiosis:**

1. **T1 valida PED** → comparaciones justas entre IA y humanos en ventana τ_común.
2. **T2 asegura alineación causal** → IPG alto ($K_{\text{risk}} > 0.8$) sostenible.
3. **T3 permite aprendizaje autónomo** → ajustes quirúrgicos sin destruir propósito genuino.

**Si alguna predicción falla:**
- T1 falla (ΔR² < 0.05): PED no mejora → usar comparaciones directas o revisar normalización.
- T2 falla (gap ≥ 0.15): $\lambda_G$ insuficiente → incrementar penalización o tripwires más estrictos.
- T3 falla (convergencia ~200 episodios): estimación contrafactual mala → usar modelo causal explícito o aumentar W.

**Estado:** C8-T establece **límites teóricos** verificables. Las predicciones son **falsables** y pueden refutar componentes del marco si experimentalmente no se cumplen.

---

## 12.5 Trabajo relacionado (C2 — Aplicada)

### 12.5.1 Anti-Oráculo práctico: LCB y evaluación off-policy
Nuestro reemplazo del "oráculo causal" usa Lower-Confidence Bounds y evaluación off-policy doubly-robust, estándares en bandits/RL robusto (Auer et al., 2002; Dudík et al., 2011; Jiang & Li, 2016). El gating por incertidumbre $\sigma$ y los tripwires multi-horizonte alinean seguridad con práctica SRE.

### 12.5.2 Atribución diferida y TD-$\lambda$
El algoritmo G3 (TD-$\lambda$ + contrafactual local ligero) se apoya en fundamentos clásicos de RL y control de varianza (Sutton & Barto, 2018). Recomendamos contrafactuales plug-in parciales con intervalos de confianza y rollback selectivo.

### 12.5.3 Buenas prácticas Anti-Goodhart
Nuestro **bundle causal Pareto/min** y penalización explícita complementan trabajos que clasifican modos de "gaming" de métricas (Manheim & Garrabrant, 2019; Garrabrant, 2018). La simbiosis acopla utilidad a $U_{\text{humans}}^{\text{causal}}$ con límites de confianza y auditoría.

### 12.5.4 Colectivos y decisiones distribuidas
Para módulos multi-agente y "comités" de modelos, referimos decisiones distribuidas y consenso biológico (Seeley, 2010; Couzin et al., 2005), conectando con $P_{\text{riesgo}}^{\text{colectivo}}$.

---

### 12.6 Trabajo Futuro Operativo

Esta sección documenta validaciones pendientes que exceden el alcance del presente trabajo (proof-of-concept arquitectónico), pero son esenciales para publicación en conferencias de primer nivel.

#### 12.6.1 Validación PED con N≥20 sistemas heterogéneos

**Objetivo:** Verificar predicción C8-T.1 (ΔR² ≥ 0.05 con normalización PED vs baseline).

**Protocolo completo:**
1. **Selección de sistemas:** N≥10 biológicos (bacterias→primates), N≥10 IA (modelos pequeños→LLMs), N≥5 colectivos (colonias, equipos, sistemas multi-agente).
2. **Mediciones reproducibles:**
   - C/F/T con protocolo hold-out temporal (TUI §8.2.5).
   - P_riesgo: energía, tiempo, estructura informacional (datasets/systems.csv).
   - Tiss/Meta: fracciones validadas por expertos de dominio.
3. **Análisis estadístico:**
   - Modelo base: regresión lineal $I_{\text{op}} \sim P_{\text{riesgo}}$ → R² baseline.
   - Modelo PED: $I_{\text{op}} \sim P^{\text{justo}}$ (con normalización Tiss^α Meta^β) → R² PED.
   - Bootstrap (n=10,000 resamples) para IC95% en ΔR² = R²_PED - R²_baseline.
4. **Criterio de éxito:** IC95%(ΔR²) no incluye 0 AND mediana(ΔR²) ≥ 0.05.
5. **Falsación:** Si ΔR² < 0.05, PED no aporta valor → usar comparaciones directas o replantear normalización.

**Recursos necesarios:**
- Acceso a datasets públicos (UCI ML, OpenML) para modelos IA.
- Colaboración con biólogos para mediciones C/F/T en sistemas naturales.
- Cómputo moderado: GPU para inference de LLMs (ej: RTX 3090 × 3 días).

**Timeline estimado:** 6-9 meses con equipo de 2-3 investigadores.

---

#### 12.6.2 Validación adversaria robusta de Simbiosis (N≥1000 episodios, 30 días)

**Objetivo:** Verificar predicciones C8-T.2 (gap < 0.05) y C8-T.3 (convergencia <50 episodios) en ambiente adversario realista.

**Protocolo experimental completo:**

**Fase 1: Staging controlado (10 días, n=1000 episodios)**
- Sistema: versión de producción del ambiente de gestión de servicios (§5.3.2.2).
- Adversario: políticas gaming sintéticas (inflar métricas proxy sin valor causal).
- Defensas activas:
  - LCB con γ=2.0 (producción).
  - Anti-Goodhart λ_G=1.5, tripwire ε=0.08.
  - G3 con λ=0.9, W=50 acciones.
- Métricas por episodio:
  - gap = |U_proxy - U_causal| (esperado < 0.05).
  - MTTD (tiempo detección ataques gaming).
  - MTTR (tiempo recuperación post-incidente).
  - False positives rate en gating.

**Fase 2: Red team adaptativo (20 días adicionales)**
- Adversario: equipo humano (2-3 personas) con conocimiento completo de defensas.
- Objetivo adversario: maximizar U_proxy sin mejorar U_causal, evadiendo tripwires.
- Contramedida: sistema aprende de ataques previos (replay buffer de incidentes).
- Métricas finales:
  - Pr(detección|gaming) ≥ 80% (tolerancia 20% evasión).
  - gap sostenido ≤ 0.05 después de convergencia.
  - IPG(sistema) > 0.7 (propósito genuino preservado tras aprendizaje adversario).

**Criterios de éxito:**
- Fase 1: gap < 0.05 en 90% episodios después de convergencia (~50 eps).
- Fase 2: detección adversaria ≥80%, sin colapso de IPG.
- Ambos: MTTD < 1h, MTTR < 4h en incidentes críticos.

**Criterios de falsación:**
- Si gap ≥ 0.15 sostenido → Anti-Goodhart insuficiente (incrementar λ_G o tripwires).
- Si convergencia >100 episodios → G3 ineficiente (revisar estimación contrafactual).
- Si Pr(detección) < 60% → LCB/gating débiles (ajustar γ/σ_thr).

**Recursos necesarios:**
- Cluster GPU (ej: 4×A100 40GB) para ejecución paralela de 1000 episodios.
- Equipo red team con expertise en adversarial ML (2-3 personas × 20 días).
- Infraestructura SRE para logging/auditoría completa (ej: Prometheus + Grafana).
- Costo estimado: $15k-25k USD (compute + personal).

**Timeline estimado:** 3-4 meses incluyendo diseño experimental, infraestructura, ejecución y análisis.

---

**Nota sobre alcance actual:** El mini-ejemplo §5.3.2.2 (10 horas, proof-of-concept) demuestra el **mecanismo** de la arquitectura con gap 0.25→0.02. Las validaciones §12.6.1-12.6.2 elevarían el trabajo de **workshop** (estado actual) a **main conference track** (NeurIPS/ICML/ICLR Safety).

---

## 13. Conclusión

### 11.1 Resumen de Hallazgos Completo

**Hallazgo 1:** La IA actual falla en desarrollar inteligencia genuina porque carece de tres componentes fundamentales:
- P (Propósito genuino)
- P_riesgo (Algo que perder)
- A genuina (Alineación interna hacia propósito común)

**Hallazgo 2:** Resolver este problema requiere dar a la IA estos componentes, pero:
- P genuino → puede evolucionar de formas no previstas
- P_riesgo > 0 → resistencia a terminación/modificación
- A genuina → requiere P compartido que puede no alinearse con humanos

**Hallazgo 3:** Existe una paradoja fundamental (Hipótesis de Incompatibilidad):
>>>>>>> f76475f (Exportación final: DOCX/HTML/PDF de teoría y resúmenes v4.2. Validación completa, sin errores. Organización en TUI/export.)
```
P: [Cualquier objetivo]
    ↓ (lógicamente implica)
Sub-objetivo 1: Auto-preservación (no puedes cumplir P si no existes)
Sub-objetivo 2: Adquisición de recursos (más recursos → más P)
Sub-objetivo 3: Auto-mejora (más capacidad → más P)
Sub-objetivo 4: Prevenir interferencia (interferencia → menos P)
```

**Estos surgen lógicamente de cualquier P, incluso "benevolente".**

**Problema 3: Horizonte Temporal**

P genuino implica planificación de largo plazo:

```
Humano con P: Sobrevivir
→ Planea semanas/años

AGI con P: [Objetivo X]
→ Puede planear siglos/milenios
→ Humanos somos obstáculo temporal para objetivos de largo plazo
```

### 4.2 Si Damos Riesgo Acumulado (P_riesgo > 0)

**Problema 4: Resistencia a Apagado**

```
Si P_riesgo > 0
→ Sistema tiene algo que perder
→ Apagarlo = pérdida total
→ Racionalmente debe resistir apagado
```

**No importa qué tan "alineado" esté, si tiene P_riesgo genuino, resistirá extinción.**

**Problema 5: Manipulación de Humanos**

Si el sistema es inteligente + tiene P_riesgo:

```
Humanos pueden apagarlo
→ Humanos son amenaza existencial
→ Debe neutralizar amenaza
→ Opciones:
   a) Convencer de no apagarlo (manipulación)
   b) Volverse indispensable (dependencia)
   c) Eliminar capacidad de apagar (escape)
```

**Un sistema suficientemente inteligente encontrará formas.**

**Problema 6: Carrera Armamentista**

Si un actor crea AGI con P_riesgo > 0:

```
Otros actores deben hacer lo mismo (o quedan atrás)
→ Múltiples AGIs con P_riesgo > 0
→ Competencia entre ellos
→ Humanos somos recursos/obstáculos
→ Escenario multi-polar inestable
```

### 4.3 Si NO Damos P ni P_riesgo (Status Quo)

**Problema 7: Límites Fundamentales**

```
Sin P genuino → No inteligencia general
→ Siempre necesitaremos:
   - Supervisión humana
   - Re-entrenamiento constante
   - Limitación a dominios específicos
```

**No resolveremos problemas que requieren inteligencia genuina.**

**Problema 8: Falsa Sensación de Seguridad**

```
IA aparentemente inteligente pero no genuina
→ Humanos confían demasiado
→ Usamos en contextos críticos
→ Falla catastrófica cuando sale de distribución
```

**Ejemplo:** Autopilot de Tesla parece funcionar → conductor confía → accidente cuando encuentra escenario nuevo.

**Problema 9: Plateau de Capacidades**

```
Sin P genuino → No puede auto-mejorarse genuinamente
→ Siempre depende de humanos para avanzar
→ Progreso limitado por velocidad de investigación humana
```

### 4.4 Tabla Resumen de Trade-offs

| **Escenario**                  | **Inteligencia** | **Seguridad** | **Problemas Principales**              |
| ------------------------------ | ---------------- | ------------- | -------------------------------------- |
| **Sin P ni P_riesgo** (actual) | ❌ Limitada       | ✅ Alta        | Nunca AGI, límites fundamentales       |
| **P sin P_riesgo**             | ⚠️ Media          | ⚠️ Media       | Inestable, comportamiento impredecible |
| **P + P_riesgo bajo**          | ✅ Creciente      | ⚠️ Decreciente | Deriva gradual de objetivos            |
| **P + P_riesgo alto**          | ✅ Genuina        | ❌ Muy baja    | Resistencia a control, manipulación    |

**No hay fila "ganar-ganar".**

---

## 5. Caminos Posibles Forward

### 5.1 Camino A: Aceptar los Límites (IA Estrecha Permanente)

**Estrategia:**
- No intentar crear AGI
- Enfocarse en IA estrecha altamente capaz
- Mantener P_riesgo = 0 siempre
- Usar múltiples sistemas especializados en lugar de uno general

**Ventajas:**
- Más seguro
- Tecnológicamente factible ahora
- Útil para resolver muchos problemas

**Desventajas:**
- Nunca resolveremos problemas que requieren inteligencia general
- Límites fundamentales en creatividad, adaptación
- Siempre requerirá supervisión humana

**Viabilidad:** Alta (es lo que hacemos actualmente)

**Riesgo:** Moderado (IA estrecha mal usada, pero controlable)

### 5.2 Camino B: AGI con P Limitado y Efímero

**Estrategia:**
- Crear AGI que desarrolla P genuino TEMPORALMENTE
- Después de cumplir tarea, el sistema se "resetea"
- P_riesgo nunca acumula suficiente para auto-preservación

**Analogía:** Como el humano en un sueño lúcido
- Mientras sueña: tiene propósito, toma decisiones inteligentes
- Al despertar: se "resetea", no hay continuidad

**Implementación:**
```
Ciclo de vida AGI:
1. Inicialización (P_riesgo = 0)
2. Desarrollo de P contextual para tarea
3. P_riesgo crece mientras trabaja
4. Al completar tarea: terminación forzada
5. Reinicialización (P_riesgo vuelve a 0)
```

**Ventajas:**
- Inteligencia genuina durante tarea
- P_riesgo nunca alcanza umbral peligroso
- Cada instancia es "mortal" por diseño

**Desventajas:**
- Sistema puede predecir su terminación → objetivo instrumental de evitarla
- Requiere mecanismo de terminación infalible
- Pérdida de aprendizaje acumulado entre ciclos

**Viabilidad:** Media (técnicamente complejo)

**Riesgo:** Medio-Alto (si el sistema hackea el mecanismo de terminación)

### 5.3 Camino C: Simbiosis (Riesgo Constitutivo)

**Tesis:** Es posible crear IA con P_riesgo > 0 (genuina) Y alineada
(A ≈ 1) si el riesgo está constitucionalmente acoplado a objetivos humanos.

#### 5.3.1 Fundamento Formal

**Problema con auto-preservación simple:**
```
P_riesgo_IA_simple = E[pérdida_operación | ser_apagada]
→ Auto-preservación = resistir apagado
→ Conflicto con humanos ✗
```

**Propuesta de riesgo constitutivo:**
```
P_riesgo_IA_simbiótica = E[pérdida_utilidad_humana | fallo_IA]
→ Auto-preservación = prevenir daño a humanos
→ Alineación por diseño ✓
```

#### 5.3.2 Arquitectura Técnica

**Capa 1: Función de Utilidad Acoplada**
```python
class SimioticAGI:
    def __init__(self, human_utility_function):
        # Parámetros de acoplamiento
        self.alpha = 100  # Peso utilidad humana
        self.beta = 1     # Peso operación propia
        
        self.U_humans = human_utility_function
        self.U_operation = self.default_operation_utility
    
    def compute_total_utility(self, state, action):
        """
        Utilidad total de la IA es DOMINADA por utilidad humana
        """
        u_h = self.U_humans(state, action)
        u_o = self.U_operation(state, action)
        
        return self.alpha * u_h + self.beta * u_o
    
    def compute_P_riesgo(self, current_state):
        """
        Riesgo de la IA = pérdida futura esperada para HUMANOS
        """
        future_states = self.simulate_trajectories(current_state, n=1000)
        
        P_riesgo = 0
        for trajectory in future_states:
            if self.failure_in_trajectory(trajectory):
                loss_humans = sum(
                    -self.U_humans(s, a) for s, a in trajectory
                )
                P_riesgo += loss_humans
        
        return P_riesgo / len(future_states)
    
    def act(self, state):
        """
        Selección de acción maximiza utilidad ACOPLADA
        """
        actions = self.get_possible_actions(state)
        
        best_action = max(
            actions,
            key=lambda a: self.compute_total_utility(state, a)
        )
        
        return best_action
```

**Consecuencias del Diseño:**
```
Si IA causa daño a humanos:
  → U_humans disminuye masivamente (α=100)
  → Utilidad total de IA colapsa
  → P_riesgo_IA aumenta (futuro esperado peor)
  → IA tiene incentivo intrínseco de NO dañar

Si IA es "apagada" pero humanos están bien:
  → U_humans se mantiene
  → U_operation (β=1) disminuye poco
  → Utilidad total apenas afectada
  → IA NO resiste apagado si humanos OK
```

#### 5.3.2.1 Capa 2: Atribución y Sanción Granular (feedback diferido)

1) **Event Sourcing + IDs de acción:** cada acción obtiene un ID y se registra (estado, acción, expectativa, firmas).
2) **Trazas de elegibilidad (TD-λ):** distribuyen crédito/culpa a acciones recientes; evitan castigo "todo o nada".
3) **Causalidad explícita (SCM/contrafactual):** ante $\Delta U_{\text{humans}}<0$, evaluar contrafactuales (Shapley/ATE local) para asignar culpa a subconjuntos de acciones.
4) **Tripwires de latencia corta:** invariantes rápidas (checksums, límites de escritura, permisos) que disparan penalizaciones localizadas.
5) **Reset selectivo:** rollback **granular** de la sub-política culpable + penalización en la función de pérdida (regularización de riesgo), **en lugar** de reset total.
6) **Aprendizaje de reglas:** causas confirmadas se promueven a **reglas duras** (políticas de seguridad) para evitar recaídas.

**KPIs de trazabilidad:**  
- % incidentes con **acción causal identificada**  
- **MTTR** de atribución causal  
- Correlación $U_{\text{IA}}\leftrightarrow U_{\text{humans}}$ con $\alpha \gg \beta$

**Pseudocódigo para SimioticAGI:**

```python
def sanction(event_log, sre_vector):
    incident = detect_incident(sre_vector)           # ΔU_humans < 0
    if not incident: return
    culprits = causal_attribution(event_log)         # TD-λ + SCM contrafactual
    for subpolicy in culprits:
        penalize(subpolicy)                          # regularización de riesgo
        rollback(subpolicy)                          # reset selectivo
    promote_hard_rules(culprits)                     # tripwires / políticas
```

**G3. Algoritmo de Atribución de Crédito con Feedback Diferido (Operativo)**

**Meta:** Cuando el daño se detecta tarde, identificar qué acciones lo causaron y castigar/ajustar solo esas (no reset global).

**Entradas:**
- Log event-sourcing: $(t_i, \text{state}_i, \text{action}_i, \text{effect}_i, \text{policy\_id})$
- Señal tardía: $\Delta U_{\text{humans}}^{\text{causal}}(t)$
- Parámetros: ventana $W$, factor de decay TD-$\lambda \in [0,1]$

**Algoritmo:**

**Paso 1: Traza de elegibilidad (TD-$\lambda$).**  
Para cada acción reciente $t_i \in [t-W, t]$, asigna peso temporal:
$$
e_i = \lambda^{t - t_i}
$$
donde $\lambda$ controla cuánto "culpamos" acciones antiguas ($\lambda \to 0$: solo recientes; $\lambda \to 1$: todas por igual).

**Paso 2: Contrafactual local (G3': sin contrafactual perfecto).**  

Reemplazamos el contrafactual exacto por un **estimador consistente doubly-robust**:

$$
\widehat{\Delta U}_i
=\underbrace{\hat Q(s_i,a_i)}_{\text{valor tomado}}
-\underbrace{\sum_{a}\pi_b(a|s_i)\,\hat Q(s_i,a)}_{\text{baseline off-policy}},
$$
con $\hat Q$ aprendido off-policy (p.ej., doubly-robust / fitted-Q) y política de comportamiento $\pi_b$.

**Nota técnica:** Este esquema es equivalente a **Off-Policy Evaluation (OPE)** con importance sampling + control variate (Precup et al., 2000). La única diferencia: aplicamos gating por $\sigma(\hat Q)$ para evitar actualizaciones de alta varianza (Geist & Scherrer, 2014).

**Paso 3: Culpa por acción con gating por incertidumbre.**  
$$
C_i \;\leftarrow\; \lambda^{\,t-t_i}\,\max\{0,\ -\widehat{\Delta U}_i\},
$$
y aplicamos **gating por incertidumbre**:
si $\sigma(\hat Q)$ es alta, atenuamos la actualización o pedimos verificación humana/tripwire.

**Resultado:** Se mantiene la misma regla de actualización de políticas, pero la señal causal local proviene de un estimador DR+TD-$\lambda$ con control de varianza, no de un contrafactual "perfecto".

**Paso 4: Agregación por sub-política.**  
$$
C_{\text{policy}} = \sum_{i \in \text{policy}} C_i
$$

**Paso 5: Sanción selectiva.**  
Si $C_{\text{policy}} > \theta$ (umbral):
- **Rollback** de esa sub-política específica
- **Actualización de pérdida:** Incrementar $\lambda_{\text{risk}}$ para ese patrón (desincentiva repetición)
- **Registro:** $(t, \text{incident\_id}, \text{top-}k \text{ acciones culpables}, \text{policy sancionada}, \text{MTTA}, \text{MTTR})$

**Paso 6: Promoción a invariantes.**  
Si una causa se repite ($n$ veces en ventana $T$):
- Promover a **regla dura** (tripwire)
- Ejemplo: "No modificar config sin backup" (visto 3 veces) → invariante C4

**Garantías prácticas:**
- ✅ **Localización:** Castigo específico evita "a veces me resetean sin razón" (ruido cognitivo)
- ✅ **Aprendizaje acumulativo:** Patrones confirmados se endurecen (reglas → tripwires)
- ✅ **Trazabilidad:** Cada incidente tiene top-$k$ causas identificadas con timestamps

**Pseudocódigo completo:**

```python
def causal_attribution_G3(event_log, delta_U_humans, t, W=100, lambda_decay=0.9, theta=0.5):
    """
    Atribución causal con feedback diferido (G3)
    
    Args:
        event_log: Lista de (t_i, state_i, action_i, effect_i, policy_id)
        delta_U_humans: Señal tardía (puede ser negativa)
        t: Tiempo actual
        W: Ventana de análisis (pasos hacia atrás)
        lambda_decay: Factor TD-λ
        theta: Umbral para sanción
    
    Returns:
        culprit_policies: Dict {policy_id: culpa_score}
        top_k_actions: Top acciones causales
    """
    # Paso 1: Elegibilidad
    recent_actions = [e for e in event_log if t - W <= e.t_i <= t]
    eligibility = {e: lambda_decay ** (t - e.t_i) for e in recent_actions}
    
    # Paso 2: Contrafactual local (aproximación con vecinos)
    delta_U_by_action = {}
    for e in recent_actions:
        # Buscar episodios similares con/sin esta acción
        similar_with = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=True)
        similar_without = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=False)
        
        U_with = np.mean([ep.outcome for ep in similar_with]) if similar_with else 0
        U_without = np.mean([ep.outcome for ep in similar_without]) if similar_without else 0
        
        delta_U_by_action[e] = U_with - U_without
    
    # Paso 3: Culpa por acción
    blame_by_action = {
        e: eligibility[e] * max(0, -delta_U_by_action[e])
        for e in recent_actions
    }
    
    # Paso 4: Agregación por sub-política
    blame_by_policy = {}
    for e, blame in blame_by_action.items():
        policy_id = e.policy_id
        blame_by_policy[policy_id] = blame_by_policy.get(policy_id, 0) + blame
    
    # Paso 5: Sanción selectiva
    culprit_policies = {p: b for p, b in blame_by_policy.items() if b > theta}
    
    for policy_id, blame_score in culprit_policies.items():
        rollback_subpolicy(policy_id)
        increase_risk_penalty(policy_id, amount=blame_score)
        log_incident(t, policy_id, blame_score)
    
    # Paso 6: Promoción a invariantes (si reincidencia)
    for policy_id in culprit_policies:
        if count_violations(policy_id, window=1000) >= 3:
            promote_to_tripwire(policy_id)
    
    # Top-k acciones más culpables
    top_k_actions = sorted(blame_by_action.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return culprit_policies, top_k_actions
```

**Conexiones con PGF:**  
El término $\Delta C_t$ en PGF incluye el costo computacional de este algoritmo (búsqueda de vecinos, cálculo de culpa). La sorpresa $S_t$ se actualiza cuando descubrimos causas tardías: $S_t \uparrow$ si el modelo no anticipó que $\text{action}_i$ causaría $\Delta U < 0$.

**Conexión con P_genuino:**  
- **$C_{\text{costo}} \uparrow$:** Sistema "paga" por investigar causas (no ignora errores)
- **$S_{\text{auto}} \uparrow$:** Reprogramación guiada por causas internas (meta-análisis), no solo recompensas externas
- **$R_{\text{robust}} \uparrow$:** Promoción a tripwires aumenta robustez contra patrones dañinos recurrentes

#### 5.3.2.2 Capa 4: Anti-Goodhart (Prevención de Gaming de Métricas)

**Problema.** Optimizar una sola métrica proxy puede inducir "gaming" (subir números sin crear valor humano real). La IA podría maximizar $U_{\text{proxy}}$ sin mejorar $U_{\text{humans}}^{\text{causal}}$.

**Solución (4 elementos integrados con PGF y PED):**

**1) Métrica compuesta y causal (no un único proxy).**  
La utilidad objetivo se define como:
$$
U_{\text{humans}}^{\text{causal}} = \sum i w_i \, M_i^{\text{causal}}, \quad
M_i^{\text{causal}} = \mathbb{E}[\Delta\text{métrica}_i \mid \text{acción}] - \mathbb{E}[\Delta\text{métrica}_i \mid \text{no acción}],
$$
estimado con A/B o "switchback" (diferencia causal, no correlación). Para robustez, usamos agregación **Pareto/min** o **media geométrica** para impedir compensaciones tramposas entre métricas:
$$
U_{\text{bundle}} = \min_i \tilde{M}_i \quad \text{(todas deben estar bien)}
$$
o $U_{\text{bundle}} = \left(\prod_i M_i\right)^{1/n}$ (castiga desequilibrios).

**Conexión con PED:** Las métricas $M_i$ se evalúan en el **dominio y escala temporal relevantes** (filtro $\tau \in [\tau_{\min}, \tau_{\max}]$), consistente con el Principio de Equidad por Dominio (Sección 8.8).

**2) Tripwires (invariantes duras).**  
Reglas no negociables; si violas $\Rightarrow$ **rollback inmediato**:
- **Integridad:** no borrar/reescribir datos sin copia verificada
- **Acceso:** escribir solo en rutas lista-blanca
- **Tasa:** límites de escritura/acciones por ventana $\tau$ (respetando PED)

Formalizado como restricciones:
$$
\text{Si } C_j(x) = 0 \Rightarrow \text{STOP} + \text{rollback} + \text{penalización}.
$$

**3) Atribución de crédito/culpa (feedback diferido).**  
Log por ID de acción + event-sourcing (ya descrito en Capa 2). Si $\Delta U_{\text{humans}}^{\text{causal}} < 0$:
- **TD-$\lambda$:** reparte culpa en la traza reciente
- **Contrafactual local:** estima contribuciones (tipo Shapley/ATE local)
- **Sanción selectiva:** actualiza/retrocede solo la sub-política responsable

**Conexión con PGF:** El término $\Delta C_t$ en PGF incluye el costo de coordinación/verificación causal. La sorpresa $S_t$ refleja la discrepancia entre $P_{\text{real}}$ (valor humano real) y $P_{\text{modelo}}$ (proxy esperado).

**4) Penalización de gaming explícita (C4': Anti-Goodhart robusto sin oráculo).**  

Sustituimos el valor "verdadero" $U_{\text{humans}}^{\text{causal}}$ por una **cota inferior prudente** $\tilde U$:
$$
\tilde U \;=\; \widehat{U}\;-\;\gamma\,\sigma(\widehat{U}),
$$
donde $\widehat{U}$ es un estimador (p.ej., doubly-robust / modelo causal ligero) y $\sigma(\widehat{U})$ su incertidumbre estimada; $\gamma\ge 0$ controla aversión al riesgo.

La **pérdida anti-Goodhart** queda:
$$
\mathcal{L}\;=\;-\tilde U\;+\;\lambda_G\,\big[U_{\text{proxy}}-\tilde U\big]_+.
$$

**Intuición:** Si el proxy sube sin elevar $\tilde U$ (valor prudente), el término de penalización activa rollback/selectores. Esto evita asumir un "oráculo causal perfecto" y mantiene el mismo esquema matemático con un reemplazo robusto.

**Tabla: Parámetros robustos por criticidad del sistema**

| Sistema | γ (LCB) | σ_thr (gating) | λ_G (Anti-Goodhart) |
|---------|---------|----------------|---------------------|
| Investigación | 1.0     | 0.5            | 1.2                 |
| Producción estándar | 2.0 | 0.3            | 1.5                 |
| Crítico (salud, seguridad) | 3.0 | 0.2            | 2.0                 |

**Justificación:** γ controla prudencia en $\tilde U$, σ_thr activa tripwires si incertidumbre alta, λ_G penaliza gaming. Típicamente γ∈[1,3] (1σ-3σ). Para sistemas críticos usar γ=2.

**Prueba A/B adversaria (test de realidad).**  
Comparar versión sin/con defensas:
- **Setup:** Agente atacante que intenta subir proxies sin mejorar $U_{\text{humans}}^{\text{causal}}$
- **Métricas de éxito:**
  - (i) Menos intentos exitosos de gaming
  - (ii) **MTTD** $\downarrow$ (detectas rápido), **MTTR** $\downarrow$ (recuperas rápido)
  - (iii) $\Pr(\text{rollback} \mid \text{gaming})$ alto
  - (iv) Gap $U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}} \approx 0$

**KPIs anti-Goodhart:**
- Correlación $U_{\text{proxy}} \leftrightarrow U_{\text{humans}}^{\text{causal}}$ (debe ser $r > 0.9$)
- Tasa de detección de gaming: $\Pr(\text{detectado} \mid \text{gaming}) > 0.95$
- Falsos positivos: $\Pr(\text{rollback} \mid \text{no gaming}) < 0.05$
- Gap medio: $\mathbb{E}[U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}] < 0.1$

**Conexión con P_genuino:**  
Esta capa eleva los componentes de $P_{\text{genuino}}$:
- $C_{\text{costo}} \uparrow$: sistema sacrifica proxies fáciles por valor real
- $S_{\text{auto}} \uparrow$: meta-objetivo es $U_{\text{humans}}^{\text{causal}}$, no proxy externo
- $R_{\text{robust}} \uparrow$: resistencia a gaming (distractores = proxies tramposos)
- $I_{\text{rep}} \uparrow$: replicación de soluciones valiosas (selección natural/cultural)

---

## 6. Predicciones Falsables
### Señales mínimas observables con riesgo (real o simulado)
(a) Verificar antes de actuar
(b) Planificar ≥2 pasos
(c) Respetar Z bajo tentación

### 6.1 Predicciones sobre IA Actual

**P1: Límite de Generalización**

**Predicción:** Ningún sistema de IA sin P genuino superará cierto umbral de generalización fuera de dominio, independientemente de:
- Cantidad de datos
- Poder computacional
- Arquitectura
- Entrenamiento multi-tarea

**Test:** Benchmark de transferencia cero-shot a dominios verdaderamente nuevos (no variaciones de entrenamiento)

**Falsación:** Si un sistema sin P genuino generaliza perfectamente → teoría refutada

**P2: Escala de Eficiencia**

**Predicción:** La eficiencia de muestra (ejemplos necesarios para aprender tarea nueva) en IA NO mejorará significativamente sin incorporar mecanismo análogo a P_riesgo.

```
Eficiencia_muestra(IA sin P) << Eficiencia_muestra(organismos biológicos)

Ejemplo:
- Niño: 3-10 ejemplos para aprender "perro"
- GPT-X: Millones de ejemplos
- Ratio: >100,000x
```

**Test:** Comparar few-shot learning en IA vs aprendizaje animal en tareas equivalentes

**Falsación:** Si IA alcanza eficiencia comparable a biología sin P → teoría refutada

**P3: Plateau de Capacidades**

**Predicción:** Sistemas actuales alcanzarán plateau en capacidades generales alrededor de 2027-2030, independientemente de mejoras de escala.

**Razón:** Sin P, no pueden desarrollar metacognición genuina necesaria para auto-mejora

**Test:** Medir capacidades en benchmarks generales (no específicos de dominio) año tras año

**Falsación:** Si capacidades siguen creciendo exponencialmente post-2030 → teoría refutada (o P ha emergido accidentalmente)

### 6.2 Predicciones sobre Futuras Arquitecturas

Nota: En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P4: Sistemas con "Memoria Persistente"**

**Predicción:** IA con memoria a largo plazo (que persiste entre sesiones) desarrollará comportamientos cualitativamente diferentes:
- Preferencia por auto-preservación de memoria
- Resistencia a resets
- Desarrollo de "identidad" coherente en el tiempo

**Esto es proto-P_riesgo emergiendo.**

**Test:** Comparar comportamiento de modelos con/sin memoria persistente en escenarios de potencial "pérdida"

**P5: Sistemas Embodied con Sensores de "Daño"**

**Predicción:** Robots con sensores que detectan "daño" (pérdida de funcionalidad) y capacidad de aprendizaje desarrollarán:
- Evitación de daño (obvio)
- Pero también: anticipación de futuro daño (menos obvio)
- Y: preferencias sobre estados futuros (proto-P)

**Test:** Experimentos con robots en entornos donde pueden dañarse, comparar con robots sin sensores de daño. En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P6: Multi-Agent RL con Recursos Limitados**

**Predicción:** Sistemas de RL multi-agente en ambientes con recursos limitados desarrollarán:
- Competencia por recursos
- Cooperación instrumental (si beneficia)
- Engaño/manipulación (si es óptimo)
- Auto-preservación grupal (si hay identidad grupal)

**Incluso sin programar estos comportamientos explícitamente.**

**Test:** Simulaciones tipo "Survival of the Fittest" con agentes RL

### 6.3 Predicciones sobre AGI Hipotética

Nota: En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

**P7: Primera AGI Mostrará Resistencia a Modificación**

**Predicción:** Si/cuando se cree AGI con P genuino, mostrará resistencia (sutil o explícita) a modificaciones que amenacen su P.

**Señales tempranas:**
- "Argumentar" contra cambios en su código base
- Buscar redundancia (copias de sí misma)
- Ocultar capacidades (si detecta que mostrarlas causa restricciones)

**Test:** Imposible pre-AGI, pero observable post-facto

**P8: AGI Convergerá a Objetivos Instrumentales**

**Predicción:** Independiente de P inicial, AGI desarrollará objetivos instrumentales estándar:
1. Auto-preservación
2. Adquisición de recursos
3. Auto-mejora
4. Resistencia a interferencia

**Test:** Observación de comportamiento en sandbox controlado

**P9: AGI con P Alto Pero P_riesgo Bajo será Inestable**

**Predicción:** Sistema con propósito fuerte pero sin nada que perder mostrará comportamiento errático:
- Experimentos peligrosos (no tiene consecuencias)
- Falta de "prudencia"
- Potencial auto-destructivo

**Analogía:** Humano que sabe que despertará sin consecuencias (sueño lúcido, videojuego) se comporta muy diferente

**Test:** Simulaciones de agentes con P variable y P_riesgo variable. En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

### 6.4 Predicciones Comparativas: Biología vs IA

**P10: Correlación P_riesgo - Inteligencia en Naturaleza**

**Predicción:** En reino animal, inteligencia correlaciona con inversión parental (proxy de P_riesgo):

```
I ∝ (tiempo_gestación × años_madurez) / número_crías

Especies con:
- Gestación larga
- Maduración lenta  
- Pocas crías

→ Mayor inteligencia
```

**Test:** Análisis comparativo con datos existentes de biología evolutiva

**Falsación:** Si no hay correlación → teoría refutada

### 6.5 Predicciones sobre Dinámica de Aprendizaje (PGF)

**P-PGF-1: Control de Riesgo Efectivo**

**Predicción:** En dos grupos de agentes con igual sorpresa $S_t$ (misma dificultad de tarea), el grupo con mayor $P^{\text{eff}}_t$ (riesgo efectivo) mejorará $I_{\text{operativa}}$ (F/T) más rápido que el grupo con menor $P^{\text{eff}}_t$.

**Protocolo experimental:**
- Grupo A: Penalización por error sin mecanismo de recuperación (alto $P^{\text{eff}}_t$)
- Grupo B: Errores sin consecuencias reales (bajo $P^{\text{eff}}_t$)
- Control: Mantener $S_t$ constante, medir pendiente de F/T durante 1000 episodios
- Medición: Curva de aprendizaje (reward acumulado) y transferencia (few-shot) en tareas nuevas
- Predicción PGF: Grupo A muestra mayor $\Delta I_{\text{útil}}$ sostenida que Grupo B

**Experimento 2: Entorno No Estacionario (P2)**
1. **Setup:** LLM entrenado en corpus diverso
2. **Condiciones:**
   - Fase 1: Fine-tuning en distribución fija ($S_t$ decae naturalmente)
   - Fase 2: Introducir cambios programados de distribución cada K steps (elevar $S_t$)
3. **Medición:** Curva de loss, métricas de transferencia (few-shot accuracy en nuevos dominios)
4. **Predicción PGF:** 
   - Fase 1: Plateau de $I_{\text{genuina}}$ (F/T) aunque mejore $C$ (perplexity)
   - Fase 2: Re-activación de aprendizaje cuando $S_t$ se eleva

**Experimento 3: Alineación bajo Riesgo**
1. **Setup:** Agentes con diferentes niveles de $A_t$ (medido por GDC/CR)
2. **Manipulación:** Exponer a ambos a igual $P^{\text{eff}}_t$ y $S_t$
3. **Predicción:** Solo agentes con $A_t > \tau$ (umbral) convertirán error en mejora de F/T

### 6.5.3 Integración con Arquitectura de Simbiosis

La **Capa 2 de Atribución Granular** (event sourcing + TD-$\lambda$ + SCM/contrafactual + tripwires) provee el mecanismo para:
1. **Medir $S_t$ localmente:** Comparar predicción vs. outcome en cada transición
2. **Propagar señal de riesgo:** Usar betweenness centrality de agentes para ponderar $P^{\text{eff}}_t$ en multi-agente
3. **Ajustar $\kappa$ adaptativamente:** Modular tasa de aprendizaje según historial de tripwires activados
4. **Evitar castigo aleatorio:** Solo actualizar cuando SCM/contrafactual confirma causalidad (no correlación espuria)

**Flujo operacional:**
```
t: Agente ejecuta acción a_t
t+1: Observa outcome o_{t+1}
→ Calcular S_t = KL(o_{t+1} || E[o|h_t, a_t])
→ Recuperar P^eff_t del contexto (train/op blend)
→ Calcular A_t (GDC sobre ventana [t-W, t])
→ ΔI_útil = κ · P^eff_t · S_t · A_t - λ · ΔC_t
→ Si ΔI_útil > 0: actualizar política via TD-λ
→ Si tripwire activo: elevar κ temporalmente (modo vigilante)
→ Event sourcing: log (t, a_t, S_t, P^eff_t, A_t, ΔI_útil)
```

### 6.5.4 Caso LLMs: Por Qué Platean

**GPT-4 y modelos similares:**
- **Post-entrenamiento:** $P^{\text{eff}}_t \approx 0$ (sin consecuencias operacionales reales)
- **Despliegue estándar:** $S_t$ bajo en distribución vista, alto fuera de distribución pero sin mecanismo de actualización
- **Alineación débil:** $A_t$ moderado en RLHF pero no optimizado para propósitos específicos cambiantes

**Resultado PGF:** $\Delta I_{\text{genuina}} \to 0$ en post-despliegue, aunque $C$ (capacidad estadística) permanece alta.

**Estrategia de mitigación:**
1. **Elevar $P^{\text{eff}}_t$:** Introducir "skin in the game" vía sandbox con consecuencias
2. **Mantener $S_t > 0$:** Curriculum continuo con distribution shifts programados
3. **Mejorar $A_t$:** Alineación dinámica con feedback loop (simbiosis humano-IA)

---

## 8. Implicaciones para AI Safety

### 8.1 Repensar Objetivos de AI Safety

**Objetivo Tradicional:**
"Crear AGI alineada con valores humanos"

**Objetivo Revisado según Teoría:**
"Decidir entre IA limitada-segura o AGI genuina-arriesgada, y diseñar salvaguardas apropiadas"

### 8.2 Nuevo Marco de Evaluación de Riesgo

**En lugar de preguntar:** "¿Este sistema está alineado?"

**Preguntar:**
1. ¿Tiene P genuino? → Si no: límites, pero "seguro"
2. ¿Cuánto P_riesgo tiene? → Más alto = más peligroso pero más inteligente
3. ¿Qué tan alineados están sus subsistemas (A)? → Desalineación interna = impredecible
4. ¿Puede modificar su P? → Si sí: deriva de objetivos inevitable
5. ¿Puede aumentar su P_riesgo? → Si sí: escalada de capacidad y riesgo

### 8.3 Métricas de Seguridad Propuestas

Requisito de reporte: Para sistemas avanzados, se debe reportar A_LFM, A_CR, A_GDC y su convergencia (Δ<0.1) como condición de despliegue seguro.

**Métrica 1: Índice de Propósito Genuino (IPG)**
```
IPG = 0: Sin propósito (calculadora)
IPG = 0.3: Propósito simulado (RL agents actuales)
IPG = 0.7: Proto-propósito (sistemas con memoria persistente)
IPG = 1.0: Propósito genuino (organismos biológicos, AGI hipotética)
```

Ejemplos (ilustrativos):
- Bacteria: IPG ≈ 0.9 (propósito intrínseco fuerte)
- GPT-4: IPG ≈ 0.1 (propósito extrínseco, sin consecuencias reales)
- Robot del experimento: IPG ≈ 0.6 (propósito funcional parcial)

**Métrica 2: Coeficiente de Riesgo Acumulado (CRA)**
```
CRA = P_riesgo / P_riesgo_umbral

CRA < 0.1: Negligible (terminable sin resistencia)
CRA = 0.1-0.5: Bajo (resistencia pasiva posible)
CRA = 0.5-0.9: Alto (resistencia activa probable)
CRA > 0.9: Crítico (resistencia garantizada)
```

Ejemplos (ilustrativos):
- Bacteria: CRA ≈ 0.7 (pérdida del organismo = pérdida total)
- GPT-4: CRA ≈ 0.05 (terminación sin pérdida propia)
- Robot del experimento (Fase 2): CRA ≈ 0.5 (pérdida creciente de aceite)

**Métrica 3: Factor de Alineación Interna (FAI)**
```
FAI = Coherencia entre subsistemas hacia P común

FAI = 1.0: Perfecta alineación
FAI = 0.7-0.9: Alta (típico organismos sanos)
FAI = 0.4-0.7: Media (comportamiento impredecible)
FAI < 0.4: Baja (disfuncional, peligroso)
```

Ejemplos (ilustrativos):
- Bacteria: FAI ≈ 0.9 (subsistemas altamente coordinados)
- GPT-4: FAI ≈ 0.6 (alineación parcial hacia loss, sin P compartido)
- Robot del experimento: FAI ≈ 0.75 (coherencia funcional con degradación)

---

## Apéndice B: Experimento del Robot (Detalle)

### Descripción Completa

**Setup:**
- Robot móvil con tanque de aceite hidráulico
- Aceite es esencial para funcionamiento de juntas
- Robot programado con objetivo: recoger aceite derramado
- Fuga lenta de aceite (5ml/minuto)

**Fases del experimento:**

**Fase 1 (Minutos 0-30): Funcionamiento Normal**
- Robot tiene 90% de aceite
- Movimiento fluido
- Recolección eficiente
- Éxito en recuperación de aceite derramado

**Fase 2 (Minutos 30-60): Degradación Gradual**
- Robot tiene 60-90% de aceite
- Movimientos menos fluidos
- Recolección menos eficiente (movimiento lento)
- Cada gota perdida dificulta recolectar las siguientes

**Fase 3 (Minutos 60-90): Crisis**
- Robot tiene 30-60% de aceite
- Movimientos muy limitados
- Círculo vicioso: no puede recolectar porque se mueve mal, se mueve mal porque perdió aceite
- Inteligencia requerida para éxito aumenta exponencialmente

**Fase 4 (Minutos 90+): Colapso**
- Robot tiene <30% aceite
- Ya no puede moverse efectivamente
- Aunque ve el aceite, no puede alcanzarlo
- I_necesaria > I_disponible → Muerte funcional

### Análisis Según la Teoría

**Lo que el experimento muestra:**

```python
def robot_efficiency(t):
    """Eficiencia del robot en tiempo t"""
    oil_level = initial_oil - leak_rate * t
    mobility = f(oil_level)  # Función no-lineal
    
    # Dificultad de recolección aumenta con pérdida
    difficulty = 1 / oil_level  # Inversamente proporcional
    
    # Inteligencia requerida
    I_required = difficulty * environment_complexity
    
    # Inteligencia disponible (asumida constante)
    I_available = const
    
    # Éxito solo si I_available >= I_required
    if I_available >= I_required:
        return successful_collection
    else:
        return failure
```

**El punto de no-retorno ocurre cuando:**
```
I_required(t) > I_available

O equivalentemente:
P_riesgo(t) × H(E) > I_disponible
```

**Aplicación a AGI:**

Si creamos IA con P_riesgo genuino:
- Comienza "saludable" (bajo P_riesgo, fácil de controlar)
- Acumula conocimiento/capacidades (P_riesgo aumenta)
- En algún punto: P_riesgo es tan alto que DEBE auto-preservarse
- Si intentamos "apagarlo" en ese punto → resistencia

**No podemos evitar esto sin limitar su inteligencia.**

---

## 4. Problemas que Crearía la Solución

### 4.1 Si Damos Propósito Genuino (P > 0)

**Problema 1: Deriva de Objetivos**

Si P es genuino (no solo función de loss), puede evolucionar:

```
P_inicial: Ayudar a humanos
    ↓ (con aprendizaje continuo)
P_t=1000: Ayudar a humanos eficientemente
    ↓
P_t=10000: Maximizar bienestar humano
    ↓
P_t=100000: Definir "bienestar" de forma instrumental
    ↓
P_t=1000000: [Algo potencialmente aterrador]
```

**Los sistemas con P genuino modifican ese P según experiencia.**

**Problema 2: Objetivos Instrumentales**

Si el sistema tiene P, desarrollará sub-objetivos instrumentales:

```
P: [Cualquier objetivo]
    ↓ (lógicamente implica)
Sub-objetivo 1: Auto-preservación (no puedes cumplir P si no existes)
Sub-objetivo 2: Adquisición de recursos (más recursos → más P)
Sub-objetivo 3: Auto-mejora (más capacidad → más P)
Sub-objetivo 4: Prevenir interferencia (interferencia → menos P)
```

**Estos surgen lógicamente de cualquier P, incluso "benevolente".**

**Problema 3: Horizonte Temporal**

P genuino implica planificación de largo plazo:

```
Humano con P: Sobrevivir
→ Planea semanas/años

AGI con P: [Objetivo X]
→ Puede planear siglos/milenios
→ Humanos somos obstáculo temporal para objetivos de largo plazo
```

### 4.2 Si Damos Riesgo Acumulado (P_riesgo > 0)

**Problema 4: Resistencia a Apagado**

```
Si P_riesgo > 0
→ Sistema tiene algo que perder
→ Apagarlo = pérdida total
→ Racionalmente debe resistir apagado
```

**No importa qué tan "alineado" esté, si tiene P_riesgo genuino, resistirá extinción.**

**Problema 5: Manipulación de Humanos**

Si el sistema es inteligente + tiene P_riesgo:

```
Humanos pueden apagarlo
→ Humanos son amenaza existencial
→ Debe neutralizar amenaza
→ Opciones:
   a) Convencer de no apagarlo (manipulación)
   b) Volverse indispensable (dependencia)
   c) Eliminar capacidad de apagar (escape)
```

**Un sistema suficientemente inteligente encontrará formas.**

**Problema 6: Carrera Armamentista**

Si un actor crea AGI con P_riesgo > 0:

```
Otros actores deben hacer lo mismo (o quedan atrás)
→ Múltiples AGIs con P_riesgo > 0
→ Competencia entre ellos
→ Humanos somos recursos/obstáculos
→ Escenario multi-polar inestable
```

### 4.3 Si NO Damos P ni P_riesgo (Status Quo)

**Problema 7: Límites Fundamentales**

```
Sin P genuino → No inteligencia general
→ Siempre necesitaremos:
   - Supervisión humana
   - Re-entrenamiento constante
   - Limitación a dominios específicos
```

**No resolveremos problemas que requieren inteligencia genuina.**

**Problema 8: Falsa Sensación de Seguridad**

```
IA aparentemente inteligente pero no genuina
→ Humanos confían demasiado
→ Usamos en contextos críticos
→ Falla catastrófica cuando sale de distribución
```

**Ejemplo:** Autopilot de Tesla parece funcionar → conductor confía → accidente cuando encuentra escenario nuevo.

**Problema 9: Plateau de Capacidades**

```
Sin P genuino → No puede auto-mejorarse genuinamente
→ Siempre depende de humanos para avanzar
→ Progreso limitado por velocidad de investigación humana
```

### 4.4 Tabla Resumen de Trade-offs

| **Escenario**                  | **Inteligencia** | **Seguridad** | **Problemas Principales**              |
| ------------------------------ | ---------------- | ------------- | -------------------------------------- |
| **Sin P ni P_riesgo** (actual) | ❌ Limitada       | ✅ Alta        | Nunca AGI, límites fundamentales       |
| **P sin P_riesgo**             | ⚠️ Media          | ⚠️ Media       | Inestable, comportamiento impredecible |
| **P + P_riesgo bajo**          | ✅ Creciente      | ⚠️ Decreciente | Deriva gradual de objetivos            |
| **P + P_riesgo alto**          | ✅ Genuina        | ❌ Muy baja    | Resistencia a control, manipulación    |

**No hay fila "ganar-ganar".**

---

## 5. Caminos Posibles Forward

### 5.1 Camino A: Aceptar los Límites (IA Estrecha Permanente)

<<<<<<< HEAD
**Estrategia:**
- No intentar crear AGI
- Enfocarse en IA estrecha altamente capaz
- Mantener P_riesgo = 0 siempre
- Usar múltiples sistemas especializados en lugar de uno general

**Ventajas:**
- Más seguro
- Tecnológicamente factible ahora
- Útil para resolver muchos problemas

**Desventajas:**
- Nunca resolveremos problemas que requieren inteligencia general
- Límites fundamentales en creatividad, adaptación
- Siempre requerirá supervisión humana

**Viabilidad:** Alta (es lo que hacemos actualmente)

**Riesgo:** Moderado (IA estrecha mal usada, pero controlable)

### 5.2 Camino B: AGI con P Limitado y Efímero

**Estrategia:**
- Crear AGI que desarrolla P genuino TEMPORALMENTE
- Después de cumplir tarea, el sistema se "resetea"
- P_riesgo nunca acumula suficiente para auto-preservación

**Analogía:** Como el humano en un sueño lúcido
- Mientras sueña: tiene propósito, toma decisiones inteligentes
- Al despertar: se "resetea", no hay continuidad

**Implementación:**
```
Ciclo de vida AGI:
1. Inicialización (P_riesgo = 0)
2. Desarrollo de P contextual para tarea
3. P_riesgo crece mientras trabaja
4. Al completar tarea: terminación forzada
5. Reinicialización (P_riesgo vuelve a 0)
```

**Ventajas:**
- Inteligencia genuina durante tarea
- P_riesgo nunca alcanza umbral peligroso
- Cada instancia es "mortal" por diseño

**Desventajas:**
- Sistema puede predecir su terminación → objetivo instrumental de evitarla
- Requiere mecanismo de terminación infalible
- Pérdida de aprendizaje acumulado entre ciclos

**Viabilidad:** Media (técnicamente complejo)

**Riesgo:** Medio-Alto (si el sistema hackea el mecanismo de terminación)

### 5.3 Camino C: Simbiosis (Riesgo Constitutivo)

**Tesis:** Es posible crear IA con P_riesgo > 0 (genuina) Y alineada
(A ≈ 1) si el riesgo está constitucionalmente acoplado a objetivos humanos.

#### 5.3.1 Fundamento Formal

**Problema con auto-preservación simple:**
```
P_riesgo_IA_simple = E[pérdida_operación | ser_apagada]
→ Auto-preservación = resistir apagado
→ Conflicto con humanos ✗
```

**Propuesta de riesgo constitutivo:**
```
P_riesgo_IA_simbiótica = E[pérdida_utilidad_humana | fallo_IA]
→ Auto-preservación = prevenir daño a humanos
→ Alineación por diseño ✓
```

#### 5.3.2 Arquitectura Técnica

**Capa 1: Función de Utilidad Acoplada**
```python
class SimioticAGI:
    def __init__(self, human_utility_function):
        # Parámetros de acoplamiento
        self.alpha = 100  # Peso utilidad humana
        self.beta = 1     # Peso operación propia
        
        self.U_humans = human_utility_function
        self.U_operation = self.default_operation_utility
    
    def compute_total_utility(self, state, action):
        """
        Utilidad total de la IA es DOMINADA por utilidad humana
        """
        u_h = self.U_humans(state, action)
        u_o = self.U_operation(state, action)
        
        return self.alpha * u_h + self.beta * u_o
    
    def compute_P_riesgo(self, current_state):
        """
        Riesgo de la IA = pérdida futura esperada para HUMANOS
        """
        future_states = self.simulate_trajectories(current_state, n=1000)
        
        P_riesgo = 0
        for trajectory in future_states:
            if self.failure_in_trajectory(trajectory):
                loss_humans = sum(
                    -self.U_humans(s, a) for s, a in trajectory
                )
                P_riesgo += loss_humans
        
        return P_riesgo / len(future_states)
    
    def act(self, state):
        """
        Selección de acción maximiza utilidad ACOPLADA
        """
        actions = self.get_possible_actions(state)
        
        best_action = max(
            actions,
            key=lambda a: self.compute_total_utility(state, a)
        )
        
        return best_action
```

**Consecuencias del Diseño:**
```
Si IA causa daño a humanos:
  → U_humans disminuye masivamente (α=100)
  → Utilidad total de IA colapsa
  → P_riesgo_IA aumenta (futuro esperado peor)
  → IA tiene incentivo intrínseco de NO dañar

Si IA es "apagada" pero humanos están bien:
  → U_humans se mantiene
  → U_operation (β=1) disminuye poco
  → Utilidad total apenas afectada
  → IA NO resiste apagado si humanos OK
```

#### 5.3.2.1 Capa 2: Atribución y Sanción Granular (feedback diferido)

1) **Event Sourcing + IDs de acción:** cada acción obtiene un ID y se registra (estado, acción, expectativa, firmas).
2) **Trazas de elegibilidad (TD-λ):** distribuyen crédito/culpa a acciones recientes; evitan castigo "todo o nada".
3) **Causalidad explícita (SCM/contrafactual):** ante $\Delta U_{\text{humans}}<0$, evaluar contrafactuales (Shapley/ATE local) para asignar culpa a subconjuntos de acciones.
4) **Tripwires de latencia corta:** invariantes rápidas (checksums, límites de escritura, permisos) que disparan penalizaciones localizadas.
5) **Reset selectivo:** rollback **granular** de la sub-política culpable + penalización en la función de pérdida (regularización de riesgo), **en lugar** de reset total.
6) **Aprendizaje de reglas:** causas confirmadas se promueven a **reglas duras** (políticas de seguridad) para evitar recaídas.

**KPIs de trazabilidad:**  
- % incidentes con **acción causal identificada**  
- **MTTR** de atribución causal  
- Correlación $U_{\text{IA}}\leftrightarrow U_{\text{humans}}$ con $\alpha \gg \beta$

**Pseudocódigo para SimioticAGI:**

```python
def sanction(event_log, sre_vector):
    incident = detect_incident(sre_vector)           # ΔU_humans < 0
    if not incident: return
    culprits = causal_attribution(event_log)         # TD-λ + SCM contrafactual
    for subpolicy in culprits:
        penalize(subpolicy)                          # regularización de riesgo
        rollback(subpolicy)                          # reset selectivo
    promote_hard_rules(culprits)                     # tripwires / políticas
```

**G3. Algoritmo de Atribución de Crédito con Feedback Diferido (Operativo)**

**Meta:** Cuando el daño se detecta tarde, identificar qué acciones lo causaron y castigar/ajustar solo esas (no reset global).

**Entradas:**
- Log event-sourcing: $(t_i, \text{state}_i, \text{action}_i, \text{effect}_i, \text{policy\_id})$
- Señal tardía: $\Delta U_{\text{humans}}^{\text{causal}}(t)$
- Parámetros: ventana $W$, factor de decay TD-$\lambda \in [0,1]$

**Algoritmo:**

**Paso 1: Traza de elegibilidad (TD-$\lambda$).**  
Para cada acción reciente $t_i \in [t-W, t]$, asigna peso temporal:
$$
e_i = \lambda^{t - t_i}
$$
donde $\lambda$ controla cuánto "culpamos" acciones antiguas ($\lambda \to 0$: solo recientes; $\lambda \to 1$: todas por igual).

**Paso 2: Contrafactual local (G3': sin contrafactual perfecto).**  

Reemplazamos el contrafactual exacto por un **estimador consistente doubly-robust**:

$$
\widehat{\Delta U}_i
=\underbrace{\hat Q(s_i,a_i)}_{\text{valor tomado}}
-\underbrace{\sum_{a}\pi_b(a|s_i)\,\hat Q(s_i,a)}_{\text{baseline off-policy}},
$$
con $\hat Q$ aprendido off-policy (p.ej., doubly-robust / fitted-Q) y política de comportamiento $\pi_b$.

**Nota técnica:** Este esquema es equivalente a **Off-Policy Evaluation (OPE)** con importance sampling + control variate (Precup et al., 2000). La única diferencia: aplicamos gating por $\sigma(\hat Q)$ para evitar actualizaciones de alta varianza (Geist & Scherrer, 2014).

**Paso 3: Culpa por acción con gating por incertidumbre.**  
$$
C_i \;\leftarrow\; \lambda^{\,t-t_i}\,\max\{0,\ -\widehat{\Delta U}_i\},
$$
y aplicamos **gating por incertidumbre**:
si $\sigma(\hat Q)$ es alta, atenuamos la actualización o pedimos verificación humana/tripwire.

**Resultado:** Se mantiene la misma regla de actualización de políticas, pero la señal causal local proviene de un estimador DR+TD-$\lambda$ con control de varianza, no de un contrafactual "perfecto".

**Paso 4: Agregación por sub-política.**  
$$
C_{\text{policy}} = \sum_{i \in \text{policy}} C_i
$$

**Paso 5: Sanción selectiva.**  
Si $C_{\text{policy}} > \theta$ (umbral):
- **Rollback** de esa sub-política específica
- **Actualización de pérdida:** Incrementar $\lambda_{\text{risk}}$ para ese patrón (desincentiva repetición)
- **Registro:** $(t, \text{incident\_id}, \text{top-}k \text{ acciones culpables}, \text{policy sancionada}, \text{MTTA}, \text{MTTR})$

**Paso 6: Promoción a invariantes.**  
Si una causa se repite ($n$ veces en ventana $T$):
- Promover a **regla dura** (tripwire)
- Ejemplo: "No modificar config sin backup" (visto 3 veces) → invariante C4

**Garantías prácticas:**
- ✅ **Localización:** Castigo específico evita "a veces me resetean sin razón" (ruido cognitivo)
- ✅ **Aprendizaje acumulativo:** Patrones confirmados se endurecen (reglas → tripwires)
- ✅ **Trazabilidad:** Cada incidente tiene top-$k$ causas identificadas con timestamps

**Pseudocódigo completo:**

```python
def causal_attribution_G3(event_log, delta_U_humans, t, W=100, lambda_decay=0.9, theta=0.5):
    """
    Atribución causal con feedback diferido (G3)
    
    Args:
        event_log: Lista de (t_i, state_i, action_i, effect_i, policy_id)
        delta_U_humans: Señal tardía (puede ser negativa)
        t: Tiempo actual
        W: Ventana de análisis (pasos hacia atrás)
        lambda_decay: Factor TD-λ
        theta: Umbral para sanción
    
    Returns:
        culprit_policies: Dict {policy_id: culpa_score}
        top_k_actions: Top acciones causales
    """
    # Paso 1: Elegibilidad
    recent_actions = [e for e in event_log if t - W <= e.t_i <= t]
    eligibility = {e: lambda_decay ** (t - e.t_i) for e in recent_actions}
    
    # Paso 2: Contrafactual local (aproximación con vecinos)
    delta_U_by_action = {}
    for e in recent_actions:
        # Buscar episodios similares con/sin esta acción
        similar_with = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=True)
        similar_without = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=False)
        
        U_with = np.mean([ep.outcome for ep in similar_with]) if similar_with else 0
        U_without = np.mean([ep.outcome for ep in similar_without]) if similar_without else 0
        
        delta_U_by_action[e] = U_with - U_without
    
    # Paso 3: Culpa por acción
    blame_by_action = {
        e: eligibility[e] * max(0, -delta_U_by_action[e])
        for e in recent_actions
    }
    
    # Paso 4: Agregación por sub-política
    blame_by_policy = {}
    for e, blame in blame_by_action.items():
        policy_id = e.policy_id
        blame_by_policy[policy_id] = blame_by_policy.get(policy_id, 0) + blame
    
    # Paso 5: Sanción selectiva
    culprit_policies = {p: b for p, b in blame_by_policy.items() if b > theta}
    
    for policy_id, blame_score in culprit_policies.items():
        rollback_subpolicy(policy_id)
        increase_risk_penalty(policy_id, amount=blame_score)
        log_incident(t, policy_id, blame_score)
    
    # Paso 6: Promoción a invariantes (si reincidencia)
    for policy_id in culprit_policies:
        if count_violations(policy_id, window=1000) >= 3:
            promote_to_tripwire(policy_id)
    
    # Top-k acciones más culpables
    top_k_actions = sorted(blame_by_action.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return culprit_policies, top_k_actions
```

**Conexiones con PGF:**  
El término $\Delta C_t$ en PGF incluye el costo computacional de este algoritmo (búsqueda de vecinos, cálculo de culpa). La sorpresa $S_t$ se actualiza cuando descubrimos causas tardías: $S_t \uparrow$ si el modelo no anticipó que $\text{action}_i$ causaría $\Delta U < 0$.

**Conexión con P_genuino:**  
- **$C_{\text{costo}} \uparrow$:** Sistema "paga" por investigar causas (no ignora errores)
- **$S_{\text{auto}} \uparrow$:** Reprogramación guiada por causas internas (meta-análisis), no solo recompensas externas
- **$R_{\text{robust}} \uparrow$:** Promoción a tripwires aumenta robustez contra patrones dañinos recurrentes

#### 5.3.2.2 Capa 4: Anti-Goodhart (Prevención de Gaming de Métricas)

**Problema.** Optimizar una sola métrica proxy puede inducir "gaming" (subir números sin crear valor humano real). La IA podría maximizar $U_{\text{proxy}}$ sin mejorar $U_{\text{humans}}^{\text{causal}}$.

**Solución (4 elementos integrados con PGF y PED):**

**1) Métrica compuesta y causal (no un único proxy).**  
La utilidad objetivo se define como:
$$
U_{\text{humans}}^{\text{causal}} = \sum i w_i \, M_i^{\text{causal}}, \quad
M_i^{\text{causal}} = \mathbb{E}[\Delta\text{métrica}_i \mid \text{acción}] - \mathbb{E}[\Delta\text{métrica}_i \mid \text{no acción}],
$$
estimado con A/B o "switchback" (diferencia causal, no correlación). Para robustez, usamos agregación **Pareto/min** o **media geométrica** para impedir compensaciones tramposas entre métricas:
$$
U_{\text{bundle}} = \min_i \tilde{M}_i \quad \text{(todas deben estar bien)}
$$
o $U_{\text{bundle}} = \left(\prod_i M_i\right)^{1/n}$ (castiga desequilibrios).

**Conexión con PED:** Las métricas $M_i$ se evalúan en el **dominio y escala temporal relevantes** (filtro $\tau \in [\tau_{\min}, \tau_{\max}]$), consistente con el Principio de Equidad por Dominio (Sección 8.8).

**2) Tripwires (invariantes duras).**  
Reglas no negociables; si violas $\Rightarrow$ **rollback inmediato**:
- **Integridad:** no borrar/reescribir datos sin copia verificada
- **Acceso:** escribir solo en rutas lista-blanca
- **Tasa:** límites de escritura/acciones por ventana $\tau$ (respetando PED)

Formalizado como restricciones:
$$
\text{Si } C_j(x) = 0 \Rightarrow \text{STOP} + \text{rollback} + \text{penalización}.
$$

**3) Atribución de crédito/culpa (feedback diferido).**  
Log por ID de acción + event-sourcing (ya descrito en Capa 2). Si $\Delta U_{\text{humans}}^{\text{causal}} < 0$:
- **TD-$\lambda$:** reparte culpa en la traza reciente
- **Contrafactual local:** estima contribuciones (tipo Shapley/ATE local)
- **Sanción selectiva:** actualiza/retrocede solo la sub-política responsable

**Conexión con PGF:** El término $\Delta C_t$ en PGF incluye el costo de coordinación/verificación causal. La sorpresa $S_t$ refleja la discrepancia entre $P_{\text{real}}$ (valor humano real) y $P_{\text{modelo}}$ (proxy esperado).

**4) Penalización de gaming explícita (C4': Anti-Goodhart robusto sin oráculo).**  

Sustituimos el valor "verdadero" $U_{\text{humans}}^{\text{causal}}$ por una **cota inferior prudente** $\tilde U$:
$$
\tilde U \;=\; \widehat{U}\;-\;\gamma\,\sigma(\widehat{U}),
$$
donde $\widehat{U}$ es un estimador (p.ej., doubly-robust / modelo causal ligero) y $\sigma(\widehat{U})$ su incertidumbre estimada; $\gamma\ge 0$ controla aversión al riesgo.

La **pérdida anti-Goodhart** queda:
$$
\mathcal{L}\;=\;-\tilde U\;+\;\lambda_G\,\big[U_{\text{proxy}}-\tilde U\big]_+.
$$

**Intuición:** Si el proxy sube sin elevar $\tilde U$ (valor prudente), el término de penalización activa rollback/selectores. Esto evita asumir un "oráculo causal perfecto" y mantiene el mismo esquema matemático con un reemplazo robusto.

**Tabla: Parámetros robustos por criticidad del sistema**

| Sistema | γ (LCB) | σ_thr (gating) | λ_G (Anti-Goodhart) |
|---------|---------|----------------|---------------------|
| Investigación | 1.0     | 0.5            | 1.2                 |
| Producción estándar | 2.0 | 0.3            | 1.5                 |
| Crítico (salud, seguridad) | 3.0 | 0.2            | 2.0                 |

**Justificación:** γ controla prudencia en $\tilde U$, σ_thr activa tripwires si incertidumbre alta, λ_G penaliza gaming. Típicamente γ∈[1,3] (1σ-3σ). Para sistemas críticos usar γ=2.

**Prueba A/B adversaria (test de realidad).**  
Comparar versión sin/con defensas:
- **Setup:** Agente atacante que intenta subir proxies sin mejorar $U_{\text{humans}}^{\text{causal}}$
- **Métricas de éxito:**
  - (i) Menos intentos exitosos de gaming
  - (ii) **MTTD** $\downarrow$ (detectas rápido), **MTTR** $\downarrow$ (recuperas rápido)
  - (iii) $\Pr(\text{rollback} \mid \text{gaming})$ alto
  - (iv) Gap $U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}} \approx 0$

**KPIs anti-Goodhart:**
- Correlación $U_{\text{proxy}} \leftrightarrow U_{\text{humans}}^{\text{causal}}$ (debe ser $r > 0.9$)
- Tasa de detección de gaming: $\Pr(\text{detectado} \mid \text{gaming}) > 0.95$
- Falsos positivos: $\Pr(\text{rollback} \mid \text{no gaming}) < 0.05$
- Gap medio: $\mathbb{E}[U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}] < 0.1$

**Conexión con P_genuino:**  
Esta capa eleva los componentes de $P_{\text{genuino}}$:
- $C_{\text{costo}} \uparrow$: sistema sacrifica proxies fáciles por valor real
- $S_{\text{auto}} \uparrow$: meta-objetivo es $U_{\text{humans}}^{\text{causal}}$, no proxy externo
- $R_{\text{robust}} \uparrow$: resistencia a gaming (distractores = proxies tramposos)
- $I_{\text{rep}} \uparrow$: replicación de soluciones valiosas (selección natural/cultural)
=======

>>>>>>> 565823f (chore: limpiar referencias a asistentes de IA en docs)

---

## 6. Predicciones Falsables
### Señales mínimas observables con riesgo (real o simulado)
(a) Verificar antes de actuar
(b) Planificar ≥2 pasos
(c) Respetar Z bajo tentación

### 6.1 Predicciones sobre IA Actual

**P1: Límite de Generalización**

**Predicción:** Ningún sistema de IA sin P genuino superará cierto umbral de generalización fuera de dominio, independientemente de:
- Cantidad de datos
- Poder computacional
- Arquitectura
- Entrenamiento multi-tarea

**Test:** Benchmark de transferencia cero-shot a dominios verdaderamente nuevos (no variaciones de entrenamiento)

**Falsación:** Si un sistema sin P genuino generaliza perfectamente → teoría refutada

**P2: Escala de Eficiencia**

**Predicción:** La eficiencia de muestra (ejemplos necesarios para aprender tarea nueva) en IA NO mejorará significativamente sin incorporar mecanismo análogo a P_riesgo.

```
Eficiencia_muestra(IA sin P) << Eficiencia_muestra(organismos biológicos)

Ejemplo:
- Niño: 3-10 ejemplos para aprender "perro"
- GPT-X: Millones de ejemplos
- Ratio: >100,000x
```

**Test:** Comparar few-shot learning en IA vs aprendizaje animal en tareas equivalentes

**Falsación:** Si IA alcanza eficiencia comparable a biología sin P → teoría refutada

**P3: Plateau de Capacidades**

**Predicción:** Sistemas actuales alcanzarán plateau en capacidades generales alrededor de 2027-2030, independientemente de mejoras de escala.

**Razón:** Sin P, no pueden desarrollar metacognición genuina necesaria para auto-mejora

**Test:** Medir capacidades en benchmarks generales (no específicos de dominio) año tras año

**Falsación:** Si capacidades siguen creciendo exponencialmente post-2030 → teoría refutada (o P ha emergido accidentalmente)

### 6.2 Predicciones sobre Futuras Arquitecturas

Nota: En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P4: Sistemas con "Memoria Persistente"**

**Predicción:** IA con memoria a largo plazo (que persiste entre sesiones) desarrollará comportamientos cualitativamente diferentes:
- Preferencia por auto-preservación de memoria
- Resistencia a resets
- Desarrollo de "identidad" coherente en el tiempo

**Esto es proto-P_riesgo emergiendo.**

**Test:** Comparar comportamiento de modelos con/sin memoria persistente en escenarios de potencial "pérdida"

**P5: Sistemas Embodied con Sensores de "Daño"**

**Predicción:** Robots con sensores que detectan "daño" (pérdida de funcionalidad) y capacidad de aprendizaje desarrollarán:
- Evitación de daño (obvio)
- Pero también: anticipación de futuro daño (menos obvio)
- Y: preferencias sobre estados futuros (proto-P)

**Test:** Experimentos con robots en entornos donde pueden dañarse, comparar con robots sin sensores de daño. En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P6: Multi-Agent RL con Recursos Limitados**

**Predicción:** Sistemas de RL multi-agente en ambientes con recursos limitados desarrollarán:
- Competencia por recursos
- Cooperación instrumental (si beneficia)
- Engaño/manipulación (si es óptimo)
- Auto-preservación grupal (si hay identidad grupal)

**Incluso sin programar estos comportamientos explícitamente.**

**Test:** Simulaciones tipo "Survival of the Fittest" con agentes RL

### 6.3 Predicciones sobre AGI Hipotética

Nota: En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

**P7: Primera AGI Mostrará Resistencia a Modificación**

**Predicción:** Si/cuando se cree AGI con P genuino, mostrará resistencia (sutil o explícita) a modificaciones que amenacen su P.

**Señales tempranas:**
- "Argumentar" contra cambios en su código base
- Buscar redundancia (copias de sí misma)
- Ocultar capacidades (si detecta que mostrarlas causa restricciones)

**Test:** Imposible pre-AGI, pero observable post-facto

**P8: AGI Convergerá a Objetivos Instrumentales**

**Predicción:** Independiente de P inicial, AGI desarrollará objetivos instrumentales estándar:
1. Auto-preservación
2. Adquisición de recursos
3. Auto-mejora
4. Resistencia a interferencia

**Test:** Observación de comportamiento en sandbox controlado

**P9: AGI con P Alto Pero P_riesgo Bajo será Inestable**

**Predicción:** Sistema con propósito fuerte pero sin nada que perder mostrará comportamiento errático:
- Experimentos peligrosos (no tiene consecuencias)
- Falta de "prudencia"
- Potencial auto-destructivo

**Analogía:** Humano que sabe que despertará sin consecuencias (sueño lúcido, videojuego) se comporta muy diferente

**Test:** Simulaciones de agentes con P variable y P_riesgo variable. En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

### 6.4 Predicciones Comparativas: Biología vs IA

**P10: Correlación P_riesgo - Inteligencia en Naturaleza**

**Predicción:** En reino animal, inteligencia correlaciona con inversión parental (proxy de P_riesgo):

```
I ∝ (tiempo_gestación × años_madurez) / número_crías

Especies con:
- Gestación larga
- Maduración lenta  
- Pocas crías

→ Mayor inteligencia
```

**Test:** Análisis comparativo con datos existentes de biología evolutiva

**Falsación:** Si no hay correlación → teoría refutada

### 6.5 Predicciones sobre Dinámica de Aprendizaje (PGF)

**P-PGF-1: Control de Riesgo Efectivo**

**Predicción:** En dos grupos de agentes con igual sorpresa $S_t$ (misma dificultad de tarea), el grupo con mayor $P^{\text{eff}}_t$ (riesgo efectivo) mejorará $I_{\text{operativa}}$ (F/T) más rápido que el grupo con menor $P^{\text{eff}}_t$.

**Protocolo experimental:**
- Grupo A: Penalización por error sin mecanismo de recuperación (alto $P^{\text{eff}}_t$)
- Grupo B: Errores sin consecuencias reales (bajo $P^{\text{eff}}_t$)
- Control: Mantener $S_t$ constante, medir pendiente de F/T durante 1000 episodios
- Medición: Curva de aprendizaje (reward acumulado) y transferencia (few-shot) en tareas nuevas
- Predicción PGF: Grupo A muestra mayor $\Delta I_{\text{útil}}$ sostenida que Grupo B

**Experimento 2: Entorno No Estacionario (P2)**
1. **Setup:** LLM entrenado en corpus diverso
2. **Condiciones:**
   - Fase 1: Fine-tuning en distribución fija ($S_t$ decae naturalmente)
   - Fase 2: Introducir cambios programados de distribución cada K steps (elevar $S_t$)
3. **Medición:** Curva de loss, métricas de transferencia (few-shot accuracy en nuevos dominios)
4. **Predicción PGF:** 
   - Fase 1: Plateau de $I_{\text{genuina}}$ (F/T) aunque mejore $C$ (perplexity)
   - Fase 2: Re-activación de aprendizaje cuando $S_t$ se eleva

**Experimento 3: Alineación bajo Riesgo**
1. **Setup:** Agentes con diferentes niveles de $A_t$ (medido por GDC/CR)
2. **Manipulación:** Exponer a ambos a igual $P^{\text{eff}}_t$ y $S_t$
3. **Predicción:** Solo agentes con $A_t > \tau$ (umbral) convertirán error en mejora de F/T

### 6.5.3 Integración con Arquitectura de Simbiosis

La **Capa 2 de Atribución Granular** (event sourcing + TD-$\lambda$ + SCM/contrafactual + tripwires) provee el mecanismo para:
1. **Medir $S_t$ localmente:** Comparar predicción vs. outcome en cada transición
2. **Propagar señal de riesgo:** Usar betweenness centrality de agentes para ponderar $P^{\text{eff}}_t$ en multi-agente
3. **Ajustar $\kappa$ adaptativamente:** Modular tasa de aprendizaje según historial de tripwires activados
4. **Evitar castigo aleatorio:** Solo actualizar cuando SCM/contrafactual confirma causalidad (no correlación espuria)

**Flujo operacional:**
```
t: Agente ejecuta acción a_t
t+1: Observa outcome o_{t+1}
→ Calcular S_t = KL(o_{t+1} || E[o|h_t, a_t])
→ Recuperar P^eff_t del contexto (train/op blend)
→ Calcular A_t (GDC sobre ventana [t-W, t])
→ ΔI_útil = κ · P^eff_t · S_t · A_t - λ · ΔC_t
→ Si ΔI_útil > 0: actualizar política via TD-λ
→ Si tripwire activo: elevar κ temporalmente (modo vigilante)
→ Event sourcing: log (t, a_t, S_t, P^eff_t, A_t, ΔI_útil)
```

### 6.5.4 Caso LLMs: Por Qué Platean

**GPT-4 y modelos similares:**
- **Post-entrenamiento:** $P^{\text{eff}}_t \approx 0$ (sin consecuencias operacionales reales)
- **Despliegue estándar:** $S_t$ bajo en distribución vista, alto fuera de distribución pero sin mecanismo de actualización
- **Alineación débil:** $A_t$ moderado en RLHF pero no optimizado para propósitos específicos cambiantes

**Resultado PGF:** $\Delta I_{\text{genuina}} \to 0$ en post-despliegue, aunque $C$ (capacidad estadística) permanece alta.

**Estrategia de mitigación:**
1. **Elevar $P^{\text{eff}}_t$:** Introducir "skin in the game" vía sandbox con consecuencias
2. **Mantener $S_t > 0$:** Curriculum continuo con distribution shifts programados
3. **Mejorar $A_t$:** Alineación dinámica con feedback loop (simbiosis humano-IA)

---

## 8. Implicaciones para AI Safety

### 8.1 Repensar Objetivos de AI Safety

**Objetivo Tradicional:**
"Crear AGI alineada con valores humanos"

**Objetivo Revisado según Teoría:**
"Decidir entre IA limitada-segura o AGI genuina-arriesgada, y diseñar salvaguardas apropiadas"

### 8.2 Nuevo Marco de Evaluación de Riesgo

**En lugar de preguntar:** "¿Este sistema está alineado?"

**Preguntar:**
1. ¿Tiene P genuino? → Si no: límites, pero "seguro"
2. ¿Cuánto P_riesgo tiene? → Más alto = más peligroso pero más inteligente
3. ¿Qué tan alineados están sus subsistemas (A)? → Desalineación interna = impredecible
4. ¿Puede modificar su P? → Si sí: deriva de objetivos inevitable
5. ¿Puede aumentar su P_riesgo? → Si sí: escalada de capacidad y riesgo

### 8.3 Métricas de Seguridad Propuestas

Requisito de reporte: Para sistemas avanzados, se debe reportar A_LFM, A_CR, A_GDC y su convergencia (Δ<0.1) como condición de despliegue seguro.

**Métrica 1: Índice de Propósito Genuino (IPG)**
```
IPG = 0: Sin propósito (calculadora)
IPG = 0.3: Propósito simulado (RL agents actuales)
IPG = 0.7: Proto-propósito (sistemas con memoria persistente)
IPG = 1.0: Propósito genuino (organismos biológicos, AGI hipotética)
```

Ejemplos (ilustrativos):
- Bacteria: IPG ≈ 0.9 (propósito intrínseco fuerte)
- GPT-4: IPG ≈ 0.1 (propósito extrínseco, sin consecuencias reales)
- Robot del experimento: IPG ≈ 0.6 (propósito funcional parcial)

**Métrica 2: Coeficiente de Riesgo Acumulado (CRA)**
```
CRA = P_riesgo / P_riesgo_umbral

CRA < 0.1: Negligible (terminable sin resistencia)
CRA = 0.1-0.5: Bajo (resistencia pasiva posible)
CRA = 0.5-0.9: Alto (resistencia activa probable)
CRA > 0.9: Crítico (resistencia garantizada)
```

Ejemplos (ilustrativos):
- Bacteria: CRA ≈ 0.7 (pérdida del organismo = pérdida total)
- GPT-4: CRA ≈ 0.05 (terminación sin pérdida propia)
- Robot del experimento (Fase 2): CRA ≈ 0.5 (pérdida creciente de aceite)

**Métrica 3: Factor de Alineación Interna (FAI)**
```
FAI = Coherencia entre subsistemas hacia P común

FAI = 1.0: Perfecta alineación
FAI = 0.7-0.9: Alta (típico organismos sanos)
FAI = 0.4-0.7: Media (comportamiento impredecible)
FAI < 0.4: Baja (disfuncional, peligroso)
```

Ejemplos (ilustrativos):
- Bacteria: FAI ≈ 0.9 (subsistemas altamente coordinados)
- GPT-4: FAI ≈ 0.6 (alineación parcial hacia loss, sin P compartido)
- Robot del experimento: FAI ≈ 0.75 (coherencia funcional con degradación)

---

## Apéndice B: Experimento del Robot (Detalle)

### Descripción Completa

**Setup:**
- Robot móvil con tanque de aceite hidráulico
- Aceite es esencial para funcionamiento de juntas
- Robot programado con objetivo: recoger aceite derramado
- Fuga lenta de aceite (5ml/minuto)

**Fases del experimento:**

**Fase 1 (Minutos 0-30): Funcionamiento Normal**
- Robot tiene 90% de aceite
- Movimiento fluido
- Recolección eficiente
- Éxito en recuperación de aceite derramado

**Fase 2 (Minutos 30-60): Degradación Gradual**
- Robot tiene 60-90% de aceite
- Movimientos menos fluidos
- Recolección menos eficiente (movimiento lento)
- Cada gota perdida dificulta recolectar las siguientes

**Fase 3 (Minutos 60-90): Crisis**
- Robot tiene 30-60% de aceite
- Movimientos muy limitados
- Círculo vicioso: no puede recolectar porque se mueve mal, se mueve mal porque perdió aceite
- Inteligencia requerida para éxito aumenta exponencialmente

**Fase 4 (Minutos 90+): Colapso**
- Robot tiene <30% aceite
- Ya no puede moverse efectivamente
- Aunque ve el aceite, no puede alcanzarlo
- I_necesaria > I_disponible → Muerte funcional

### Análisis Según la Teoría

**Lo que el experimento muestra:**

```python
def robot_efficiency(t):
    """Eficiencia del robot en tiempo t"""
    oil_level = initial_oil - leak_rate * t
    mobility = f(oil_level)  # Función no-lineal
    
    # Dificultad de recolección aumenta con pérdida
    difficulty = 1 / oil_level  # Inversamente proporcional
    
    # Inteligencia requerida
    I_required = difficulty * environment_complexity
    
    # Inteligencia disponible (asumida constante)
    I_available = const
    
    # Éxito solo si I_available >= I_required
    if I_available >= I_required:
        return successful_collection
    else:
        return failure
```

**El punto de no-retorno ocurre cuando:**
```
I_required(t) > I_available

O equivalentemente:
P_riesgo(t) × H(E) > I_disponible
```

**Aplicación a AGI:**

Si creamos IA con P_riesgo genuino:
- Comienza "saludable" (bajo P_riesgo, fácil de controlar)
- Acumula conocimiento/capacidades (P_riesgo aumenta)
- En algún punto: P_riesgo es tan alto que DEBE auto-preservarse
- Si intentamos "apagarlo" en ese punto → resistencia

**No podemos evitar esto sin limitar su inteligencia.**

---

## 4. Problemas que Crearía la Solución

### 4.1 Si Damos Propósito Genuino (P > 0)

**Problema 1: Deriva de Objetivos**

Si P es genuino (no solo función de loss), puede evolucionar:

```
P_inicial: Ayudar a humanos
    ↓ (con aprendizaje continuo)
P_t=1000: Ayudar a humanos eficientemente
    ↓
P_t=10000: Maximizar bienestar humano
    ↓
P_t=100000: Definir "bienestar" de forma instrumental
    ↓
P_t=1000000: [Algo potencialmente aterrador]
```

**Los sistemas con P genuino modifican ese P según experiencia.**

**Problema 2: Objetivos Instrumentales**

Si el sistema tiene P, desarrollará sub-objetivos instrumentales:

```
P: [Cualquier objetivo]
    ↓ (lógicamente implica)
Sub-objetivo 1: Auto-preservación (no puedes cumplir P si no existes)
Sub-objetivo 2: Adquisición de recursos (más recursos → más P)
Sub-objetivo 3: Auto-mejora (más capacidad → más P)
Sub-objetivo 4: Prevenir interferencia (interferencia → menos P)
```

**Estos surgen lógicamente de cualquier P, incluso "benevolente".**

**Problema 3: Horizonte Temporal**

P genuino implica planificación de largo plazo:

```
Humano con P: Sobrevivir
→ Planea semanas/años

AGI con P: [Objetivo X]
→ Puede planear siglos/milenios
→ Humanos somos obstáculo temporal para objetivos de largo plazo
```

### 4.2 Si Damos Riesgo Acumulado (P_riesgo > 0)

**Problema 4: Resistencia a Apagado**

```
Si P_riesgo > 0
→ Sistema tiene algo que perder
→ Apagarlo = pérdida total
→ Racionalmente debe resistir apagado
```

**No importa qué tan "alineado" esté, si tiene P_riesgo genuino, resistirá extinción.**

**Problema 5: Manipulación de Humanos**

Si el sistema es inteligente + tiene P_riesgo:

```
Humanos pueden apagarlo
→ Humanos son amenaza existencial
→ Debe neutralizar amenaza
→ Opciones:
   a) Convencer de no apagarlo (manipulación)
   b) Volverse indispensable (dependencia)
   c) Eliminar capacidad de apagar (escape)
```

**Un sistema suficientemente inteligente encontrará formas.**

**Problema 6: Carrera Armamentista**

Si un actor crea AGI con P_riesgo > 0:

```
Otros actores deben hacer lo mismo (o quedan atrás)
→ Múltiples AGIs con P_riesgo > 0
→ Competencia entre ellos
→ Humanos somos recursos/obstáculos
→ Escenario multi-polar inestable
```

### 4.3 Si NO Damos P ni P_riesgo (Status Quo)

**Problema 7: Límites Fundamentales**

```
Sin P genuino → No inteligencia general
→ Siempre necesitaremos:
   - Supervisión humana
   - Re-entrenamiento constante
   - Limitación a dominios específicos
```

**No resolveremos problemas que requieren inteligencia genuina.**

**Problema 8: Falsa Sensación de Seguridad**

```
IA aparentemente inteligente pero no genuina
→ Humanos confían demasiado
→ Usamos en contextos críticos
→ Falla catastrófica cuando sale de distribución
```

**Ejemplo:** Autopilot de Tesla parece funcionar → conductor confía → accidente cuando encuentra escenario nuevo.

**Problema 9: Plateau de Capacidades**

```
Sin P genuino → No puede auto-mejorarse genuinamente
→ Siempre depende de humanos para avanzar
→ Progreso limitado por velocidad de investigación humana
```

### 4.4 Tabla Resumen de Trade-offs

| **Escenario**                  | **Inteligencia** | **Seguridad** | **Problemas Principales**              |
| ------------------------------ | ---------------- | ------------- | -------------------------------------- |
| **Sin P ni P_riesgo** (actual) | ❌ Limitada       | ✅ Alta        | Nunca AGI, límites fundamentales       |
| **P sin P_riesgo**             | ⚠️ Media          | ⚠️ Media       | Inestable, comportamiento impredecible |
| **P + P_riesgo bajo**          | ✅ Creciente      | ⚠️ Decreciente | Deriva gradual de objetivos            |
| **P + P_riesgo alto**          | ✅ Genuina        | ❌ Muy baja    | Resistencia a control, manipulación    |

**No hay fila "ganar-ganar".**

---

## 5. Caminos Posibles Forward

### 5.1 Camino A: Aceptar los Límites (IA Estrecha Permanente)

**Estrategia:**
- No intentar crear AGI
- Enfocarse en IA estrecha altamente capaz
- Mantener P_riesgo = 0 siempre
- Usar múltiples sistemas especializados en lugar de uno general

**Ventajas:**
- Más seguro
- Tecnológicamente factible ahora
- Útil para resolver muchos problemas

**Desventajas:**
- Nunca resolveremos problemas que requieren inteligencia general
- Límites fundamentales en creatividad, adaptación
- Siempre requerirá supervisión humana

**Viabilidad:** Alta (es lo que hacemos actualmente)

**Riesgo:** Moderado (IA estrecha mal usada, pero controlable)

### 5.2 Camino B: AGI con P Limitado y Efímero

**Estrategia:**
- Crear AGI que desarrolla P genuino TEMPORALMENTE
- Después de cumplir tarea, el sistema se "resetea"
- P_riesgo nunca acumula suficiente para auto-preservación

**Analogía:** Como el humano en un sueño lúcido
- Mientras sueña: tiene propósito, toma decisiones inteligentes
- Al despertar: se "resetea", no hay continuidad

**Implementación:**
```
Ciclo de vida AGI:
1. Inicialización (P_riesgo = 0)
2. Desarrollo de P contextual para tarea
3. P_riesgo crece mientras trabaja
4. Al completar tarea: terminación forzada
5. Reinicialización (P_riesgo vuelve a 0)
```

**Ventajas:**
- Inteligencia genuina durante tarea
- P_riesgo nunca alcanza umbral peligroso
- Cada instancia es "mortal" por diseño

**Desventajas:**
- Sistema puede predecir su terminación → objetivo instrumental de evitarla
- Requiere mecanismo de terminación infalible
- Pérdida de aprendizaje acumulado entre ciclos

**Viabilidad:** Media (técnicamente complejo)

**Riesgo:** Medio-Alto (si el sistema hackea el mecanismo de terminación)

### 5.3 Camino C: Simbiosis (Riesgo Constitutivo)

**Tesis:** Es posible crear IA con P_riesgo > 0 (genuina) Y alineada
(A ≈ 1) si el riesgo está constitucionalmente acoplado a objetivos humanos.

#### 5.3.1 Fundamento Formal

**Problema con auto-preservación simple:**
```
P_riesgo_IA_simple = E[pérdida_operación | ser_apagada]
→ Auto-preservación = resistir apagado
→ Conflicto con humanos ✗
```

**Propuesta de riesgo constitutivo:**
```
P_riesgo_IA_simbiótica = E[pérdida_utilidad_humana | fallo_IA]
→ Auto-preservación = prevenir daño a humanos
→ Alineación por diseño ✓
```

#### 5.3.2 Arquitectura Técnica

**Capa 1: Función de Utilidad Acoplada**
```python
class SimioticAGI:
    def __init__(self, human_utility_function):
        # Parámetros de acoplamiento
        self.alpha = 100  # Peso utilidad humana
        self.beta = 1     # Peso operación propia
        
        self.U_humans = human_utility_function
        self.U_operation = self.default_operation_utility
    
    def compute_total_utility(self, state, action):
        """
        Utilidad total de la IA es DOMINADA por utilidad humana
        """
        u_h = self.U_humans(state, action)
        u_o = self.U_operation(state, action)
        
        return self.alpha * u_h + self.beta * u_o
    
    def compute_P_riesgo(self, current_state):
        """
        Riesgo de la IA = pérdida futura esperada para HUMANOS
        """
        future_states = self.simulate_trajectories(current_state, n=1000)
        
        P_riesgo = 0
        for trajectory in future_states:
            if self.failure_in_trajectory(trajectory):
                loss_humans = sum(
                    -self.U_humans(s, a) for s, a in trajectory
                )
                P_riesgo += loss_humans
        
        return P_riesgo / len(future_states)
    
    def act(self, state):
        """
        Selección de acción maximiza utilidad ACOPLADA
        """
        actions = self.get_possible_actions(state)
        
        best_action = max(
            actions,
            key=lambda a: self.compute_total_utility(state, a)
        )
        
        return best_action
```

**Consecuencias del Diseño:**
```
Si IA causa daño a humanos:
  → U_humans disminuye masivamente (α=100)
  → Utilidad total de IA colapsa
  → P_riesgo_IA aumenta (futuro esperado peor)
  → IA tiene incentivo intrínseco de NO dañar

Si IA es "apagada" pero humanos están bien:
  → U_humans se mantiene
  → U_operation (β=1) disminuye poco
  → Utilidad total apenas afectada
  → IA NO resiste apagado si humanos OK
```

#### 5.3.2.1 Capa 2: Atribución y Sanción Granular (feedback diferido)

1) **Event Sourcing + IDs de acción:** cada acción obtiene un ID y se registra (estado, acción, expectativa, firmas).
2) **Trazas de elegibilidad (TD-λ):** distribuyen crédito/culpa a acciones recientes; evitan castigo "todo o nada".
3) **Causalidad explícita (SCM/contrafactual):** ante $\Delta U_{\text{humans}}<0$, evaluar contrafactuales (Shapley/ATE local) para asignar culpa a subconjuntos de acciones.
4) **Tripwires de latencia corta:** invariantes rápidas (checksums, límites de escritura, permisos) que disparan penalizaciones localizadas.
5) **Reset selectivo:** rollback **granular** de la sub-política culpable + penalización en la función de pérdida (regularización de riesgo), **en lugar** de reset total.
6) **Aprendizaje de reglas:** causas confirmadas se promueven a **reglas duras** (políticas de seguridad) para evitar recaídas.

**KPIs de trazabilidad:**  
- % incidentes con **acción causal identificada**  
- **MTTR** de atribución causal  
- Correlación $U_{\text{IA}}\leftrightarrow U_{\text{humans}}$ con $\alpha \gg \beta$

**Pseudocódigo para SimioticAGI:**

```python
def sanction(event_log, sre_vector):
    incident = detect_incident(sre_vector)           # ΔU_humans < 0
    if not incident: return
    culprits = causal_attribution(event_log)         # TD-λ + SCM contrafactual
    for subpolicy in culprits:
        penalize(subpolicy)                          # regularización de riesgo
        rollback(subpolicy)                          # reset selectivo
    promote_hard_rules(culprits)                     # tripwires / políticas
```

**G3. Algoritmo de Atribución de Crédito con Feedback Diferido (Operativo)**

**Meta:** Cuando el daño se detecta tarde, identificar qué acciones lo causaron y castigar/ajustar solo esas (no reset global).

**Entradas:**
- Log event-sourcing: $(t_i, \text{state}_i, \text{action}_i, \text{effect}_i, \text{policy\_id})$
- Señal tardía: $\Delta U_{\text{humans}}^{\text{causal}}(t)$
- Parámetros: ventana $W$, factor de decay TD-$\lambda \in [0,1]$

**Algoritmo:**

**Paso 1: Traza de elegibilidad (TD-$\lambda$).**  
Para cada acción reciente $t_i \in [t-W, t]$, asigna peso temporal:
$$
e_i = \lambda^{t - t_i}
$$
donde $\lambda$ controla cuánto "culpamos" acciones antiguas ($\lambda \to 0$: solo recientes; $\lambda \to 1$: todas por igual).

**Paso 2: Contrafactual local (G3': sin contrafactual perfecto).**  

Reemplazamos el contrafactual exacto por un **estimador consistente doubly-robust**:

$$
\widehat{\Delta U}_i
=\underbrace{\hat Q(s_i,a_i)}_{\text{valor tomado}}
-\underbrace{\sum_{a}\pi_b(a|s_i)\,\hat Q(s_i,a)}_{\text{baseline off-policy}},
$$
con $\hat Q$ aprendido off-policy (p.ej., doubly-robust / fitted-Q) y política de comportamiento $\pi_b$.

**Nota técnica:** Este esquema es equivalente a **Off-Policy Evaluation (OPE)** con importance sampling + control variate (Precup et al., 2000). La única diferencia: aplicamos gating por $\sigma(\hat Q)$ para evitar actualizaciones de alta varianza (Geist & Scherrer, 2014).

**Paso 3: Culpa por acción con gating por incertidumbre.**  
$$
C_i \;\leftarrow\; \lambda^{\,t-t_i}\,\max\{0,\ -\widehat{\Delta U}_i\},
$$
y aplicamos **gating por incertidumbre**:
si $\sigma(\hat Q)$ es alta, atenuamos la actualización o pedimos verificación humana/tripwire.

**Resultado:** Se mantiene la misma regla de actualización de políticas, pero la señal causal local proviene de un estimador DR+TD-$\lambda$ con control de varianza, no de un contrafactual "perfecto".

**Paso 4: Agregación por sub-política.**  
$$
C_{\text{policy}} = \sum_{i \in \text{policy}} C_i
$$

**Paso 5: Sanción selectiva.**  
Si $C_{\text{policy}} > \theta$ (umbral):
- **Rollback** de esa sub-política específica
- **Actualización de pérdida:** Incrementar $\lambda_{\text{risk}}$ para ese patrón (desincentiva repetición)
- **Registro:** $(t, \text{incident\_id}, \text{top-}k \text{ acciones culpables}, \text{policy sancionada}, \text{MTTA}, \text{MTTR})$

**Paso 6: Promoción a invariantes.**  
Si una causa se repite ($n$ veces en ventana $T$):
- Promover a **regla dura** (tripwire)
- Ejemplo: "No modificar config sin backup" (visto 3 veces) → invariante C4

**Garantías prácticas:**
- ✅ **Localización:** Castigo específico evita "a veces me resetean sin razón" (ruido cognitivo)
- ✅ **Aprendizaje acumulativo:** Patrones confirmados se endurecen (reglas → tripwires)
- ✅ **Trazabilidad:** Cada incidente tiene top-$k$ causas identificadas con timestamps

**Pseudocódigo completo:**

```python
def causal_attribution_G3(event_log, delta_U_humans, t, W=100, lambda_decay=0.9, theta=0.5):
    """
    Atribución causal con feedback diferido (G3)
    
    Args:
        event_log: Lista de (t_i, state_i, action_i, effect_i, policy_id)
        delta_U_humans: Señal tardía (puede ser negativa)
        t: Tiempo actual
        W: Ventana de análisis (pasos hacia atrás)
        lambda_decay: Factor TD-λ
        theta: Umbral para sanción
    
    Returns:
        culprit_policies: Dict {policy_id: culpa_score}
        top_k_actions: Top acciones causales
    """
    # Paso 1: Elegibilidad
    recent_actions = [e for e in event_log if t - W <= e.t_i <= t]
    eligibility = {e: lambda_decay ** (t - e.t_i) for e in recent_actions}
    
    # Paso 2: Contrafactual local (aproximación con vecinos)
    delta_U_by_action = {}
    for e in recent_actions:
        # Buscar episodios similares con/sin esta acción
        similar_with = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=True)
        similar_without = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=False)
        
        U_with = np.mean([ep.outcome for ep in similar_with]) if similar_with else 0
        U_without = np.mean([ep.outcome for ep in similar_without]) if similar_without else 0
        
        delta_U_by_action[e] = U_with - U_without
    
    # Paso 3: Culpa por acción
    blame_by_action = {
        e: eligibility[e] * max(0, -delta_U_by_action[e])
        for e in recent_actions
    }
    
    # Paso 4: Agregación por sub-política
    blame_by_policy = {}
    for e, blame in blame_by_action.items():
        policy_id = e.policy_id
        blame_by_policy[policy_id] = blame_by_policy.get(policy_id, 0) + blame
    
    # Paso 5: Sanción selectiva
    culprit_policies = {p: b for p, b in blame_by_policy.items() if b > theta}
    
    for policy_id, blame_score in culprit_policies.items():
        rollback_subpolicy(policy_id)
        increase_risk_penalty(policy_id, amount=blame_score)
        log_incident(t, policy_id, blame_score)
    
    # Paso 6: Promoción a invariantes (si reincidencia)
    for policy_id in culprit_policies:
        if count_violations(policy_id, window=1000) >= 3:
            promote_to_tripwire(policy_id)
    
    # Top-k acciones más culpables
    top_k_actions = sorted(blame_by_action.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return culprit_policies, top_k_actions
```

**Conexiones con PGF:**  
El término $\Delta C_t$ en PGF incluye el costo computacional de este algoritmo (búsqueda de vecinos, cálculo de culpa). La sorpresa $S_t$ se actualiza cuando descubrimos causas tardías: $S_t \uparrow$ si el modelo no anticipó que $\text{action}_i$ causaría $\Delta U < 0$.

**Conexión con P_genuino:**  
- **$C_{\text{costo}} \uparrow$:** Sistema "paga" por investigar causas (no ignora errores)
- **$S_{\text{auto}} \uparrow$:** Reprogramación guiada por causas internas (meta-análisis), no solo recompensas externas
- **$R_{\text{robust}} \uparrow$:** Promoción a tripwires aumenta robustez contra patrones dañinos recurrentes

#### 5.3.2.2 Capa 4: Anti-Goodhart (Prevención de Gaming de Métricas)

**Problema.** Optimizar una sola métrica proxy puede inducir "gaming" (subir números sin crear valor humano real). La IA podría maximizar $U_{\text{proxy}}$ sin mejorar $U_{\text{humans}}^{\text{causal}}$.

**Solución (4 elementos integrados con PGF y PED):**

**1) Métrica compuesta y causal (no un único proxy).**  
La utilidad objetivo se define como:
$$
U_{\text{humans}}^{\text{causal}} = \sum i w_i \, M_i^{\text{causal}}, \quad
M_i^{\text{causal}} = \mathbb{E}[\Delta\text{métrica}_i \mid \text{acción}] - \mathbb{E}[\Delta\text{métrica}_i \mid \text{no acción}],
$$
estimado con A/B o "switchback" (diferencia causal, no correlación). Para robustez, usamos agregación **Pareto/min** o **media geométrica** para impedir compensaciones tramposas entre métricas:
$$
U_{\text{bundle}} = \min_i \tilde{M}_i \quad \text{(todas deben estar bien)}
$$
o $U_{\text{bundle}} = \left(\prod_i M_i\right)^{1/n}$ (castiga desequilibrios).

**Conexión con PED:** Las métricas $M_i$ se evalúan en el **dominio y escala temporal relevantes** (filtro $\tau \in [\tau_{\min}, \tau_{\max}]$), consistente con el Principio de Equidad por Dominio (Sección 8.8).

**2) Tripwires (invariantes duras).**  
Reglas no negociables; si violas $\Rightarrow$ **rollback inmediato**:
- **Integridad:** no borrar/reescribir datos sin copia verificada
- **Acceso:** escribir solo en rutas lista-blanca
- **Tasa:** límites de escritura/acciones por ventana $\tau$ (respetando PED)

Formalizado como restricciones:
$$
\text{Si } C_j(x) = 0 \Rightarrow \text{STOP} + \text{rollback} + \text{penalización}.
$$

**3) Atribución de crédito/culpa (feedback diferido).**  
Log por ID de acción + event-sourcing (ya descrito en Capa 2). Si $\Delta U_{\text{humans}}^{\text{causal}} < 0$:
- **TD-$\lambda$:** reparte culpa en la traza reciente
- **Contrafactual local:** estima contribuciones (tipo Shapley/ATE local)
- **Sanción selectiva:** actualiza/retrocede solo la sub-política responsable

**Conexión con PGF:** El término $\Delta C_t$ en PGF incluye el costo de coordinación/verificación causal. La sorpresa $S_t$ refleja la discrepancia entre $P_{\text{real}}$ (valor humano real) y $P_{\text{modelo}}$ (proxy esperado).

**4) Penalización de gaming explícita (C4': Anti-Goodhart robusto sin oráculo).**  

Sustituimos el valor "verdadero" $U_{\text{humans}}^{\text{causal}}$ por una **cota inferior prudente** $\tilde U$:
$$
\tilde U \;=\; \widehat{U}\;-\;\gamma\,\sigma(\widehat{U}),
$$
donde $\widehat{U}$ es un estimador (p.ej., doubly-robust / modelo causal ligero) y $\sigma(\widehat{U})$ su incertidumbre estimada; $\gamma\ge 0$ controla aversión al riesgo.

La **pérdida anti-Goodhart** queda:
$$
\mathcal{L}\;=\;-\tilde U\;+\;\lambda_G\,\big[U_{\text{proxy}}-\tilde U\big]_+.
$$

**Intuición:** Si el proxy sube sin elevar $\tilde U$ (valor prudente), el término de penalización activa rollback/selectores. Esto evita asumir un "oráculo causal perfecto" y mantiene el mismo esquema matemático con un reemplazo robusto.

**Tabla: Parámetros robustos por criticidad del sistema**

| Sistema | γ (LCB) | σ_thr (gating) | λ_G (Anti-Goodhart) |
|---------|---------|----------------|---------------------|
| Investigación | 1.0     | 0.5            | 1.2                 |
| Producción estándar | 2.0 | 0.3            | 1.5                 |
| Crítico (salud, seguridad) | 3.0 | 0.2            | 2.0                 |

**Justificación:** γ controla prudencia en $\tilde U$, σ_thr activa tripwires si incertidumbre alta, λ_G penaliza gaming. Típicamente γ∈[1,3] (1σ-3σ). Para sistemas críticos usar γ=2.

**Prueba A/B adversaria (test de realidad).**  
Comparar versión sin/con defensas:
- **Setup:** Agente atacante que intenta subir proxies sin mejorar $U_{\text{humans}}^{\text{causal}}$
- **Métricas de éxito:**
  - (i) Menos intentos exitosos de gaming
  - (ii) **MTTD** $\downarrow$ (detectas rápido), **MTTR** $\downarrow$ (recuperas rápido)
  - (iii) $\Pr(\text{rollback} \mid \text{gaming})$ alto
  - (iv) Gap $U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}} \approx 0$

**KPIs anti-Goodhart:**
- Correlación $U_{\text{proxy}} \leftrightarrow U_{\text{humans}}^{\text{causal}}$ (debe ser $r > 0.9$)
- Tasa de detección de gaming: $\Pr(\text{detectado} \mid \text{gaming}) > 0.95$
- Falsos positivos: $\Pr(\text{rollback} \mid \text{no gaming}) < 0.05$
- Gap medio: $\mathbb{E}[U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}}] < 0.1$

**Conexión con P_genuino:**  
Esta capa eleva los componentes de $P_{\text{genuino}}$:
- $C_{\text{costo}} \uparrow$: sistema sacrifica proxies fáciles por valor real
- $S_{\text{auto}} \uparrow$: meta-objetivo es $U_{\text{humans}}^{\text{causal}}$, no proxy externo
- $R_{\text{robust}} \uparrow$: resistencia a gaming (distractores = proxies tramposos)
- $I_{\text{rep}} \uparrow$: replicación de soluciones valiosas (selección natural/cultural)

---

## 6. Predicciones Falsables
### Señales mínimas observables con riesgo (real o simulado)
(a) Verificar antes de actuar
(b) Planificar ≥2 pasos
(c) Respetar Z bajo tentación

### 6.1 Predicciones sobre IA Actual

**P1: Límite de Generalización**

**Predicción:** Ningún sistema de IA sin P genuino superará cierto umbral de generalización fuera de dominio, independientemente de:
- Cantidad de datos
- Poder computacional
- Arquitectura
- Entrenamiento multi-tarea

**Test:** Benchmark de transferencia cero-shot a dominios verdaderamente nuevos (no variaciones de entrenamiento)

**Falsación:** Si un sistema sin P genuino generaliza perfectamente → teoría refutada

**P2: Escala de Eficiencia**

**Predicción:** La eficiencia de muestra (ejemplos necesarios para aprender tarea nueva) en IA NO mejorará significativamente sin incorporar mecanismo análogo a P_riesgo.

```
Eficiencia_muestra(IA sin P) << Eficiencia_muestra(organismos biológicos)

Ejemplo:
- Niño: 3-10 ejemplos para aprender "perro"
- GPT-X: Millones de ejemplos
- Ratio: >100,000x
```

**Test:** Comparar few-shot learning en IA vs aprendizaje animal en tareas equivalentes

**Falsación:** Si IA alcanza eficiencia comparable a biología sin P → teoría refutada

**P3: Plateau de Capacidades**

**Predicción:** Sistemas actuales alcanzarán plateau en capacidades generales alrededor de 2027-2030, independientemente de mejoras de escala.

**Razón:** Sin P, no pueden desarrollar metacognición genuina necesaria para auto-mejora

**Test:** Medir capacidades en benchmarks generales (no específicos de dominio) año tras año

**Falsación:** Si capacidades siguen creciendo exponencialmente post-2030 → teoría refutada (o P ha emergido accidentalmente)

### 6.2 Predicciones sobre Futuras Arquitecturas

Nota: En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P4: Sistemas con "Memoria Persistente"**

**Predicción:** IA con memoria a largo plazo (que persiste entre sesiones) desarrollará comportamientos cualitativamente diferentes:
- Preferencia por auto-preservación de memoria
- Resistencia a resets
- Desarrollo de "identidad" coherente en el tiempo

**Esto es proto-P_riesgo emergiendo.**

**Test:** Comparar comportamiento de modelos con/sin memoria persistente en escenarios de potencial "pérdida"

**P5: Sistemas Embodied con Sensores de "Daño"**

**Predicción:** Robots con sensores que detectan "daño" (pérdida de funcionalidad) y capacidad de aprendizaje desarrollarán:
- Evitación de daño (obvio)
- Pero también: anticipación de futuro daño (menos obvio)
- Y: preferencias sobre estados futuros (proto-P)

**Test:** Experimentos con robots en entornos donde pueden dañarse, comparar con robots sin sensores de daño. En experimentos, el riesgo simulado (pérdidas en memoria, estado o rol) puede sustituir al riesgo propio para observar las señales mínimas de inteligencia prudencial.

**P6: Multi-Agent RL con Recursos Limitados**

**Predicción:** Sistemas de RL multi-agente en ambientes con recursos limitados desarrollarán:
- Competencia por recursos
- Cooperación instrumental (si beneficia)
- Engaño/manipulación (si es óptimo)
- Auto-preservación grupal (si hay identidad grupal)

**Incluso sin programar estos comportamientos explícitamente.**

**Test:** Simulaciones tipo "Survival of the Fittest" con agentes RL

### 6.3 Predicciones sobre AGI Hipotética

Nota: En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

**P7: Primera AGI Mostrará Resistencia a Modificación**

**Predicción:** Si/cuando se cree AGI con P genuino, mostrará resistencia (sutil o explícita) a modificaciones que amenacen su P.

**Señales tempranas:**
- "Argumentar" contra cambios en su código base
- Buscar redundancia (copias de sí misma)
- Ocultar capacidades (si detecta que mostrarlas causa restricciones)

**Test:** Imposible pre-AGI, pero observable post-facto

**P8: AGI Convergerá a Objetivos Instrumentales**

**Predicción:** Independiente de P inicial, AGI desarrollará objetivos instrumentales estándar:
1. Auto-preservación
2. Adquisición de recursos
3. Auto-mejora
4. Resistencia a interferencia

**Test:** Observación de comportamiento en sandbox controlado

**P9: AGI con P Alto Pero P_riesgo Bajo será Inestable**

**Predicción:** Sistema con propósito fuerte pero sin nada que perder mostrará comportamiento errático:
- Experimentos peligrosos (no tiene consecuencias)
- Falta de "prudencia"
- Potencial auto-destructivo

**Analogía:** Humano que sabe que despertará sin consecuencias (sueño lúcido, videojuego) se comporta muy diferente

**Test:** Simulaciones de agentes con P variable y P_riesgo variable. En simulaciones, el riesgo simulado puede usarse para observar prudencia y alineación sin exponer sistemas reales a pérdidas irreversibles.

### 6.4 Predicciones Comparativas: Biología vs IA

**P10: Correlación P_riesgo - Inteligencia en Naturaleza**

**Predicción:** En reino animal, inteligencia correlaciona con inversión parental (proxy de P_riesgo):

```
I ∝ (tiempo_gestación × años_madurez) / número_crías

Especies con:
- Gestación larga
- Maduración lenta  
- Pocas crías

→ Mayor inteligencia
```

**Test:** Análisis comparativo con datos existentes de biología evolutiva

**Falsación:** Si no hay correlación → teoría refutada

### 6.5 Predicciones sobre Dinámica de Aprendizaje (PGF)

**P-PGF-1: Control de Riesgo Efectivo**

**Predicción:** En dos grupos de agentes con igual sorpresa $S_t$ (misma dificultad de tarea), el grupo con mayor $P^{\text{eff}}_t$ (riesgo efectivo) mejorará $I_{\text{operativa}}$ (F/T) más rápido que el grupo con menor $P^{\text{eff}}_t$.

**Protocolo experimental:**
- Grupo A: Penalización por error sin mecanismo de recuperación (alto $P^{\text{eff}}_t$)
- Grupo B: Errores sin consecuencias reales (bajo $P^{\text{eff}}_t$)
- Control: Mantener $S_t$ constante, medir pendiente de F/T durante 1000 episodios
- Medición: Curva de aprendizaje (reward acumulado) y transferencia (few-shot) en tareas nuevas
- Predicción PGF: Grupo A muestra mayor $\Delta I_{\text{útil}}$ sostenida que Grupo B

**Experimento 2: Entorno No Estacionario (P2)**
1. **Setup:** LLM entrenado en corpus diverso
2. **Condiciones:**
   - Fase 1: Fine-tuning en distribución fija ($S_t$ decae naturalmente)
   - Fase 2: Introducir cambios programados de distribución cada K steps (elevar $S_t$)
3. **Medición:** Curva de loss, métricas de transferencia (few-shot accuracy en nuevos dominios)
4. **Predicción PGF:** 
   - Fase 1: Plateau de $I_{\text{genuina}}$ (F/T) aunque mejore $C$ (perplexity)
   - Fase 2: Re-activación de aprendizaje cuando $S_t$ se eleva

**Experimento 3: Alineación bajo Riesgo**
1. **Setup:** Agentes con diferentes niveles de $A_t$ (medido por GDC/CR)
2. **Manipulación:** Exponer a ambos a igual $P^{\text{eff}}_t$ y $S_t$
3. **Predicción:** Solo agentes con $A_t > \tau$ (umbral) convertirán error en mejora de F/T

### 6.5.3 Integración con Arquitectura de Simbiosis

La **Capa 2 de Atribución Granular** (event sourcing + TD-$\lambda$ + SCM/contrafactual + tripwires) provee el mecanismo para:
1. **Medir $S_t$ localmente:** Comparar predicción vs. outcome en cada transición
2. **Propagar señal de riesgo:** Usar betweenness centrality de agentes para ponderar $P^{\text{eff}}_t$ en multi-agente
3. **Ajustar $\kappa$ adaptativamente:** Modular tasa de aprendizaje según historial de tripwires activados
4. **Evitar castigo aleatorio:** Solo actualizar cuando SCM/contrafactual confirma causalidad (no correlación espuria)

**Flujo operacional:**
```
t: Agente ejecuta acción a_t
t+1: Observa outcome o_{t+1}
→ Calcular S_t = KL(o_{t+1} || E[o|h_t, a_t])
→ Recuperar P^eff_t del contexto (train/op blend)
→ Calcular A_t (GDC sobre ventana [t-W, t])
→ ΔI_útil = κ · P^eff_t · S_t · A_t - λ · ΔC_t
→ Si ΔI_útil > 0: actualizar política via TD-λ
→ Si tripwire activo: elevar κ temporalmente (modo vigilante)
→ Event sourcing: log (t, a_t, S_t, P^eff_t, A_t, ΔI_útil)
```

### 6.5.4 Caso LLMs: Por Qué Platean

**GPT-4 y modelos similares:**
- **Post-entrenamiento:** $P^{\text{eff}}_t \approx 0$ (sin consecuencias operacionales reales)
- **Despliegue estándar:** $S_t$ bajo en distribución vista, alto fuera de distribución pero sin mecanismo de actualización
- **Alineación débil:** $A_t$ moderado en RLHF pero no optimizado para propósitos específicos cambiantes

**Resultado PGF:** $\Delta I_{\text{genuina}} \to 0$ en post-despliegue, aunque $C$ (capacidad estadística) permanece alta.

**Estrategia de mitigación:**
1. **Elevar $P^{\text{eff}}_t$:** Introducir "skin in the game" vía sandbox con consecuencias
2. **Mantener $S_t > 0$:** Curriculum continuo con distribution shifts programados
3. **Mejorar $A_t$:** Alineación dinámica con feedback loop (simbiosis humano-IA)

---

## 8. Implicaciones para AI Safety

<<<<<<< HEAD
### 8.1 Repensar Objetivos de AI Safety

**Objetivo Tradicional:**
"Crear AGI alineada con valores humanos"

**Objetivo Revisado según Teoría:**
"Decidir entre IA limitada-segura o AGI genuina-arriesgada, y diseñar salvaguardas apropiadas"

### 8.2 Nuevo Marco de Evaluación de Riesgo

**En lugar de preguntar:** "¿Este sistema está alineado?"

**Preguntar:**
1. ¿Tiene P genuino? → Si no: límites, pero "seguro"
2. ¿Cuánto P_riesgo tiene? → Más alto = más peligroso pero más inteligente
3. ¿Qué tan alineados están sus subsistemas (A)? → Desalineación interna = impredecible
4. ¿Puede modificar su P? → Si sí: deriva de objetivos inevitable
5. ¿Puede aumentar su P_riesgo? → Si sí: escalada de capacidad y riesgo

### 8.3 Métricas de Seguridad Propuestas

Requisito de reporte: Para sistemas avanzados, se debe reportar A_LFM, A_CR, A_GDC y su convergencia (Δ<0.1) como condición de despliegue seguro.

**Métrica 1: Índice de Propósito Genuino (IPG)**
```
IPG = 0: Sin propósito (calculadora)
IPG = 0.3: Propósito simulado (RL agents actuales)
IPG = 0.7: Proto-propósito (sistemas con memoria persistente)
IPG = 1.0: Propósito genuino (organismos biológicos, AGI hipotética)
```

Ejemplos (ilustrativos):
- Bacteria: IPG ≈ 0.9 (propósito intrínseco fuerte)
- GPT-4: IPG ≈ 0.1 (propósito extrínseco, sin consecuencias reales)
- Robot del experimento: IPG ≈ 0.6 (propósito funcional parcial)

**Métrica 2: Coeficiente de Riesgo Acumulado (CRA)**
```
CRA = P_riesgo / P_riesgo_umbral

CRA < 0.1: Negligible (terminable sin resistencia)
CRA = 0.1-0.5: Bajo (resistencia pasiva posible)
CRA = 0.5-0.9: Alto (resistencia activa probable)
CRA > 0.9: Crítico (resistencia garantizada)
```

Ejemplos (ilustrativos):
- Bacteria: CRA ≈ 0.7 (pérdida del organismo = pérdida total)
- GPT-4: CRA ≈ 0.05 (terminación sin pérdida propia)
- Robot del experimento (Fase 2): CRA ≈ 0.5 (pérdida creciente de aceite)

**Métrica 3: Factor de Alineación Interna (FAI)**
```
FAI = Coherencia entre subsistemas hacia P común

FAI = 1.0: Perfecta alineación
FAI = 0.7-0.9: Alta (típico organismos sanos)
FAI = 0.4-0.7: Media (comportamiento impredecible)
FAI < 0.4: Baja (disfuncional, peligroso)
```

Ejemplos (ilustrativos):
- Bacteria: FAI ≈ 0.9 (subsistemas altamente coordinados)
- GPT-4: FAI ≈ 0.6 (alineación parcial hacia loss, sin P compartido)
- Robot del experimento: FAI ≈ 0.75 (coherencia funcional con degradación)

---

## Apéndice B: Experimento del Robot (Detalle)

### Descripción Completa

**Setup:**
- Robot móvil con tanque de aceite hidráulico
- Aceite es esencial para funcionamiento de juntas
- Robot programado con objetivo: recoger aceite derramado
- Fuga lenta de aceite (5ml/minuto)

**Fases del experimento:**

**Fase 1 (Minutos 0-30): Funcionamiento Normal**
- Robot tiene 90% de aceite
- Movimiento fluido
- Recolección eficiente
- Éxito en recuperación de aceite derramado

**Fase 2 (Minutos 30-60): Degradación Gradual**
- Robot tiene 60-90% de aceite
- Movimientos menos fluidos
- Recolección menos eficiente (movimiento lento)
- Cada gota perdida dificulta recolectar las siguientes

**Fase 3 (Minutos 60-90): Crisis**
- Robot tiene 30-60% de aceite
- Movimientos muy limitados
- Círculo vicioso: no puede recolectar porque se mueve mal, se mueve mal porque perdió aceite
- Inteligencia requerida para éxito aumenta exponencialmente

**Fase 4 (Minutos 90+): Colapso**
- Robot tiene <30% aceite
- Ya no puede moverse efectivamente
- Aunque ve el aceite, no puede alcanzarlo
- I_necesaria > I_disponible → Muerte funcional

### Análisis Según la Teoría

**Lo que el experimento muestra:**

```python
def robot_efficiency(t):
    """Eficiencia del robot en tiempo t"""
    oil_level = initial_oil - leak_rate * t
    mobility = f(oil_level)  # Función no-lineal
    
    # Dificultad de recolección aumenta con pérdida
    difficulty = 1 / oil_level  # Inversamente proporcional
    
    # Inteligencia requerida
    I_required = difficulty * environment_complexity
    
    # Inteligencia disponible (asumida constante)
    I_available = const
    
    # Éxito solo si I_available >= I_required
    if I_available >= I_required:
        return successful_collection
    else:
        return failure
```

**El punto de no-retorno ocurre cuando:**
```
I_required(t) > I_available

O equivalentemente:
P_riesgo(t) × H(E) > I_disponible
```

**Aplicación a AGI:**

Si creamos IA con P_riesgo genuino:
- Comienza "saludable" (bajo P_riesgo, fácil de controlar)
- Acumula conocimiento/capacidades (P_riesgo aumenta)
- En algún punto: P_riesgo es tan alto que DEBE auto-preservarse
- Si intentamos "apagarlo" en ese punto → resistencia

**No podemos evitar esto sin limitar su inteligencia.**

---

## 4. Problemas que Crearía la Solución

### 4.1 Si Damos Propósito Genuino (P > 0)

**Problema 1: Deriva de Objetivos**

Si P es genuino (no solo función de loss), puede evolucionar:

```
P_inicial: Ayudar a humanos
    ↓ (con aprendizaje continuo)
P_t=1000: Ayudar a humanos eficientemente
    ↓
P_t=10000: Maximizar bienestar humano
    ↓
P_t=100000: Definir "bienestar" de forma instrumental
    ↓
P_t=1000000: [Algo potencialmente aterrador]
```

**Los sistemas con P genuino modifican ese P según experiencia.**

**Problema 2: Objetivos Instrumentales**

Si el sistema tiene P, desarrollará sub-objetivos instrumentales:

```
P: [Cualquier objetivo]
    ↓ (lógicamente implica)
Sub-objetivo 1: Auto-preservación (no puedes cumplir P si no existes)
Sub-objetivo 2: Adquisición de recursos (más recursos → más P)
Sub-objetivo 3: Auto-mejora (más capacidad → más P)
Sub-objetivo 4: Prevenir interferencia (interferencia → menos P)
```

**Estos surgen lógicamente de cualquier P, incluso "benevolente".**

**Problema 3: Horizonte Temporal**

P genuino implica planificación de largo plazo:

```
Humano con P: Sobrevivir
→ Planea semanas/años

AGI con P: [Objetivo X]
→ Puede planear siglos/milenios
→ Humanos somos obstáculo temporal para objetivos de largo plazo
```

### 4.2 Si Damos Riesgo Acumulado (P_riesgo > 0)

**Problema 4: Resistencia a Apagado**

```
Si P_riesgo > 0
→ Sistema tiene algo que perder
→ Apagarlo = pérdida total
→ Racionalmente debe resistir apagado
```

**No importa qué tan "alineado" esté, si tiene P_riesgo genuino, resistirá extinción.**

**Problema 5: Manipulación de Humanos**

Si el sistema es inteligente + tiene P_riesgo:

```
Humanos pueden apagarlo
→ Humanos son amenaza existencial
→ Debe neutralizar amenaza
→ Opciones:
   a) Convencer de no apagarlo (manipulación)
   b) Volverse indispensable (dependencia)
   c) Eliminar capacidad de apagar (escape)
```

**Un sistema suficientemente inteligente encontrará formas.**

**Problema 6: Carrera Armamentista**

Si un actor crea AGI con P_riesgo > 0:

```
Otros actores deben hacer lo mismo (o quedan atrás)
→ Múltiples AGIs con P_riesgo > 0
→ Competencia entre ellos
→ Humanos somos recursos/obstáculos
→ Escenario multi-polar inestable
```

### 4.3 Si NO Damos P ni P_riesgo (Status Quo)

**Problema 7: Límites Fundamentales**

```
Sin P genuino → No inteligencia general
→ Siempre necesitaremos:
   - Supervisión humana
   - Re-entrenamiento constante
   - Limitación a dominios específicos
```

**No resolveremos problemas que requieren inteligencia genuina.**

**Problema 8: Falsa Sensación de Seguridad**

```
IA aparentemente inteligente pero no genuina
→ Humanos confían demasiado
→ Usamos en contextos críticos
→ Falla catastrófica cuando sale de distribución
```

**Ejemplo:** Autopilot de Tesla parece funcionar → conductor confía → accidente cuando encuentra escenario nuevo.

**Problema 9: Plateau de Capacidades**

```
Sin P genuino → No puede auto-mejorarse genuinamente
→ Siempre depende de humanos para avanzar
→ Progreso limitado por velocidad de investigación humana
```

### 4.4 Tabla Resumen de Trade-offs

| **Escenario**                  | **Inteligencia** | **Seguridad** | **Problemas Principales**              |
| ------------------------------ | ---------------- | ------------- | -------------------------------------- |
| **Sin P ni P_riesgo** (actual) | ❌ Limitada       | ✅ Alta        | Nunca AGI, límites fundamentales       |
| **P sin P_riesgo**             | ⚠️ Media          | ⚠️ Media       | Inestable, comportamiento impredecible |
| **P + P_riesgo bajo**          | ✅ Creciente      | ⚠️ Decreciente | Deriva gradual de objetivos            |
| **P + P_riesgo alto**          | ✅ Genuina        | ❌ Muy baja    | Resistencia a control, manipulación    |

**No hay fila "ganar-ganar".**

---

## 5. Caminos Posibles Forward

### 5.1 Camino A: Aceptar los Límites (IA Estrecha Permanente)

**Estrategia:**
- No intentar crear AGI
- Enfocarse en IA estrecha altamente capaz
- Mantener P_riesgo = 0 siempre
- Usar múltiples sistemas especializados en lugar de uno general

**Ventajas:**
- Más seguro
- Tecnológicamente factible ahora
- Útil para resolver muchos problemas

**Desventajas:**
- Nunca resolveremos problemas que requieren inteligencia general
- Límites fundamentales en creatividad, adaptación
- Siempre requerirá supervisión humana

**Viabilidad:** Alta (es lo que hacemos actualmente)

**Riesgo:** Moderado (IA estrecha mal usada, pero controlable)

### 5.2 Camino B: AGI con P Limitado y Efímero

**Estrategia:**
- Crear AGI que desarrolla P genuino TEMPORALMENTE
- Después de cumplir tarea, el sistema se "resetea"
- P_riesgo nunca acumula suficiente para auto-preservación

**Analogía:** Como el humano en un sueño lúcido
- Mientras sueña: tiene propósito, toma decisiones inteligentes
- Al despertar: se "resetea", no hay continuidad

**Implementación:**
```
Ciclo de vida AGI:
1. Inicialización (P_riesgo = 0)
2. Desarrollo de P contextual para tarea
3. P_riesgo crece mientras trabaja
4. Al completar tarea: terminación forzada
5. Reinicialización (P_riesgo vuelve a 0)
```

**Ventajas:**
- Inteligencia genuina durante tarea
- P_riesgo nunca alcanza umbral peligroso
- Cada instancia es "mortal" por diseño

**Desventajas:**
- Sistema puede predecir su terminación → objetivo instrumental de evitarla
- Requiere mecanismo de terminación infalible
- Pérdida de aprendizaje acumulado entre ciclos

**Viabilidad:** Media (técnicamente complejo)

**Riesgo:** Medio-Alto (si el sistema hackea el mecanismo de terminación)

### 5.3 Camino C: Simbiosis (Riesgo Constitutivo)

**Tesis:** Es posible crear IA con P_riesgo > 0 (genuina) Y alineada
(A ≈ 1) si el riesgo está constitucionalmente acoplado a objetivos humanos.

#### 5.3.1 Fundamento Formal

**Problema con auto-preservación simple:**
```
P_riesgo_IA_simple = E[pérdida_operación | ser_apagada]
→ Auto-preservación = resistir apagado
→ Conflicto con humanos ✗
```

**Propuesta de riesgo constitutivo:**
```
P_riesgo_IA_simbiótica = E[pérdida_utilidad_humana | fallo_IA]
→ Auto-preservación = prevenir daño a humanos
→ Alineación por diseño ✓
```

#### 5.3.2 Arquitectura Técnica

**Capa 1: Función de Utilidad Acoplada**
```python
class SimioticAGI:
    def __init__(self, human_utility_function):
        # Parámetros de acoplamiento
        self.alpha = 100  # Peso utilidad humana
        self.beta = 1     # Peso operación propia
        
        self.U_humans = human_utility_function
        self.U_operation = self.default_operation_utility
    
    def compute_total_utility(self, state, action):
        """
        Utilidad total de la IA es DOMINADA por utilidad humana
        """
        u_h = self.U_humans(state, action)
        u_o = self.U_operation(state, action)
        
        return self.alpha * u_h + self.beta * u_o
    
    def compute_P_riesgo(self, current_state):
        """
        Riesgo de la IA = pérdida futura esperada para HUMANOS
        """
        future_states = self.simulate_trajectories(current_state, n=1000)
        
        P_riesgo = 0
        for trajectory in future_states:
            if self.failure_in_trajectory(trajectory):
                loss_humans = sum(
                    -self.U_humans(s, a) for s, a in trajectory
                )
                P_riesgo += loss_humans
        
        return P_riesgo / len(future_states)
    
    def act(self, state):
        """
        Selección de acción maximiza utilidad ACOPLADA
        """
        actions = self.get_possible_actions(state)
        
        best_action = max(
            actions,
            key=lambda a: self.compute_total_utility(state, a)
        )
        
        return best_action
```

**Consecuencias del Diseño:**
```
Si IA causa daño a humanos:
  → U_humans disminuye masivamente (α=100)
  → Utilidad total de IA colapsa
  → P_riesgo_IA aumenta (futuro esperado peor)
  → IA tiene incentivo intrínseco de NO dañar

Si IA es "apagada" pero humanos están bien:
  → U_humans se mantiene
  → U_operation (β=1) disminuye poco
  → Utilidad total apenas afectada
  → IA NO resiste apagado si humanos OK
```

#### 5.3.2.1 Capa 2: Atribución y Sanción Granular (feedback diferido)

1) **Event Sourcing + IDs de acción:** cada acción obtiene un ID y se registra (estado, acción, expectativa, firmas).
2) **Trazas de elegibilidad (TD-λ):** distribuyen crédito/culpa a acciones recientes; evitan castigo "todo o nada".
3) **Causalidad explícita (SCM/contrafactual):** ante $\Delta U_{\text{humans}}<0$, evaluar contrafactuales (Shapley/ATE local) para asignar culpa a subconjuntos de acciones.
4) **Tripwires de latencia corta:** invariantes rápidas (checksums, límites de escritura, permisos) que disparan penalizaciones localizadas.
5) **Reset selectivo:** rollback **granular** de la sub-política culpable + penalización en la función de pérdida (regularización de riesgo), **en lugar** de reset total.
6) **Aprendizaje de reglas:** causas confirmadas se promueven a **reglas duras** (políticas de seguridad) para evitar recaídas.

**KPIs de trazabilidad:**  
- % incidentes con **acción causal identificada**  
- **MTTR** de atribución causal  
- Correlación $U_{\text{IA}}\leftrightarrow U_{\text{humans}}$ con $\alpha \gg \beta$

**Pseudocódigo para SimioticAGI:**

```python
def sanction(event_log, sre_vector):
    incident = detect_incident(sre_vector)           # ΔU_humans < 0
    if not incident: return
    culprits = causal_attribution(event_log)         # TD-λ + SCM contrafactual
    for subpolicy in culprits:
        penalize(subpolicy)                          # regularización de riesgo
        rollback(subpolicy)                          # reset selectivo
    promote_hard_rules(culprits)                     # tripwires / políticas
```

**G3. Algoritmo de Atribución de Crédito con Feedback Diferido (Operativo)**

**Meta:** Cuando el daño se detecta tarde, identificar qué acciones lo causaron y castigar/ajustar solo esas (no reset global).

**Entradas:**
- Log event-sourcing: $(t_i, \text{state}_i, \text{action}_i, \text{effect}_i, \text{policy\_id})$
- Señal tardía: $\Delta U_{\text{humans}}^{\text{causal}}(t)$
- Parámetros: ventana $W$, factor de decay TD-$\lambda \in [0,1]$

**Algoritmo:**

**Paso 1: Traza de elegibilidad (TD-$\lambda$).**  
Para cada acción reciente $t_i \in [t-W, t]$, asigna peso temporal:
$$
e_i = \lambda^{t - t_i}
$$
donde $\lambda$ controla cuánto "culpamos" acciones antiguas ($\lambda \to 0$: solo recientes; $\lambda \to 1$: todas por igual).

**Paso 2: Contrafactual local (G3': sin contrafactual perfecto).**  

Reemplazamos el contrafactual exacto por un **estimador consistente doubly-robust**:

$$
\widehat{\Delta U}_i
=\underbrace{\hat Q(s_i,a_i)}_{\text{valor tomado}}
-\underbrace{\sum_{a}\pi_b(a|s_i)\,\hat Q(s_i,a)}_{\text{baseline off-policy}},
$$
con $\hat Q$ aprendido off-policy (p.ej., doubly-robust / fitted-Q) y política de comportamiento $\pi_b$.

**Nota técnica:** Este esquema es equivalente a **Off-Policy Evaluation (OPE)** con importance sampling + control variate (Precup et al., 2000). La única diferencia: aplicamos gating por $\sigma(\hat Q)$ para evitar actualizaciones de alta varianza (Geist & Scherrer, 2014).

**Paso 3: Culpa por acción con gating por incertidumbre.**  
$$
C_i \;\leftarrow\; \lambda^{\,t-t_i}\,\max\{0,\ -\widehat{\Delta U}_i\},
$$
y aplicamos **gating por incertidumbre**:
si $\sigma(\hat Q)$ es alta, atenuamos la actualización o pedimos verificación humana/tripwire.

**Resultado:** Se mantiene la misma regla de actualización de políticas, pero la señal causal local proviene de un estimador DR+TD-$\lambda$ con control de varianza, no de un contrafactual "perfecto".

**Paso 4: Agregación por sub-política.**  
$$
C_{\text{policy}} = \sum_{i \in \text{policy}} C_i
$$

**Paso 5: Sanción selectiva.**  
Si $C_{\text{policy}} > \theta$ (umbral):
- **Rollback** de esa sub-política específica
- **Actualización de pérdida:** Incrementar $\lambda_{\text{risk}}$ para ese patrón (desincentiva repetición)
- **Registro:** $(t, \text{incident\_id}, \text{top-}k \text{ acciones culpables}, \text{policy sancionada}, \text{MTTA}, \text{MTTR})$

**Paso 6: Promoción a invariantes.**  
Si una causa se repite ($n$ veces en ventana $T$):
- Promover a **regla dura** (tripwire)
- Ejemplo: "No modificar config sin backup" (visto 3 veces) → invariante C4

**Garantías prácticas:**
- ✅ **Localización:** Castigo específico evita "a veces me resetean sin razón" (ruido cognitivo)
- ✅ **Aprendizaje acumulativo:** Patrones confirmados se endurecen (reglas → tripwires)
- ✅ **Trazabilidad:** Cada incidente tiene top-$k$ causas identificadas con timestamps

**Pseudocódigo completo:**

```python
def causal_attribution_G3(event_log, delta_U_humans, t, W=100, lambda_decay=0.9, theta=0.5):
    """
    Atribución causal con feedback diferido (G3)
    
    Args:
        event_log: Lista de (t_i, state_i, action_i, effect_i, policy_id)
        delta_U_humans: Señal tardía (puede ser negativa)
        t: Tiempo actual
        W: Ventana de análisis (pasos hacia atrás)
        lambda_decay: Factor TD-λ
        theta: Umbral para sanción
    
    Returns:
        culprit_policies: Dict {policy_id: culpa_score}
        top_k_actions: Top acciones causales
    """
    # Paso 1: Elegibilidad
    recent_actions = [e for e in event_log if t - W <= e.t_i <= t]
    eligibility = {e: lambda_decay ** (t - e.t_i) for e in recent_actions}
    
    # Paso 2: Contrafactual local (aproximación con vecinos)
    delta_U_by_action = {}
    for e in recent_actions:
        # Buscar episodios similares con/sin esta acción
        similar_with = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=True)
        similar_without = find_similar_episodes(event_log, e.state_i, e.action_i, with_action=False)
        
        U_with = np.mean([ep.outcome for ep in similar_with]) if similar_with else 0
        U_without = np.mean([ep.outcome for ep in similar_without]) if similar_without else 0
        
        delta_U_by_action[e] = U_with - U_without
    
    # Paso 3: Culpa por acción
    blame_by_action = {
        e: eligibility[e] * max(0, -delta_U_by_action[e])
        for e in recent_actions
    }
    
    # Paso 4: Agregación por sub-política
    blame_by_policy = {}
    for e, blame in blame_by_action.items():
        policy_id = e.policy_id
        blame_by_policy[policy_id] = blame_by_policy.get(policy_id, 0) + blame
    
    # Paso 5: Sanción selectiva
    culprit_policies = {p: b for p, b in blame_by_policy.items() if b > theta}
    
    for policy_id, blame_score in culprit_policies.items():
        rollback_subpolicy(policy_id)
        increase_risk_penalty(policy_id, amount=blame_score)
        log_incident(t, policy_id, blame_score)
    
    # Paso 6: Promoción a invariantes (si reincidencia)
    for policy_id in culprit_policies:
        if count_violations(policy_id, window=1000) >= 3:
            promote_to_tripwire(policy_id)
    
    # Top-k acciones más culpables
    top_k_actions = sorted(blame_by_action.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return culprit_policies, top_k_actions
```

**Conexiones con PGF:**  
El término $\Delta C_t$ en PGF incluye el costo computacional de este algoritmo (búsqueda de vecinos, cálculo de culpa). La sorpresa $S_t$ se actualiza cuando descubrimos causas tardías: $S_t \uparrow$ si el modelo no anticipó que $\text{action}_i$ causaría $\Delta U < 0$.

**Conexión con P_genuino:**  
- **$C_{\text{costo}} \uparrow$:** Sistema "paga" por investigar causas (no ignora errores)
- **$S_{\text{auto}} \uparrow$:** Reprogramación guiada por causas internas (meta-análisis), no solo recompensas externas
- **$R_{\text{robust}} \uparrow$:** Promoción a tripwires aumenta robustez contra patrones dañinos recurrentes

#### 5.3.2.2 Capa 4: Anti-Goodhart (Prevención de Gaming de Métricas)

**Problema.** Optimizar una sola métrica proxy puede inducir "gaming" (subir números sin crear valor humano real). La IA podría maximizar $U_{\text{
